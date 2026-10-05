from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import Document


@register(Document)
class DocumentTranslation(BaseTranslationOptions):
    fields = ("name", "file")
