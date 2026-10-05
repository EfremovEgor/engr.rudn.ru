"""Базовые классы админки: единый вид всех разделов и удобный перевод.

* Переводимые поля автоматически выносятся во вкладки «Русский» / «English».
* Под каждым английским полем показывается русский оригинал (переводчику не нужно
  переключать вкладки).
* В списках есть колонка и фильтр «Перевод EN».
"""

from copy import deepcopy

from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.forms.widgets import ArrayWidget
from unfold.decorators import display

from apps.core.fields import RichTextField
from apps.core.i18n import (
    DEFAULT_LANGUAGE,
    EXTRA_LANGUAGES,
    LANGUAGE_FLAGS,
    instance_translation_status,
    localized,
    translated_field_names,
    translation_status_q,
)

LANGUAGE_TAB_TITLES = {"ru": "Русский", "en": "English"}
STATUS_LABELS = {
    "complete": "Переведено",
    "partial": "Частично",
    "missing": "Нет перевода",
}

FORMFIELD_OVERRIDES = {
    RichTextField: {"widget": CKEditor5Widget},
    ArrayField: {"widget": ArrayWidget},
}


def thumbnail(url: str | None, size: int = 48, rounded: bool = False):
    if not url:
        return "—"
    radius = "9999px" if rounded else "6px"
    return format_html(
        '<img src="{}" alt="" loading="lazy" style="width:{}px;height:{}px;object-fit:cover;border-radius:{}">',
        url,
        size,
        size,
        radius,
    )


def file_url(field_file) -> str | None:
    try:
        return field_file.url if field_file else None
    except ValueError:
        return None


class TranslationStatusFilter(admin.SimpleListFilter):
    title = "Перевод на английский"
    parameter_name = "translation_en"
    language = "en"

    def lookups(self, request, model_admin):
        return list(STATUS_LABELS.items())

    def queryset(self, request, queryset):
        conditions = translation_status_q(queryset.model, self.language)
        if self.value() in conditions:
            return queryset.filter(conditions[self.value()])
        return queryset


class TranslationAdminMixin:
    """Раскладывает переводимые поля по языковым вкладкам."""

    #: Порядок переводимых полей во вкладках (по умолчанию — порядок регистрации).
    translated_fields: tuple[str, ...] | None = None

    def get_translated_fields(self) -> list[str]:
        if self.translated_fields is not None:
            return list(self.translated_fields)
        from apps.core.i18n import translation_options

        opts = translation_options(self.model)
        return list(opts.fields) if opts else []

    def _all_localized(self) -> set[str]:
        names = set()
        for name in translated_field_names(self.model):
            names.add(name)
            for lang in (DEFAULT_LANGUAGE, *EXTRA_LANGUAGES):
                names.add(localized(name, lang))
        return names

    def get_fieldsets(self, request, obj=None):
        translated = self.get_translated_fields()
        hidden = self._all_localized()
        if self.fieldsets:
            fieldsets = []
            for title, options in deepcopy(self.fieldsets):
                fields = []
                for field in options.get("fields", ()):
                    if isinstance(field, (list, tuple)):
                        row = tuple(f for f in field if f not in hidden)
                        if row:
                            fields.append(row)
                    elif field not in hidden:
                        fields.append(field)
                if fields:
                    options["fields"] = fields
                    fieldsets.append((title, options))
        else:
            form_fields = super().get_fieldsets(request, obj)[0][1]["fields"]
            main = [f for f in form_fields if f not in hidden]
            fieldsets = [(None, {"fields": main})] if main else []
        if translated:
            for lang in (DEFAULT_LANGUAGE, *EXTRA_LANGUAGES):
                fieldsets.append(
                    (
                        f"{LANGUAGE_FLAGS.get(lang, '')} {LANGUAGE_TAB_TITLES.get(lang, lang)}".strip(),
                        {"fields": [localized(name, lang) for name in translated], "classes": ["tab"]},
                    )
                )
        return fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change=change, **kwargs)
        translated = self.get_translated_fields()
        if not translated:
            return form

        class TranslationHintsForm(form):
            def __init__(self, *args, **kw):
                super().__init__(*args, **kw)
                for name in translated:
                    source = getattr(self.instance, localized(name, DEFAULT_LANGUAGE), None)
                    if not source:
                        continue
                    if isinstance(source, (list, tuple)):
                        source = "; ".join(map(str, source))
                    elif hasattr(source, "name") and not isinstance(source, str):
                        source = source.name
                    preview = Truncator(strip_tags(str(source)).replace("&nbsp;", " ")).chars(300)
                    for lang in EXTRA_LANGUAGES:
                        field = self.fields.get(localized(name, lang))
                        if field is not None:
                            hint = f"RU: {preview}"
                            field.help_text = f"{field.help_text} · {hint}" if field.help_text else hint

        TranslationHintsForm.__name__ = form.__name__
        return TranslationHintsForm

    def get_list_filter(self, request):
        filters = list(super().get_list_filter(request))
        if self.get_translated_fields() and TranslationStatusFilter not in filters:
            filters.append(TranslationStatusFilter)
        return filters

    @display(
        description="EN",
        label={
            STATUS_LABELS["complete"]: "success",
            STATUS_LABELS["partial"]: "warning",
            STATUS_LABELS["missing"]: "danger",
        },
    )
    def translation_status(self, obj):
        status = instance_translation_status(obj, "en")
        return STATUS_LABELS.get(status, "—")

    def get_list_display(self, request):
        columns = list(super().get_list_display(request))
        if self.get_translated_fields() and "translation_status" not in columns:
            columns.append("translation_status")
        return columns


class BaseAdmin(TranslationAdminMixin, ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True
    list_per_page = 50
    formfield_overrides = FORMFIELD_OVERRIDES

    @display(description="Опубликовано", boolean=True, ordering="is_published")
    def published(self, obj):
        return obj.is_published

    @admin.action(description="Опубликовать выбранные")
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано: {updated}")

    @admin.action(description="Скрыть выбранные с сайта")
    def make_hidden(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"Скрыто: {updated}")


class PublishableAdmin(BaseAdmin):
    actions = ["make_published", "make_hidden"]


class TranslatableInlineMixin:
    """В строчных формах (inline) переводимые поля идут парами RU/EN."""

    formfield_overrides = FORMFIELD_OVERRIDES

    def get_fields(self, request, obj=None):
        translated = translated_field_names(self.model)
        langs = (DEFAULT_LANGUAGE, *EXTRA_LANGUAGES)
        localized_names = {localized(name, lang) for name in translated for lang in langs}
        result = []
        for field in super().get_fields(request, obj):
            if field in translated:
                candidates = [localized(field, lang) for lang in langs]
            elif field in localized_names:
                continue
            else:
                candidates = [field]
            result.extend(c for c in candidates if c not in result)
        return result


class BaseTabularInline(TranslatableInlineMixin, TabularInline):
    extra = 0
    show_change_link = True


class BaseStackedInline(TranslatableInlineMixin, StackedInline):
    extra = 0
    show_change_link = True
