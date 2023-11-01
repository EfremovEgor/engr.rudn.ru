from django.db import models
from django.contrib.postgres.fields import ArrayField as postgres_array_field
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField
from django_jsonform.models.fields import JSONField, ArrayField

STUDY_LEVELS = [
    ("Бакалавриат", "Бакалавриат"),
    ("Специалитет", "Специалитет"),
    ("Магистратура", "Магистратура"),
    ("Аспирантура", "Аспирантура"),
]


class IndexContact(models.Model):
    position = models.IntegerField(verbose_name="Позиция")
    heading = models.CharField(verbose_name="Заголовок", max_length=255)
    sub_heading = models.CharField(verbose_name="Подзаголовок", max_length=255)
    image = models.ImageField(
        verbose_name="Фотография", upload_to="index_contacts", blank=False, null=True
    )
    phone_numbers = postgres_array_field(
        PhoneNumberField(verbose_name="Номер телефона"),
        verbose_name="Номера телефонов",
        size=10,
        blank=True,
        null=True,
    )
    location = models.CharField(
        verbose_name="Локация", max_length=255, blank=True, null=True
    )
    emails = ArrayField(
        models.EmailField(verbose_name="Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    working_hours = models.CharField(
        verbose_name="Рабочее время", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.heading

    class Meta:
        verbose_name = "Контакт на главной странице"
        verbose_name_plural = "Контакты на главной странице"


class ProfileDetails(models.Model):
    name = models.TextField(verbose_name="Название")
    budget_places = models.PositiveIntegerField(
        verbose_name="Количество бюджетных мест"
    )
    price_first_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(1 год)", null=True, blank=True
    )
    price_second_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(2 год)", null=True, blank=True
    )
    price_third_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(3 год)", null=True, blank=True
    )
    price_fourth_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(4 год)", null=True, blank=True
    )
    price_fifth_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(5 год)", null=True, blank=True
    )
    price_sixth_year = models.PositiveIntegerField(
        verbose_name="Стоимость обучения по контракту(6 год)", null=True, blank=True
    )
    SCORES_SCHEMA = {
        "type": "dict",  # or 'object'
        "keys": {  # or 'properties'
            "Обязательные предметы": {
                "type": "list",
                "items": {
                    "title": "Информация о предмете",
                    "type": "dict",
                    "keys": {
                        "subject": {"type": "string", "title": "Предмет"},
                        "score": {"type": "integer", "title": "Балл"},
                    },
                },
            },
            "Дополнительные предметы (один на выбор)": {
                "type": "list",
                "items": {
                    "title": "Информация о предмете",
                    "type": "dict",
                    "keys": {
                        "subject": {"type": "string", "title": "Предмет"},
                        "score": {"type": "integer", "title": "Балл"},
                    },
                },
            },
        },
    }
    minimal_passing_scores = JSONField(
        verbose_name="Минимальные проходные баллы:",
        schema=SCORES_SCHEMA,
    )
    program_manager = models.CharField(
        verbose_name="Руководитель программы", max_length=255
    )
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(
        verbose_name="Электронная почта", max_length=255, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Информация по профилю направления подготовки"
        verbose_name_plural = "Информация по профилям направления подготовки"


class Profile(models.Model):
    name = models.TextField(verbose_name="Название")
    cipher = models.CharField(verbose_name="Шифр", max_length=255)

    study_level = models.CharField(
        verbose_name="Уровень обучения", max_length=255, choices=STUDY_LEVELS
    )
    full_time_details = models.OneToOneField(
        ProfileDetails,
        verbose_name="Информация по очной форме обучения",
        on_delete=models.CASCADE,
        related_name="full_time_details",
        blank=True,
        null=True,
    )
    part_time_details = models.OneToOneField(
        ProfileDetails,
        verbose_name="Информация по очно-заочной форме обучения",
        on_delete=models.CASCADE,
        related_name="part_time_details",
        blank=True,
        null=True,
    )
    extramural_details = models.OneToOneField(
        ProfileDetails,
        verbose_name="Информация по заочной форме обучения",
        on_delete=models.CASCADE,
        related_name="extramural_details",
        blank=True,
        null=True,
    )
    content = RichTextUploadingField(verbose_name="Информация")

    def __str__(self) -> str:
        return f"{self.study_level} - {self.name}"

    class Meta:
        verbose_name = "Профиль направления"
        verbose_name_plural = "Профили направления"


class StudyDirection(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    study_level = models.CharField(
        verbose_name="Уровень обучения", max_length=255, choices=STUDY_LEVELS
    )
    cipher = models.CharField(verbose_name="Шифр", max_length=255)
    profiles = models.ManyToManyField(Profile, verbose_name="Профили", blank=True)

    def __str__(self) -> str:
        return f"{self.study_level} - [{self.cipher}] {self.name}"

    class Meta:
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"


class AdministrationProfiles(models.Model):
    position = models.PositiveIntegerField(verbose_name="Позиция")
    employee = models.ForeignKey(
        "profiles.EmployeeProfile", verbose_name="Сотрудник", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.position} - {self.employee.full_name}"

    class Meta:
        verbose_name = "Профиль дирекции"
        verbose_name_plural = "Профили дирекции"
