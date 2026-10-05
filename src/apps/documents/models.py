from pathlib import Path

from django.db import models

from apps.core.models import PublishableModel


class Document(PublishableModel):
    """Файл, публикуемый в одном из разделов сайта (единая модель вместо четырёх)."""

    class Category(models.TextChoices):
        APPLICANTS_CIS = "applicants_cis", "Абитуриентам: нормативные документы (РФ и СНГ)"
        APPLICANTS_FOREIGN = "applicants_foreign", "Абитуриентам: нормативные документы (иностранные граждане)"
        OPEN_DAYS_PRESENTATION = "open_days_presentation", "Дни открытых дверей: презентации"
        OPEN_DAYS_PHOTO = "open_days_photo", "Дни открытых дверей: фотографии"
        STUDENT_APPLICATION = "student_application", "Студентам: образцы заявлений"

    category = models.CharField("Раздел", max_length=64, choices=Category.choices, db_index=True)
    name = models.CharField("Название", max_length=255)
    file = models.FileField(
        "Файл",
        max_length=255,
        upload_to="documents",
        help_text="Для английской версии сайта можно загрузить отдельный файл; если его нет — показывается русский.",
    )
    position = models.IntegerField("Позиция", default=0)
    created_at = models.DateTimeField("Добавлен", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["category", "position", "name"]

    def __str__(self):
        return self.name_ru or self.name or ""

    @property
    def extension(self) -> str:
        return Path(self.file.name or "").suffix.lstrip(".").lower()
