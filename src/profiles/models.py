from django.db import models
from django.contrib.postgres.fields import ArrayField as postgres_array_field
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField
from django_jsonform.models.fields import JSONField, ArrayField


class EmployeeProfile(models.Model):
    full_name = models.TextField(verbose_name="ФИО")
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="profiles",
        default="profile_default.png",
        blank=True,
    )
    job_title = ArrayField(
        models.CharField(verbose_name="Должность/Звание", max_length=255),
        verbose_name="Должности/Звания",
        size=20,
        blank=True,
        null=True,
    )
    office = models.TextField(verbose_name="Кабинет")
    emails = ArrayField(
        models.EmailField(verbose_name="Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    phone_numbers = postgres_array_field(
        PhoneNumberField(verbose_name="Номер телефона"),
        verbose_name="Номера телефонов",
        size=10,
        blank=True,
        null=True,
    )
    working_hours = models.CharField(
        verbose_name="Рабочее время", max_length=255, blank=True, null=True
    )
    STAFF_SUPPORT_SCHEMA = {
        "type": "dict",
        "keys": {
            "full_name": {
                "type": "string",
                "title": "ФИО",
            },
            "email": {
                "type": "string",
                "title": "Почта",
            },
            "office": {
                "type": "string",
                "title": "Кабинет",
            },
            "working_hours": {
                "type": "string",
                "title": "Рабочее время",
            },
            "phone_number": {
                "type": "string",
                "title": "Номер телефона",
            },
        },
    }
    staff_support = JSONField(
        verbose_name="Помощник", schema=STAFF_SUPPORT_SCHEMA, blank=True, null=True
    )
    content = RichTextUploadingField(
        verbose_name="Информация",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.full_name
