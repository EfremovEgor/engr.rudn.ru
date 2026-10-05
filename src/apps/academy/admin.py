from django.contrib import admin
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin

from .models import AdministrationMember, Department


@admin.register(Department)
class DepartmentAdmin(BaseAdmin):
    list_display = ("name", "abbreviation", "slug", "head")
    search_fields = ("name_ru", "name_en", "abbreviation")
    autocomplete_fields = ("head", "contact_employee", "staff")
    list_select_related = ("head__related_profile",)
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = (
        (None, {"fields": (("abbreviation", "slug"), "job_title", ("head", "contact_employee"), "staff", "position")}),
    )


@admin.register(AdministrationMember)
class AdministrationMemberAdmin(BaseAdmin):
    list_display = ("employee", "job_titles")
    autocomplete_fields = ("employee",)
    list_select_related = ("employee",)
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)

    @display(description="Должности")
    def job_titles(self, obj):
        return "; ".join(obj.employee.job_title_ru or []) or "—"
