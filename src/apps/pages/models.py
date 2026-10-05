from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import get_language
from phonenumber_field.modelfields import PhoneNumberField

from apps.core.fields import RichTextField
from apps.core.models import PublishableModel


class IndexContact(models.Model):
    position = models.IntegerField("Позиция", default=0)
    heading = models.CharField("Заголовок", max_length=255)
    sub_heading = models.CharField("Подзаголовок", max_length=255)
    image = models.ImageField("Фотография", upload_to="index_contacts", blank=False, null=True)
    phone_numbers = ArrayField(
        PhoneNumberField("Номер телефона"),
        verbose_name="Номера телефонов",
        size=10,
        blank=True,
        null=True,
    )
    location = models.CharField("Адрес", max_length=255, blank=True, null=True)
    emails = ArrayField(
        models.EmailField("Электронный адрес", max_length=255),
        verbose_name="Электронные адреса",
        size=10,
        blank=True,
        null=True,
    )
    working_hours = models.CharField("Рабочее время", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Контакт на главной"
        verbose_name_plural = "Контакты на главной"
        ordering = ["position"]

    def __str__(self) -> str:
        return self.heading or ""


class MainSlider(PublishableModel):
    name = models.TextField("Название")
    position = models.IntegerField("Позиция", default=0)
    url = models.URLField("Ссылка", max_length=255, blank=True, null=True)
    image_full = models.ImageField(
        "Изображение для компьютера",
        upload_to="main_slider_full",
        blank=True,
        null=True,
        help_text="Широкий баннер для экранов от 960px.",
    )
    image_mobile = models.ImageField(
        "Изображение для телефона",
        upload_to="main_slider_mobile",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Слайд на главной"
        verbose_name_plural = "Слайдер на главной"
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name or ""


page_path_validator = RegexValidator(
    r"^[a-z0-9][a-z0-9_\-/]*[a-z0-9]$|^[a-z0-9]$",
    "Используйте латиницу в нижнем регистре, цифры, «-», «_» и «/» (без «/» в начале и конце).",
)


class Page(PublishableModel):
    """Произвольная контентная страница, создаваемая из админки.

    Открывается по адресу /<path> (и /en/<path> для английской версии), если такой адрес
    не занят страницами сайта.
    """

    path = models.CharField(
        "Адрес страницы",
        max_length=255,
        unique=True,
        validators=[page_path_validator],
        help_text="Например: science/new-lab → https://academy.rudn.ru/science/new-lab",
    )
    title = models.CharField("Заголовок", max_length=255)
    content = RichTextField("Содержимое", blank=True, default="")
    seo_description = models.CharField(
        "Описание для поисковиков", max_length=300, blank=True, default=""
    )
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Изменена", auto_now=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ["path"]

    def __str__(self):
        return self.title_ru or self.title or self.path

    def get_absolute_url(self):
        lang = get_language() or settings.LANGUAGE_CODE
        prefix = "" if lang == settings.LANGUAGE_CODE else f"/{lang}"
        return f"{prefix}/{self.path}"
