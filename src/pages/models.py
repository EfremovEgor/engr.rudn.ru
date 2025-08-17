from django.db import models
from django.contrib.postgres.fields import ArrayField as postgres_array_field
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField
from django_jsonform.models.fields import JSONField, ArrayField
from django.utils.translation import gettext_lazy as _


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
    ("Заведующий кафедрой", "Заведующий кафедрой"),
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
    name_en  = models.TextField(_("Название (EN)"), blank=True, null=True)
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
    study_duration = models.DecimalField(
        "Продолжительность обучения",
        max_digits=4,
        decimal_places=1,
        null=True, blank=True
    )
    admission_url = models.URLField(
        "Ссылка на admission.rudn", max_length=255, null=True, blank=True
    )
    note = RichTextUploadingField(
        "Примечание", blank=True, default='', null=False
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
                        "score": {"type": "string", "title": "Балл"},
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
                        "score": {"type": "string", "title": "Балл"},
                    },
                },
            },
        },
    }
    minimal_passing_scores_budget = JSONField(
        verbose_name="Минимальные проходные баллы на бюджет:",
        schema=SCORES_SCHEMA,
        blank=True,
        null=True,
    )
    minimal_passing_scores_contract = JSONField(
        verbose_name="Минимальные проходные баллы на контракт:",
        schema=SCORES_SCHEMA,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Информация по профилю направления подготовки"
        verbose_name_plural = "Информация по профилям направления подготовки"


class DepartmentInfo(models.Model):
    class JobTitle(models.TextChoices):
        DIRECTOR = "director", _("Директор департамента")
        HEAD = "head", _("Заведующий кафедрой")

    name = models.TextField(_("Название департамента"))
    name_en = models.TextField(
        _("Название департамента (англ.)"),
        blank=True,
        null=True,
    )

    position = models.IntegerField(_("Позиция"))
    abbreviation = models.CharField(
        _("Аббревиатура"),
        max_length=255,
        blank=True,
        null=True,
    )

    job_title = models.CharField(
        _("Должность руководителя"),
        choices=JobTitle.choices,
        default=JobTitle.DIRECTOR,
        max_length=32,
    )

    info = models.TextField(_("Информация о департаменте"))
    info_en = models.TextField(
        _("Информация о департаменте (англ.)"),
        blank=True,
        null=True,
    )

    head = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name=_("Руководитель"),
        related_name="head_of_department",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    contact_employee = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name=_("Контактное лицо"),
        related_name="contact_employee",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    staff = models.ManyToManyField(
        "profiles.DepartmentStaff",
        verbose_name=_("Сотрудники департамента"),
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.position}. {self.name}"

    class Meta:
        verbose_name = _("Департамент")
        verbose_name_plural = _("Департаменты")
        ordering = ["position"]


class Profile(models.Model):
    def get_languages():
        return ["Русский"]

    name = models.TextField(verbose_name="Название")
    name_en = models.TextField(_("Название (EN)"), blank=True, null=True)
    cipher = models.CharField(
        verbose_name="Шифр",
        max_length=255,
        blank=True,
        null=True,
    )

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
    content_en  = RichTextUploadingField(_("Информация (EN)"), blank=True, null=True)

    def __str__(self):
        return f"{self.study_level} – {self.name or self.name_en}"

    class Meta:
        verbose_name = "Профиль направления"
        verbose_name_plural = "Профили направления"

class AdditionalEducation(models.Model):
    contact_employee1 = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name=_("Контактное лицо 1"),
        related_name="contact_employee1",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    contact_employee2 = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name=_("Контактное лицо 2"),
        related_name="contact_employee2",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    
    class Meta:
        verbose_name = "Дополнительное образование"
        verbose_name_plural = "Дополнительное образование"

class AdditionalEducationItem(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название программы"
    )

    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Краткое описание"
    )

    department = models.ForeignKey(
        'DepartmentInfo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кафедра"
    )

    program_director = models.ForeignKey(
        "profiles.DepartmentStaff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_programs',
        verbose_name="Руководитель программы"
    )

    contact_person = models.ForeignKey(
        "profiles.DepartmentStaff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_for_programs',
        verbose_name="Контактное лицо"
    )

    volume = models.CharField(
        max_length=100,
        verbose_name="Объем",
        help_text="Например, '72 академических часа' или '3 зачетные единицы'"
    )
    
    study_mode = models.CharField(
        max_length=100,
        verbose_name="Форма обучения"
    )

    language = models.CharField(
        max_length=100,
        verbose_name="Язык обучения"
    )
    
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        help_text="Стоимость в рублях"
    )
    
    information = RichTextUploadingField(
        verbose_name="Дополнительная информация",
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Программа ДПО"
        verbose_name_plural = "Программы ДПО"

class StudyDirection(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    name_en = models.CharField(_("Название (EN)"), max_length=255, blank=True, null=True)


    study_level = models.CharField(
        verbose_name="Уровень обучения", max_length=255, choices=STUDY_LEVELS
    )
    cipher = models.CharField(verbose_name="Шифр", max_length=255)
    profiles = models.ManyToManyField(Profile, verbose_name="Профили", blank=True)

    def __str__(self):
        return f"{self.study_level} – [{self.cipher}] {self.name or self.name_en}"


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
    cipher = models.CharField(_("Шифр"), max_length=255)
    name = models.TextField(_("Название (RU)"))
    name_en = models.TextField(_("Название (EN)"), blank=True, null=True)

    def __str__(self):
        return f"{self.cipher}  {self.name or self.name_en}"

    class Meta:
        verbose_name = _("Научное направление")
        verbose_name_plural = _("Научные направления")
        ordering = ["cipher", "name"]


class DissertationCommittee(models.Model):
    cipher = models.CharField(_("Шифр совета"), max_length=255)

    organization = models.CharField(_("Организация (RU)"),
                                        max_length=255,
                                        default="Российский университет дружбы народов")
    organization_en = models.CharField(_("Организация (EN)"),
                                        max_length=255,
                                        blank=True, null=True)                        

    faculty = models.CharField(_("Факультет (RU)"),
                                        max_length=255,
                                        default="Инженерная академия")
    faculty_en = models.CharField(_("Факультет (EN)"),
                                        max_length=255,
                                        blank=True, null=True)                        

    address = models.CharField(_("Адрес (RU)"),
                                    max_length=255,
                                    default="115419, Москва, улица Орджоникидзе, 3")
    address_en = models.CharField(_("Адрес (EN)"),
                                    max_length=255,
                                    blank=True, null=True)                            

    scientific_specialties = models.ManyToManyField(
        ScientificSpecialty,
        verbose_name=_("Научные специальности"),
        blank=True
    )

    chairman = models.CharField(_("Председатель (RU)"), max_length=255)
    chairman_en = models.CharField(_("Председатель (EN)"),
                                    max_length=255,
                                    blank=True, null=True)                            

    deputy = models.CharField(_("Заместитель председателя (RU)"), max_length=255)
    deputy_en = models.CharField(_("Заместитель председателя (EN)"),
                                    max_length=255,
                                    blank=True, null=True)                            

    secretary = models.CharField(_("Секретарь (RU)"), max_length=255)
    secretary_en = models.CharField(_("Секретарь (EN)"),
                                    max_length=255,
                                    blank=True, null=True)                            

    phone = PhoneNumberField(_("Телефон"), blank=True, null=True)
    email = models.EmailField(_("Электронная почта"), max_length=255,
                              blank=True, null=True)

    composition = ArrayField(
        models.CharField(_("Участник диссовета (RU)"), max_length=255),
        verbose_name=_("Состав диссовета"),
        size=20,
        blank=True, null=True
    )
    composition_en = ArrayField(                                                      
        models.CharField(_("Участник диссовета (EN)"), max_length=255),
        verbose_name=_("Состав диссовета (EN)"),
        size=20,
        blank=True, null=True
    )

    def __str__(self):
        return self.cipher

    class Meta:
        verbose_name = _("Диссертационный совет")
        verbose_name_plural = _("Диссертационные советы")
        ordering = ["cipher"]


class EquipmentData(models.Model):
    name = models.TextField(verbose_name="Название")
    prefix = models.CharField(
        verbose_name="Префикс",
        help_text="Для удобства поиска в админке",
        max_length=255,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="equipment",
        blank=True,
        null=True,
    )
    purpose = models.TextField(verbose_name="Назначение")

    def __str__(self) -> str:
        return f"{self.prefix} {self.name}"

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["prefix", "name"]


class PartnerData(models.Model):
    name = models.TextField(verbose_name="Наименование организации")
    link = models.URLField(
        "Ссылка на сайт",
        max_length=255,
        blank=True,
        null=True,
    )
    prefix = models.CharField(
        verbose_name="Префикс",
        help_text="Для удобства поиска в админке",
        max_length=255,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Фотография",
        upload_to="equipment",
        blank=True,
        null=True,
    )
    collaboration_direction = models.TextField(verbose_name="Предмет сотрудничества")
    result = models.TextField(verbose_name="Результат сотрудничества")
    about = models.TextField(verbose_name="О партнёре")

    def __str__(self) -> str:
        return f"{self.prefix} {self.name}"

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ["prefix", "name"]


class ScientificCenters(models.Model):
    name = models.TextField(verbose_name="Название")
    name_en = models.TextField("Название (англ.)", blank=True, null=True)
    field_name = models.TextField(
        verbose_name="Сфера деятельности",
        blank=True,
        null=True,
    )
    field_name_en = models.TextField("Сфера деятельности (англ.)", blank=True, null=True)
    position = models.IntegerField(verbose_name="Позиция")
    display = models.BooleanField("Видимость", default=True)
    page_url = models.CharField(
        "Путь",
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )
    head = models.ForeignKey(
        "profiles.EmployeeProfile",
        verbose_name="Руководитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    faculty_field = models.ForeignKey(
        DepartmentInfo,
        verbose_name="Департамент/Кафедра",
        on_delete=models.SET_NULL,
        related_name="faculty_info_for_scientific_centers",
        blank=True,
        null=True,
    )
    # address = models.CharField(
    #     verbose_name="Адрес",
    #     max_length=255,
    #     default="115419, Москва, улица Орджоникидзе, 3",
    # )
    # phone = PhoneNumberField(verbose_name="Телефон", blank=True, null=True)
    email_fields = ArrayField(
        models.EmailField(verbose_name="Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    brief_description = models.TextField(
        verbose_name="Краткое описание",
        blank=True,
        null=True,
    )
    brief_description_en = models.TextField("Краткое описание (англ.)", blank=True, null=True)
    def __str__(self) -> str:
        return f"{self.position}. {self.name}"

    class Meta:
        verbose_name = "Научный центр"
        verbose_name_plural = "Научные центры"
        ordering = ["position", "name"]


class MainSlider(models.Model):
    name = models.TextField(verbose_name="Название")
    position = models.IntegerField(verbose_name="Позиция")
    url = models.URLField(
        "Ссылка",
        max_length=255,
        blank=True,
        null=True,
    )
    image_full = models.ImageField(
        verbose_name="Фотография полноразмерная",
        upload_to="main_slider_full",
        blank=True,
        null=True,
    )
    image_mobile = models.ImageField(
        verbose_name="Фотография мобильная",
        upload_to="main_slider_mobile",
        blank=True,
        null=True,
    )
    image_full_en = models.ImageField(
        verbose_name="Фотография полноразмерная (en)",
        upload_to="main_slider_full_en",
        blank=True,
        null=True,
    )
    image_mobile_en = models.ImageField(
        verbose_name="Фотография мобильная (en)",
        upload_to="main_slider_mobile_en",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.position}. {self.name}"

    class Meta:
        verbose_name = "Картинка главного слайдера"
        verbose_name_plural = "Картинки главного слайдера"
        ordering = ["position", "name"]
