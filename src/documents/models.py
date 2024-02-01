from django.db import models


class BaseDocument(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    file = models.FileField(
        max_length=255,
        verbose_name="Файл",
        upload_to="documents",
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


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

    def __str__(self) -> str:
        return f"{self.position} - {self.name}"
