from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.core.fields import RichTextField
from apps.core.images import fit_image_on_upload
from apps.core.models import PublishableModel


class Tag(models.Model):
    name = models.CharField(
        "Тэг",
        max_length=255,
        help_text="Тэг показывается только на тех языковых версиях сайта, где заполнено его название.",
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["name"]

    def __str__(self):
        return self.name_ru or self.name_en or self.name or ""


class NewsItem(PublishableModel):
    title = models.TextField("Заголовок", null=True)
    preview_image = models.ImageField(
        "Обложка",
        upload_to="news",
        null=True,
        blank=True,
        help_text="Изображение будет обрезано до пропорций 4:3.",
    )
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", related_name="news_items", blank=True)
    content = RichTextField("Текст новости", null=True, blank=False)
    creation_date = models.DateTimeField("Дата публикации", default=timezone.now, db_index=True)

    PREVIEW_SIZE = (1200, 900)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-creation_date"]

    def __str__(self):
        return self.title_ru or self.title_en or "Без названия"

    def get_absolute_url(self):
        return reverse("news:news_detail", args=[self.pk])

    def save(self, *args, **kwargs):
        fit_image_on_upload(self.preview_image, self.PREVIEW_SIZE)
        super().save(*args, **kwargs)
