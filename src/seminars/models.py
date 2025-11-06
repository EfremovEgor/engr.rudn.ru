from django.db import models
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField, DateRangeField
from pages.models import DepartmentInfo
from datetime import date


class SeminarSpeaker(models.Model):
    first_name = models.TextField(verbose_name="Имя")
    last_name = models.TextField(verbose_name="Фамилия")
    middle_name = models.TextField(verbose_name="Отчество", blank=True, null=True)
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="seminar_speakers",
        null=True,
        blank=True,
    )
    job_title = ArrayField(
        models.CharField(
            verbose_name="Должность/Звание + Название организации", max_length=255
        ),
        verbose_name="Должности/Звания",
        size=20,
        blank=True,
        null=True,
    )

    academic_title = models.CharField(
        verbose_name="Ученое звание", max_length=255, blank=True, null=True
    )

    academic_degree = models.CharField(
        verbose_name="Ученая степень", max_length=255, blank=True, null=True
    )
    bio = RichTextUploadingField(
        verbose_name="Биография",
        blank=True,
        null=True,
    )
    bio_en = RichTextUploadingField("Биография (англ.)", blank=True, null=True)

    class Meta:
        verbose_name = "Докладчик"
        verbose_name_plural = "Докладчики"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class SeminarReport(models.Model):
    name = models.TextField(verbose_name="Название")
    name_en = models.TextField("Название (англ.)", blank=True, null=True)
    date_start = models.DateField(
        verbose_name="Дата начала",
        blank=True,
        null=True,
    )
    week = models.PositiveSmallIntegerField(verbose_name="Неделя")
    time_start = models.TimeField(
        verbose_name="Время начала",
        blank=True,
        null=True,
    )
    time_end = models.TimeField(
        verbose_name="Время завершения",
        blank=True,
        null=True,
    )
    speaker = models.ForeignKey(
        SeminarSpeaker,
        verbose_name="Докладчик",
        related_name="speaker_report",
        default="profile_default.png",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    online_meeting_url = models.URLField(
        verbose_name="Ссылка на онлайн-конференцию",
        blank=True,
        null=True,
    )
    video_recording = models.URLField(
        verbose_name="Video recording URL",
        blank=True, null=True
    )
    presentation_file = RichTextUploadingField(
        verbose_name="Presentation URL",
        blank=True, null=True
    )
    annotation = RichTextUploadingField(
        verbose_name="Аннотация",
        blank=True,
        null=True,
    )
    annotation_en = RichTextUploadingField("Аннотация (англ.)", blank=True, null=True)

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        verbose_name="UUID for URL"
    )

    class Meta:
        verbose_name = "Доклад"
        verbose_name_plural = "Доклады"

    def __str__(self):
        return self.name

    @property
    def is_past_due(self):
        return date.today() > self.date_start


class Seminar(models.Model):
    name = models.TextField(verbose_name="Название")
    name_en = models.TextField("Название (англ.)", blank=True, null=True)
    chair1 = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Председатель",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='seminar_chairman'
    )
    organizer1 = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Организатор",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='seminar_organizer'
    )
    department = models.ForeignKey(
        DepartmentInfo,
        verbose_name="Департамент",
        related_name="department_seminar",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    description = RichTextUploadingField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    description_en = RichTextUploadingField("Описание (англ.)", blank=True, null=True)
    image = models.ImageField(default= "default_seminar.jpg", upload_to="seminar_images/", null=True, blank=True)

    position = models.IntegerField(default=0, null=True)

    reports = models.ManyToManyField(SeminarReport, verbose_name="Доклады", blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Научный семинар"
        verbose_name_plural = "Научные семинары"

    def __str__(self):
        return self.name
