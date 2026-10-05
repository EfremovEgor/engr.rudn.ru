from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import Department


@register(Department)
class DepartmentTranslation(BaseTranslationOptions):
    fields = ("name", "info")
