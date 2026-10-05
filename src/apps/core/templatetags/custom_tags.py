"""Фильтры и теги сайта. Подключены как builtins (см. settings.TEMPLATES)."""

from decimal import Decimal

from django import template
from django.conf import settings
from django.utils.translation import get_language, gettext as _

from apps.core.i18n import LANGUAGE_LABELS, current_language

register = template.Library()

_LANG_LOCATIVE_RU = {"ru": "русском", "en": "английском"}
_LANG_NAME_EN = {"ru": "Russian", "en": "English"}


@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return None
    return dictionary.get(key)


@register.filter
def replace_quotes(phrase):
    return "» /\t«".join(part.strip() for part in (phrase or "").split("/"))


@register.filter
def temp_replace_head_department(phrase: str) -> str:
    return (phrase or "").replace(_("кафедры"), _("кафедрой"))


@register.filter
def get_server_uri(_value=None):
    return settings.SITE_URL.rstrip("/")


@register.filter
def truncate_url(url: str):
    if not url:
        return ""
    return url[:-1] if url.endswith("/") else url


@register.filter
def lang_code_to_label(code: str) -> str:
    """'ru' -> «Русский» / «Russian» в зависимости от языка интерфейса."""
    if not code:
        return ""
    labels = LANGUAGE_LABELS.get(code)
    if not labels:
        return code
    return labels[current_language()]


@register.filter
def langs_phrase(codes) -> str:
    """['ru', 'en'] -> «(на русском и английском языках)»."""
    if not codes:
        return ""
    codes = list(codes)[:2]
    if current_language() == "ru":
        words = [_LANG_LOCATIVE_RU.get(c, c) for c in codes]
        if len(words) == 2:
            return f"(на {words[0]} и {words[1]} языках)"
        return f"(на {words[0]} языке)"
    words = [_LANG_NAME_EN.get(c, c) for c in codes]
    if len(words) == 2:
        return f"(in {words[0]} and {words[1]} languages)"
    return f"(in {words[0]} language)"


def format_duration(value) -> str:
    return ("%.1f" % float(value)).rstrip("0").rstrip(".")


def duration_suffix(duration) -> str:
    duration = Decimal(str(duration))
    if get_language() != "ru":
        return "year" if duration == 1 else "years"
    if duration % 1:
        return "года"
    num = int(duration) % 100
    if 11 <= num <= 14:
        return "лет"
    last = num % 10
    if last == 1:
        return "год"
    if last in (2, 3, 4):
        return "года"
    return "лет"


@register.filter
def duration_text(value) -> str:
    """Decimal('4.5') -> «4.5 года» / «4.5 years»."""
    if value in (None, ""):
        return ""
    return f"{format_duration(value)} {duration_suffix(value)}"


@register.filter
def format_phone_number(phone: str):
    """'+74959550952|1234' -> '+7 495 955-09-52 (12-34)'."""
    from phonenumber_field.phonenumber import PhoneNumber

    if not phone:
        return ""
    phone = str(phone)
    number, ext = phone.split("|", 1) if "|" in phone else (phone, "")
    ext = f" ({ext[0:2]}-{ext[2:]})" if ext else ""
    try:
        return PhoneNumber.from_string(number).as_international + ext
    except Exception:
        return number + ext


@register.filter
def tel_href(phone: str) -> str:
    """Номер для ссылки tel: без добавочного."""
    return str(phone or "").split("|", 1)[0]


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    """URL текущей страницы на другом языке."""
    from django.urls import translate_url as _translate_url

    request = context.get("request")
    if request is None:
        return "/"
    return _translate_url(request.get_full_path(), lang_code)
