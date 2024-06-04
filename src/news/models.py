from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(verbose_name="Тэг", max_length=255)
    name_en = models.CharField(verbose_name="Тэг на английском", max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class NewsItem(models.Model):
    title = models.TextField(verbose_name="Название")
    title_en = models.TextField(
        verbose_name="Название на английском",
        blank=True,
        null=True,
    )

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
    content_en = RichTextUploadingField(
        verbose_name="Информация на английском",
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(verbose_name="Название", default=timezone.now)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return self.title
