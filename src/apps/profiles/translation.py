from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import DepartmentStaff, EmployeeProfile, StudentCommitteeProfile


@register(EmployeeProfile)
class EmployeeProfileTranslation(BaseTranslationOptions):
    fields = ("full_name", "job_title", "office", "working_hours", "content")


@register(DepartmentStaff)
class DepartmentStaffTranslation(BaseTranslationOptions):
    fields = ("department_responsibilities", "department_office")


@register(StudentCommitteeProfile)
class StudentCommitteeProfileTranslation(BaseTranslationOptions):
    fields = ("full_name", "job_title", "office")
