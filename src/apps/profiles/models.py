from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from django_jsonform.models.fields import JSONField
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.fields import RichTextField


class EmployeeProfile(models.Model):
    full_name = models.TextField("ФИО")
    image = models.ImageField(
        "Фотография",
        upload_to="profiles",
        default="profile_default.png",
        blank=True,
    )
    job_title = ArrayField(
        models.CharField("Должность/Звание", max_length=255),
        verbose_name="Должности/Звания",
        size=20,
        blank=True,
        null=True,
    )
    office = models.TextField("Кабинет", blank=True, null=True)
    emails = ArrayField(
        models.EmailField("Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    phone_numbers = ArrayField(
        models.TextField("Номер телефона"),
        verbose_name="Номера телефонов",
        size=10,
        blank=True,
        null=True,
        help_text="Добавочный номер указывается через «|»: +74959550952|1234",
    )
    working_hours = models.CharField("Рабочее время", max_length=255, blank=True, null=True)
    STAFF_SUPPORT_SCHEMA = {
        "type": "dict",
        "keys": {
            "full_name": {"type": "string", "title": "ФИО"},
            "email": {"type": "string", "title": "Почта"},
            "office": {"type": "string", "title": "Кабинет"},
            "working_hours": {"type": "string", "title": "Рабочее время"},
            "phone_number": {"type": "string", "title": "Номер телефона"},
        },
    }
    staff_support = JSONField("Помощник", schema=STAFF_SUPPORT_SCHEMA, blank=True, null=True)
    content = RichTextField("Информация", blank=True, null=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name or ""

    def get_absolute_url(self):
        return reverse("profiles:profile", args=[self.pk])


class DepartmentStaff(models.Model):
    """Карточка сотрудника для страниц кафедр (должности и кабинет на кафедре)."""

    related_profile = models.OneToOneField(
        EmployeeProfile,
        verbose_name="Сотрудник",
        on_delete=models.CASCADE,
        related_name="department_card",
    )
    position = models.IntegerField("Позиция", default=1)
    department_responsibilities = ArrayField(
        models.CharField("Должность/Звание", max_length=255),
        verbose_name="Должности на кафедре",
        size=20,
        blank=True,
        null=True,
    )
    department_office = models.TextField(
        "Кабинет на кафедре",
        default="Москва, ул. Орджоникидзе, д. 3., каб. ",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Сотрудник кафедры"
        verbose_name_plural = "Сотрудники кафедр"
        ordering = ["related_profile__full_name"]

    def __str__(self):
        return self.related_profile.full_name


class StudentCommitteeProfile(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    image = models.ImageField(
        "Фотография",
        upload_to="student_committee_profiles",
        default="profile_default.png",
        blank=True,
    )
    job_title = ArrayField(
        models.CharField("Должность/Звание", max_length=255),
        verbose_name="Должности/Звания",
        size=20,
        blank=True,
        null=True,
    )
    position = models.IntegerField("Позиция", default=0)
    office = models.CharField("Кабинет", max_length=255)
    email = models.EmailField("Электронный адрес", max_length=255)
    phone_number = PhoneNumberField("Номер телефона", null=True, blank=True)

    class Meta:
        verbose_name = "Член студенческого комитета"
        verbose_name_plural = "Студенческий комитет"
        ordering = ["position"]

    def __str__(self):
        return self.full_name
