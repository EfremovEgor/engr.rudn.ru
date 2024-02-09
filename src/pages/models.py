from email.policy import default
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

LANGUAGES = [
    ("Русский", "Русский"),
    ("Английский", "Английский"),
    ("Русский и английский", "Русский и английский"),
]

DEPARTMENT_JOB_TITLES = [
    ("Директор департамента", "Директор департамента"),
    ("Заведующий кафедры", "Заведующий кафедры"),
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
        verbose_name="Количество бюджетных мест", null=True, blank=True
    )
    paid_places = models.PositiveIntegerField(
        verbose_name="Количество платных мест", null=True, blank=True
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
    job_title = ArrayField(
        models.CharField(verbose_name="Должность/Звание", max_length=255),
        verbose_name="Должности/Звания",
        size=20,
        blank=True,
        null=True,
    )
    sub_header = models.CharField(
        verbose_name="Подзаголовок", max_length=255, blank=True, null=True
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


class DepartmentInfo(models.Model):
    name = models.TextField(verbose_name="Название департамента")
    position = models.IntegerField(verbose_name="Позиция")
    job_title = models.CharField(
        verbose_name="Должность руководителя",
        choices=DEPARTMENT_JOB_TITLES,
        default="Директор департамента",
        max_length=255,
    )
    info = models.TextField(verbose_name="Информация о департаменте")
    head = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Руководитель",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.position}. {self.name}"

    class Meta:
        verbose_name = "Департамен"
        verbose_name_plural = "Департаменты"
        ordering = ["position"]


class Profile(models.Model):
    def get_languages():
        return ["Русский"]

    name = models.TextField(verbose_name="Название")
    cipher = models.CharField(verbose_name="Шифр", max_length=255)

    study_level = models.CharField(
        verbose_name="Уровень обучения", max_length=255, choices=STUDY_LEVELS
    )
    faculty_field = models.ForeignKey(
        DepartmentInfo,
        verbose_name="Департамент/Кафедра",
        on_delete=models.SET_NULL,
        related_name="department_info",
        blank=True,
        null=True,
    )
    study_duration = models.IntegerField(
        verbose_name="Длительность обучения", default=4
    )
    language_fields = ArrayField(
        models.CharField(
            verbose_name="Язык обучения",
            max_length=255,
            choices=LANGUAGES,
        ),
        default=get_languages,
    )
    full_time_details = models.ForeignKey(
        ProfileDetails,
        verbose_name="Информация по очной форме обучения",
        on_delete=models.SET_NULL,
        related_name="full_time_details",
        blank=True,
        null=True,
    )
    part_time_details = models.ForeignKey(
        ProfileDetails,
        verbose_name="Информация по очно-заочной форме обучения",
        on_delete=models.SET_NULL,
        related_name="part_time_details",
        blank=True,
        null=True,
    )
    extramural_details = models.ForeignKey(
        ProfileDetails,
        verbose_name="Информация по заочной форме обучения",
        on_delete=models.SET_NULL,
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
        ordering = ["position", "employee__full_name"]


class ScientificSpecialty(models.Model):
    cipher = models.CharField(verbose_name="Шифр", max_length=255)
    name = models.TextField(verbose_name="Название")

    def __str__(self) -> str:
        return f"{self.cipher}  {self.name}"

    class Meta:
        verbose_name = "Научное направлние"
        verbose_name_plural = "Научные направления"
        ordering = ["cipher", "name"]


class DissertationCommittee(models.Model):
    cipher = models.CharField(verbose_name="Шифр совета", max_length=255)
    organization = models.CharField(
        verbose_name="Организация",
        max_length=255,
        default="Российский университет дружбы народов",
    )
    faculty = models.CharField(
        verbose_name="Факультет", max_length=255, default="Инженерная академия"
    )
    address = models.CharField(
        verbose_name="Адрес",
        max_length=255,
        default="115419, Москва, улица Орджоникидзе, 3",
    )
    scientific_specialties = models.ManyToManyField(
        ScientificSpecialty, verbose_name="Научные специальности", blank=True
    )
    chairman = models.CharField(verbose_name="Председатель", max_length=255)
    deputy = models.CharField(verbose_name="Заместитель председателя", max_length=255)
    secretary = models.CharField(verbose_name="Секретарь", max_length=255)
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(
        verbose_name="Электронная почта", max_length=255, blank=True, null=True
    )
    composition = ArrayField(
        models.CharField(verbose_name="Участник диссовета", max_length=255),
        verbose_name="Cостав диссовета",
        size=20,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.cipher}"

    class Meta:
        verbose_name = "Диссертационный совет"
        verbose_name_plural = "Диссертационные советы"
        ordering = ["cipher"]
