"""Утилиты для переводов контента (django-modeltranslation)."""

from functools import reduce
from operator import and_, or_

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.utils.translation import get_language

LANGUAGE_LABELS = {
    "ru": {"ru": "Русский", "en": "Russian"},
    "en": {"ru": "Английский", "en": "English"},
}
LANGUAGE_FLAGS = {"ru": "🇷🇺", "en": "🇬🇧"}
DEFAULT_LANGUAGE = settings.MODELTRANSLATION_DEFAULT_LANGUAGE
EXTRA_LANGUAGES = [code for code in settings.MODELTRANSLATION_LANGUAGES if code != DEFAULT_LANGUAGE]


def current_language() -> str:
    lang = (get_language() or DEFAULT_LANGUAGE)[:2]
    return lang if lang in settings.MODELTRANSLATION_LANGUAGES else DEFAULT_LANGUAGE


def localized(name: str, lang: str) -> str:
    return f"{name}_{lang.replace('-', '_')}"


def translation_options(model):
    from modeltranslation.translator import NotRegistered, translator

    try:
        return translator.get_options_for_model(model)
    except NotRegistered:
        return None


def translated_field_names(model) -> list[str]:
    """Имена исходных переводимых полей модели в порядке объявления."""
    opts = translation_options(model)
    if opts is None:
        return []
    declared = [f.name for f in model._meta.get_fields()]
    return sorted(opts.all_fields.keys(), key=lambda n: declared.index(n) if n in declared else 999)


def _empty_q(field_name: str, field) -> Q:
    q = Q(**{f"{field_name}__isnull": True})
    if isinstance(field, ArrayField):
        return q | Q(**{f"{field_name}__len": 0})
    if isinstance(field, (models.CharField, models.TextField, models.FileField)):
        return q | Q(**{field_name: ""})
    return q


def translation_status_q(model, lang: str) -> dict[str, Q]:
    """Q-условия статуса перевода на язык `lang`.

    Поле считается требующим перевода, если в языке по умолчанию оно заполнено.
    complete — все такие поля переведены; missing — не переведено ни одно;
    partial — всё остальное.
    """
    pairs = []
    for name in translated_field_names(model):
        src = localized(name, DEFAULT_LANGUAGE)
        dst = localized(name, lang)
        src_field = model._meta.get_field(src)
        dst_field = model._meta.get_field(dst)
        pairs.append((~_empty_q(src, src_field), _empty_q(dst, dst_field)))
    if not pairs:
        return {}
    # Есть что переводить, но перевод пустой
    untranslated = [has_src & dst_empty for has_src, dst_empty in pairs]
    # Есть что переводить и перевод заполнен
    translated = [has_src & ~dst_empty for has_src, dst_empty in pairs]
    complete = ~reduce(or_, untranslated)
    missing = reduce(or_, [has_src for has_src, _ in pairs]) & ~reduce(or_, translated)
    return {"complete": complete, "missing": missing, "partial": ~complete & ~missing}


def instance_translation_status(obj, lang: str) -> str | None:
    """'complete' | 'partial' | 'missing' | None (нечего переводить)."""

    def filled(value):
        if value is None:
            return False
        if hasattr(value, "name") and not isinstance(value, str):  # FieldFile
            return bool(value.name)
        return value not in ("", [], ())

    total = done = 0
    for name in translated_field_names(type(obj)):
        if filled(getattr(obj, localized(name, DEFAULT_LANGUAGE), None)):
            total += 1
            if filled(getattr(obj, localized(name, lang), None)):
                done += 1
    if total == 0:
        return None
    if done == total:
        return "complete"
    return "missing" if done == 0 else "partial"


def any_of(*qs: Q) -> Q:
    return reduce(or_, qs)


def all_of(*qs: Q) -> Q:
    return reduce(and_, qs)
