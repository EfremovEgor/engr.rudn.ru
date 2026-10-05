from django.contrib import admin
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin, BaseStackedInline, file_url, thumbnail

from .models import DepartmentStaff, EmployeeProfile, StudentCommitteeProfile


class DepartmentCardInline(BaseStackedInline):
    model = DepartmentStaff
    verbose_name = "Карточка для страниц кафедр"
    verbose_name_plural = "Карточка для страниц кафедр"
    fields = ("position", "department_responsibilities", "department_office")
    max_num = 1
    show_change_link = False


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(BaseAdmin):
    list_display = ("photo", "full_name", "positions", "contacts")
    list_display_links = ("photo", "full_name")
    search_fields = ("full_name_ru", "full_name_en", "emails", "office_ru")
    fieldsets = ((None, {"fields": ("image", "emails", "phone_numbers", "staff_support")}),)
    inlines = [DepartmentCardInline]

    @display(description="")
    def photo(self, obj):
        return thumbnail(file_url(obj.image), 40, rounded=True)

    @display(description="Должности")
    def positions(self, obj):
        return "; ".join(obj.job_title_ru or [])[:120] or "—"

    @display(description="Контакты")
    def contacts(self, obj):
        return ", ".join(obj.emails or []) or "—"


@admin.register(DepartmentStaff)
class DepartmentStaffAdmin(BaseAdmin):
    list_display = ("related_profile", "position", "responsibilities")
    search_fields = ("related_profile__full_name_ru", "related_profile__full_name_en")
    autocomplete_fields = ("related_profile",)
    list_select_related = ("related_profile",)
    fieldsets = ((None, {"fields": ("related_profile", "position")}),)

    @display(description="Должности на кафедре")
    def responsibilities(self, obj):
        return "; ".join(obj.department_responsibilities_ru or []) or "—"


@admin.register(StudentCommitteeProfile)
class StudentCommitteeProfileAdmin(BaseAdmin):
    list_display = ("photo", "full_name", "email")
    list_display_links = ("photo", "full_name")
    search_fields = ("full_name_ru", "full_name_en", "email")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = ((None, {"fields": ("image", "email", "phone_number", "position")}),)

    @display(description="")
    def photo(self, obj):
        return thumbnail(file_url(obj.image), 40, rounded=True)
