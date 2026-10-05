import uuid
from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from apps.core.fields import RichTextField
from apps.core.models import PublishableModel


class SeminarSpeaker(models.Model):
    last_name = models.TextField("Фамилия")
    first_name = models.TextField("Имя")
    middle_name = models.TextField("Отчество", blank=True, null=True)
    image = models.ImageField("Фотография", upload_to="seminar_speakers", null=True, blank=True)
    job_title = ArrayField(
        models.CharField("Должность/Звание + Название организации", max_length=255),
        verbose_name="Должности и организации",
        size=20,
        blank=True,
        null=True,
    )
    academic_title = models.CharField("Ученое звание", max_length=255, blank=True, null=True)
    academic_degree = models.CharField("Ученая степень", max_length=255, blank=True, null=True)
    bio = RichTextField("Биография", blank=True, null=True)

    class Meta:
        verbose_name = "Докладчик"
        verbose_name_plural = "Докладчики"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return " ".join(part for part in (self.last_name, self.first_name, self.middle_name) if part)

    @property
    def full_name(self):
        return str(self)


class Seminar(PublishableModel):
    name = models.TextField("Название")
    position = models.IntegerField("Позиция", default=0)
    chair = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Председатель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="chaired_seminars",
    )
    organizer = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Организатор",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="organized_seminars",
    )
    department = models.ForeignKey(
        "academy.Department",
        verbose_name="Кафедра / департамент",
        related_name="seminars",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    description = RichTextField("Описание", blank=True, null=True)
    image = models.ImageField(
        "Обложка", default="default_seminar.jpg", upload_to="seminar_images/", null=True, blank=True
    )

    class Meta:
        verbose_name = "Научный семинар"
        verbose_name_plural = "Научные семинары"
        ordering = ["position", "name"]

    def __str__(self):
        return self.name or ""

    def get_absolute_url(self):
        return reverse("seminars:seminar_detail", args=[self.pk])


class SeminarReport(models.Model):
    seminar = models.ForeignKey(
        Seminar,
        verbose_name="Семинар",
        on_delete=models.CASCADE,
        related_name="reports",
        blank=True,
        null=True,
    )
    name = models.TextField("Тема доклада")
    date_start = models.DateField("Дата", blank=True, null=True)
    week = models.PositiveSmallIntegerField("Неделя", default=1)
    time_start = models.TimeField("Время начала", blank=True, null=True)
    time_end = models.TimeField("Время окончания", blank=True, null=True)
    speaker = models.ForeignKey(
        SeminarSpeaker,
        verbose_name="Докладчик",
        related_name="reports",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    online_meeting_url = models.URLField("Ссылка на онлайн-конференцию", blank=True, null=True)
    video = models.FileField("Видеозапись (файл)", upload_to="videos/", blank=True, null=True)
    video_recording = models.URLField("Видеозапись (ссылка)", blank=True, null=True)
    presentation_file = RichTextField(
        "Материалы доклада",
        blank=True,
        null=True,
        help_text="Презентация и другие материалы: загрузите файл через кнопку изображения/ссылки в редакторе.",
    )
    annotation = RichTextField("Аннотация", blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID для ссылки")

    class Meta:
        verbose_name = "Доклад"
        verbose_name_plural = "Доклады"
        ordering = ["-date_start", "week"]

    def __str__(self):
        return self.name or ""

    def get_absolute_url(self):
        if not self.seminar_id:
            return None
        return reverse("seminars:report_detail", args=[self.seminar_id, self.uuid])

    @property
    def is_past_due(self) -> bool:
        return bool(self.date_start) and date.today() > self.date_start
