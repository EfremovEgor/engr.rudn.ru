from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext as _


class BaseDocument(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    name_en = models.CharField(_("Название (EN)"), max_length=255, blank=True, null=True)
    file = models.FileField(
        max_length=255,
        verbose_name="Файл",
        upload_to="documents",
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True
        ordering = ["name"]

    @property
    def title(self):
        return self.name_en if get_language() == "en" and self.name_en else self.name

    def __str__(self):
        return self.title

class ApplicantsCISNormativeDocument(BaseDocument):
    class Meta:
        verbose_name = "Ссылка на нормативный документ для граждан российской федерации и стран СНГ"
        verbose_name_plural = "Абитуриенты ссылки на нормативные документы для граждан российской федерации и стран СНГ"


class ApplicantsForeignNormativeDocument(BaseDocument):
    class Meta:
        verbose_name = "Ссылка на нормативный документ для иностранных граждан"
        verbose_name_plural = (
            "Абитуриенты ссылки на нормативные документы для иностранных граждан"
        )


class OpenDaysFiles(BaseDocument):
    TYPES = [
        ("Презентация", "Презентация"),
        ("Фотография", "Фотография"),
    ]
    type = models.CharField(verbose_name="Тип файла", max_length=255, choices=TYPES)

    class Meta:
        verbose_name = "Файл для дня открытых дверей"
        verbose_name_plural = "Абитуриенты файлы для дня открытых дверей"


class StudentsApplications(BaseDocument):
    position = models.IntegerField("Позиция")

    class Meta:
        verbose_name = "Образец заявления"
        verbose_name_plural = "Студенты образцы заявлений"
        ordering = ["position"]

    def __str__(self) -> str:
        return f"{self.position} - {self.name}"
