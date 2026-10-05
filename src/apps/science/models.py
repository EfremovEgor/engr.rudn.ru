from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.fields import RichTextField
from apps.core.models import PublishableModel


class ScientificCenter(PublishableModel):
    class LegacyTemplate(models.TextChoices):
        NEURAL = "neural_technologies.html", "Нейротехнологии"
        PHOTON = "photon.html", "Фотоника"
        RESTORATION = "restoration_architectural_heritage.html", "Реставрация архитектурного наследия"
        SUBSOIL = "subsoil_development.html", "Разработка недр"
        BUILDING = "technology_and_building.html", "Техника и технологии строительства"
        TRANSPORT = "operational_systems_and_complexes.html", "Транспортные системы и комплексы"
        MECHANICAL = "technologies_mechanical_engineering.html", "Машиностроение и приборостроение"
        TRANSFER = "transfer-center.html", "Центр трансфера технологий"

    name = models.TextField("Название")
    field_name = models.TextField("Сфера деятельности", blank=True, null=True)
    position = models.IntegerField("Позиция", default=0)
    slug = models.CharField(
        "Адрес страницы",
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        help_text="Часть адреса: /science/scientific_centers/<адрес>",
    )
    head = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Руководитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="headed_centers",
    )
    department = models.ForeignKey(
        "academy.Department",
        verbose_name="Кафедра / департамент",
        on_delete=models.SET_NULL,
        related_name="scientific_centers",
        blank=True,
        null=True,
    )
    emails = ArrayField(
        models.EmailField("Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    brief_description = models.TextField("Краткое описание", blank=True, null=True)
    content = RichTextField(
        "Подробное описание",
        blank=True,
        default="",
        help_text="Направления деятельности, ресурсы, проекты. Если пусто — используется старый шаблон страницы.",
    )
    legacy_template = models.CharField(
        "Старый шаблон страницы",
        max_length=100,
        choices=LegacyTemplate.choices,
        blank=True,
        default="",
        help_text="Свёрстанная вручную страница центра. Используется, пока не заполнено «Подробное описание».",
    )

    class Meta:
        verbose_name = "Научный центр"
        verbose_name_plural = "Научные центры"
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name or ""

    def get_absolute_url(self):
        if self.slug:
            return reverse("science:center_detail", args=[self.slug])
        return None


class Equipment(models.Model):
    name = models.TextField("Название")
    prefix = models.CharField(
        "Префикс", help_text="Для удобства поиска в админке", max_length=255, blank=True, null=True
    )
    image = models.ImageField("Фотография", upload_to="equipment", blank=True, null=True)
    purpose = models.TextField("Назначение")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["prefix", "name"]

    def __str__(self) -> str:
        return f"{self.prefix or ''} {self.name}".strip()


class Partner(models.Model):
    name = models.TextField("Наименование организации")
    link = models.URLField("Ссылка на сайт", max_length=255, blank=True, null=True)
    prefix = models.CharField(
        "Префикс", help_text="Для удобства поиска в админке", max_length=255, blank=True, null=True
    )
    image = models.ImageField("Логотип", upload_to="equipment", blank=True, null=True)
    collaboration_direction = models.TextField("Предмет сотрудничества")
    result = models.TextField("Результат сотрудничества")
    about = models.TextField("О партнёре")

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"
        ordering = ["prefix", "name"]

    def __str__(self) -> str:
        return f"{self.prefix or ''} {self.name}".strip()


class ScientificSpecialty(models.Model):
    cipher = models.CharField("Шифр", max_length=255)
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Научная специальность"
        verbose_name_plural = "Научные специальности"
        ordering = ["cipher", "name"]

    def __str__(self):
        return f"{self.cipher} {self.name}"


class DissertationCommittee(models.Model):
    cipher = models.CharField("Шифр совета", max_length=255)
    organization = models.CharField(
        "Организация", max_length=255, default="Российский университет дружбы народов"
    )
    faculty = models.CharField("Факультет", max_length=255, default="Инженерная академия")
    address = models.CharField("Адрес", max_length=255, default="115419, Москва, улица Орджоникидзе, 3")
    scientific_specialties = models.ManyToManyField(
        ScientificSpecialty, verbose_name="Научные специальности", blank=True, related_name="committees"
    )
    chairman = models.CharField("Председатель", max_length=255)
    deputy = models.CharField("Заместитель председателя", max_length=255)
    secretary = models.CharField("Секретарь", max_length=255)
    phone = PhoneNumberField("Телефон", blank=True, null=True)
    email = models.EmailField("Электронная почта", max_length=255, blank=True, null=True)
    composition = ArrayField(
        models.CharField("Участник диссовета", max_length=255),
        verbose_name="Состав диссовета",
        size=20,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Диссертационный совет"
        verbose_name_plural = "Диссертационные советы"
        ordering = ["cipher"]

    def __str__(self):
        return self.cipher

    def get_absolute_url(self):
        return reverse("science:dissertation_committee_detail", args=[self.pk])
