"""Работа с файлами медиатеки: загрузка, индексация существующих файлов, поиск использований."""

from pathlib import Path
from urllib.parse import quote

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .models import MediaFile, MediaFolder

EDITOR_FOLDER = "Загрузки из редактора"
BLOCKED_EXTENSIONS = {"html", "htm", "js", "mjs", "php", "py", "sh", "exe", "bat", "cmd", "svgz"}


def validate_upload(uploaded):
    extension = Path(uploaded.name).suffix.lstrip(".").lower()
    if extension in BLOCKED_EXTENSIONS:
        raise ValidationError(f"Файлы .{extension} загружать нельзя.")
    if uploaded.size > settings.MEDIA_LIBRARY_MAX_UPLOAD_SIZE:
        limit = settings.MEDIA_LIBRARY_MAX_UPLOAD_SIZE // (1024 * 1024)
        raise ValidationError(f"Файл больше {limit} МБ.")


def get_folder(name: str, parent: MediaFolder | None = None) -> MediaFolder:
    folder, _ = MediaFolder.objects.get_or_create(name=name, parent=parent)
    return folder


def store_upload(uploaded, user=None, folder: MediaFolder | None = None, title: str = "") -> MediaFile:
    validate_upload(uploaded)
    media = MediaFile(file=uploaded, folder=folder, uploaded_by=user if user and user.is_authenticated else None)
    if title:
        media.title = title
    media.save()
    return media


def human_size(size: int) -> str:
    value = float(size or 0)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if value < 1024 or unit == "ГБ":
            return f"{value:.0f} {unit}" if unit == "Б" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} ГБ"


def index_existing_files(root: Path | None = None, folder_name: str = "Ранее загруженные") -> int:
    """Регистрирует в медиатеке файлы, уже лежащие в MEDIA_ROOT (сами файлы не трогаются)."""
    root = Path(root or settings.MEDIA_ROOT)
    known = set(MediaFile.objects.values_list("file", flat=True))
    base_folder = get_folder(folder_name)
    created = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        name = path.relative_to(root).as_posix()
        if name in known or name.startswith("library/"):
            continue
        subfolder = path.parent.relative_to(root).as_posix()
        folder = get_folder(subfolder, base_folder) if subfolder != "." else base_folder
        media = MediaFile(folder=folder)
        media.file.name = name
        media.save()
        created += 1
    return created


def _text_fields(model):
    for field in model._meta.get_fields():
        if isinstance(field, (models.TextField, models.CharField)) and not field.is_relation:
            if isinstance(field, (models.SlugField, models.EmailField)) or field.choices:
                continue
            yield field


def _file_fields(model):
    for field in model._meta.get_fields():
        if isinstance(field, models.FileField):
            yield field


def find_usages(media: MediaFile, limit: int = 50) -> list[dict]:
    """Где используется файл: ссылки в HTML-контенте и файловые поля моделей."""
    name = media.file.name
    if not name:
        return []
    results = []
    for model in apps.get_models():
        if model is MediaFile or model._meta.app_label in {"admin", "sessions", "contenttypes", "auth"}:
            continue
        q = Q()
        for field in _file_fields(model):
            q |= Q(**{field.name: name})
        for field in _text_fields(model):
            if isinstance(field, models.TextField):
                for variant in {name, quote(name)}:
                    q |= Q(**{f"{field.name}__contains": variant})
        if not q:
            continue
        for obj in model._base_manager.filter(q)[:limit]:
            results.append(
                {
                    "model": model._meta.verbose_name,
                    "object": str(obj),
                    "admin_url": _admin_url(obj),
                }
            )
            if len(results) >= limit:
                return results
    return results


def _admin_url(obj):
    from django.urls import NoReverseMatch, reverse

    try:
        return reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.pk])
    except NoReverseMatch:
        return None
