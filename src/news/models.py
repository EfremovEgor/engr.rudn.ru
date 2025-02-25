from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


class Tag(models.Model):
    name = models.CharField(verbose_name="Тэг", max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class NewsItem(models.Model):
    title = models.TextField(verbose_name="Название", unique=True)
    preview_image = models.ImageField(
        verbose_name="Фотография",
        upload_to="news",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    content = RichTextUploadingField(
        verbose_name="Информация",
        blank=False,
        null=False,
    )
    creation_date = models.DateTimeField(verbose_name="Дата создания", default=timezone.now)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.preview_image:
            img = Image.open(self.preview_image)
            img = img.convert('RGB')

            img = img.resize((600, 450))

            thumb_io = io.BytesIO()
            img.save(thumb_io, 'JPEG', quality=85)
            thumb_io.seek(0)

            self.preview_image = InMemoryUploadedFile(
                thumb_io, None, self.preview_image.name, 'image/jpeg', thumb_io.getbuffer().nbytes, None
            )
        
        super().save(*args, **kwargs)
