from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import NewsItem, Tag


@register(Tag)
class TagTranslation(BaseTranslationOptions):
    # Тэг может существовать только на одном языке
    fields = ("name",)
    required_languages = ()
    fallback_undefined = {"name": ""}
    fallback_languages = {"default": ()}


@register(NewsItem)
class NewsItemTranslation(BaseTranslationOptions):
    fields = ("title", "content")
    required_languages = ()
