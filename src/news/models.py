from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


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
        blank=False,
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    content = RichTextUploadingField(
        verbose_name="Информация",
        blank=False,
        null=False,
    )
    creation_date = models.DateTimeField(verbose_name="Название", auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return self.title
