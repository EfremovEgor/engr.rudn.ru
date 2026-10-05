from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import MediaFile


@register(MediaFile)
class MediaFileTranslation(BaseTranslationOptions):
    fields = ("title", "alt")
