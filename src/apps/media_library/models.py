import mimetypes
from pathlib import Path

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import get_valid_filename
from PIL import Image
from slugify import slugify


class MediaFolder(models.Model):
    name = models.CharField("Название", max_length=255)
    parent = models.ForeignKey(
        "self", verbose_name="Родительская папка", on_delete=models.CASCADE, null=True, blank=True,
        related_name="children",
    )

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"
        ordering = ["parent__name", "name"]
        constraints = [
            models.UniqueConstraint(fields=["parent", "name"], name="media_folder_unique_name"),
        ]

    def __str__(self):
        return " / ".join(folder.name for folder in self.ancestors())

    def ancestors(self):
        chain, node, seen = [], self, set()
        while node is not None and node.pk not in seen:
            seen.add(node.pk)
            chain.append(node)
            node = node.parent
        return list(reversed(chain))


def upload_to(instance, filename):
    path = Path(filename)
    stem = slugify(path.stem, max_length=80, word_boundary=True) or "file"
    return f"library/{timezone.now():%Y/%m}/{get_valid_filename(stem + path.suffix.lower())}"


class MediaFile(models.Model):
    class Kind(models.TextChoices):
        IMAGE = "image", "Изображение"
        VIDEO = "video", "Видео"
        AUDIO = "audio", "Аудио"
        DOCUMENT = "document", "Документ"
        ARCHIVE = "archive", "Архив"
        OTHER = "other", "Другое"

    EXTENSION_KINDS = {
        Kind.IMAGE: {"jpg", "jpeg", "png", "gif", "webp", "svg", "bmp", "tif", "tiff", "avif"},
        Kind.VIDEO: {"mp4", "webm", "mov", "avi", "mkv", "m4v"},
        Kind.AUDIO: {"mp3", "wav", "ogg", "m4a"},
        Kind.DOCUMENT: {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "odt", "ods", "odp", "rtf", "txt", "csv"},
        Kind.ARCHIVE: {"zip", "rar", "7z", "tar", "gz"},
    }

    file = models.FileField("Файл", upload_to=upload_to, max_length=500)
    title = models.CharField("Название", max_length=255, blank=True)
    alt = models.CharField(
        "Альтернативный текст", max_length=255, blank=True, help_text="Описание изображения для незрячих и поисковиков."
    )
    folder = models.ForeignKey(
        MediaFolder, verbose_name="Папка", on_delete=models.SET_NULL, null=True, blank=True, related_name="files"
    )
    kind = models.CharField("Тип", max_length=16, choices=Kind.choices, default=Kind.OTHER, db_index=True)
    mime_type = models.CharField("MIME-тип", max_length=127, blank=True)
    size = models.PositiveBigIntegerField("Размер, байт", default=0)
    width = models.PositiveIntegerField("Ширина", null=True, blank=True)
    height = models.PositiveIntegerField("Высота", null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Загрузил", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField("Загружен", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.filename

    @property
    def filename(self) -> str:
        return Path(self.file.name or "").name

    @property
    def extension(self) -> str:
        return Path(self.file.name or "").suffix.lstrip(".").lower()

    @property
    def url(self) -> str:
        return self.file.url if self.file else ""

    @property
    def is_image(self) -> bool:
        return self.kind == self.Kind.IMAGE

    @classmethod
    def kind_for_extension(cls, extension: str) -> str:
        extension = extension.lower().lstrip(".")
        for kind, extensions in cls.EXTENSION_KINDS.items():
            if extension in extensions:
                return kind
        return cls.Kind.OTHER

    def fill_metadata(self):
        """Заполняет тип, размер и габариты по содержимому файла."""
        if not self.file:
            return
        self.kind = self.kind_for_extension(self.extension)
        self.mime_type = mimetypes.guess_type(self.file.name)[0] or ""
        try:
            self.size = self.file.size
        except (OSError, ValueError):
            self.size = 0
        if not self.title:
            self.title = Path(self.file.name).stem.replace("_", " ").replace("-", " ")[:255]
        if self.kind == self.Kind.IMAGE and self.extension != "svg":
            try:
                self.file.seek(0)
                with Image.open(self.file) as image:
                    self.width, self.height = image.size
                self.file.seek(0)
            except Exception:
                self.width = self.height = None

    def save(self, *args, **kwargs):
        if self.file and (not self.pk or not getattr(self.file, "_committed", True) or not self.size):
            self.fill_metadata()
        super().save(*args, **kwargs)
