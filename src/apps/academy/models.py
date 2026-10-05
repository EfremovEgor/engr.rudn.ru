from django.db import models
from django.urls import reverse


class Department(models.Model):
    class JobTitle(models.TextChoices):
        DIRECTOR = "director", "Директор департамента"
        HEAD = "head", "Заведующий кафедрой"

    name = models.TextField("Название")
    slug = models.SlugField(
        "Адрес страницы",
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Часть адреса: /academy/departments/<адрес>. Пусто — у кафедры нет отдельной страницы.",
    )
    position = models.IntegerField("Позиция", default=0)
    abbreviation = models.CharField("Аббревиатура", max_length=255, blank=True, null=True)
    job_title = models.CharField(
        "Должность руководителя",
        choices=JobTitle.choices,
        default=JobTitle.DIRECTOR,
        max_length=32,
    )
    info = models.TextField("Информация о кафедре")
    head = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name="Руководитель",
        related_name="headed_departments",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    contact_employee = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name="Контактное лицо",
        related_name="contact_for_departments",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    staff = models.ManyToManyField(
        "profiles.DepartmentStaff",
        verbose_name="Сотрудники",
        related_name="departments",
        blank=True,
    )

    class Meta:
        verbose_name = "Кафедра / департамент"
        verbose_name_plural = "Кафедры и департаменты"
        ordering = ["position"]

    def __str__(self) -> str:
        return self.name or ""

    def get_absolute_url(self):
        if self.slug:
            return reverse("academy:department_detail", args=[self.slug])
        return None


class AdministrationMember(models.Model):
    position = models.PositiveIntegerField("Позиция", default=0)
    employee = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Сотрудник",
        on_delete=models.CASCADE,
        related_name="administration_memberships",
    )

    class Meta:
        verbose_name = "Член дирекции"
        verbose_name_plural = "Дирекция"
        ordering = ["position", "employee__full_name"]

    def __str__(self) -> str:
        return self.employee.full_name
