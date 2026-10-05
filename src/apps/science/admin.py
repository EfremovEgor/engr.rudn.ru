from django.contrib import admin
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin, PublishableAdmin, file_url, thumbnail

from .models import DissertationCommittee, Equipment, Partner, ScientificCenter, ScientificSpecialty


@admin.register(ScientificCenter)
class ScientificCenterAdmin(PublishableAdmin):
    list_display = ("name", "head", "department", "slug", "page_source", "published")
    list_filter = ("is_published", "department")
    search_fields = ("name_ru", "name_en", "slug")
    autocomplete_fields = ("head", "department")
    list_select_related = ("head", "department")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = (
        (None, {"fields": ("slug", ("head", "department"), "emails", "is_published", "position")}),
        ("Старая страница", {"fields": ("legacy_template",), "classes": ["collapse"]}),
    )

    @display(description="Страница", label={"Из админки": "success", "Старый шаблон": "warning", "Нет": "danger"})
    def page_source(self, obj):
        if obj.content_ru:
            return "Из админки"
        return "Старый шаблон" if obj.legacy_template else "Нет"


@admin.register(Equipment)
class EquipmentAdmin(BaseAdmin):
    list_display = ("preview", "name", "prefix")
    list_display_links = ("preview", "name")
    search_fields = ("name_ru", "name_en", "prefix")
    fieldsets = ((None, {"fields": ("prefix", "image")}),)

    @display(description="")
    def preview(self, obj):
        return thumbnail(file_url(obj.image), 48)


@admin.register(Partner)
class PartnerAdmin(BaseAdmin):
    list_display = ("preview", "name", "prefix", "link")
    list_display_links = ("preview", "name")
    search_fields = ("name_ru", "name_en", "prefix")
    fieldsets = ((None, {"fields": ("prefix", "link", "image")}),)

    @display(description="")
    def preview(self, obj):
        return thumbnail(file_url(obj.image), 48)


@admin.register(ScientificSpecialty)
class ScientificSpecialtyAdmin(BaseAdmin):
    list_display = ("cipher", "name")
    search_fields = ("cipher", "name_ru", "name_en")
    fieldsets = ((None, {"fields": ("cipher",)}),)


@admin.register(DissertationCommittee)
class DissertationCommitteeAdmin(BaseAdmin):
    list_display = ("cipher", "chairman", "email")
    search_fields = ("cipher", "chairman_ru", "chairman_en")
    autocomplete_fields = ("scientific_specialties",)
    fieldsets = ((None, {"fields": ("cipher", "scientific_specialties", ("phone", "email"))}),)
