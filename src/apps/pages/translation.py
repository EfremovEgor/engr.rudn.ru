from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import IndexContact, MainSlider, Page


@register(IndexContact)
class IndexContactTranslation(BaseTranslationOptions):
    fields = ("heading", "sub_heading", "location", "working_hours")


@register(MainSlider)
class MainSliderTranslation(BaseTranslationOptions):
    fields = ("name", "image_full", "image_mobile")


@register(Page)
class PageTranslation(BaseTranslationOptions):
    fields = ("title", "content", "seo_description")
