from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


class Tag(models.Model):
    name = models.CharField(verbose_name="Тэг", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class NewsItem(models.Model):
    title = models.TextField(verbose_name="Название", unique=True)
    title_en = models.TextField(verbose_name="Name", unique=True, null=True, blank=True)

    preview_image = models.ImageField(
        verbose_name="Фотография",
        upload_to="news",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    content = RichTextUploadingField(
        verbose_name="Информация",
        null=False, blank=False
    )
    content_en = RichTextUploadingField(
        verbose_name="Content",
        null=True, blank=True
    )
    creation_date = models.DateTimeField(
        verbose_name="Дата создания",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        # Fallback to RU or EN as you prefer:
        if self.title:
            return self.title
        elif self.title_en:
            return self.title_en
        return "Untitled"

    def save(self, *args, **kwargs):
        if self.preview_image:
            img = Image.open(self.preview_image).convert('RGB')
            # resize to 600x450
            img = img.resize((600, 450))

            thumb_io = io.BytesIO()
            img.save(thumb_io, 'JPEG', quality=85)
            thumb_io.seek(0)

            self.preview_image = InMemoryUploadedFile(
                thumb_io,
                None,
                self.preview_image.name,
                'image/jpeg',
                thumb_io.getbuffer().nbytes,
                None
            )
        
        super().save(*args, **kwargs)
