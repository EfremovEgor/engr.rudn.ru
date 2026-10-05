from django.contrib import admin
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin, PublishableAdmin, file_url, thumbnail

from .models import IndexContact, MainSlider, Page


@admin.register(Page)
class PageAdmin(PublishableAdmin):
    list_display = ("title", "path", "published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title_ru", "title_en", "path", "content_ru")
    fieldsets = ((None, {"fields": ("path", "is_published")}),)
    readonly_fields = ("created_at", "updated_at")


@admin.register(MainSlider)
class MainSliderAdmin(PublishableAdmin):
    list_display = ("preview", "name", "url", "published")
    list_display_links = ("preview", "name")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = ((None, {"fields": ("url", "is_published", "position")}),)

    @display(description="")
    def preview(self, obj):
        return thumbnail(file_url(obj.image_full_ru), 64)


@admin.register(IndexContact)
class IndexContactAdmin(BaseAdmin):
    list_display = ("preview", "heading", "sub_heading")
    list_display_links = ("preview", "heading")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = ((None, {"fields": ("image", "phone_numbers", "emails", "position")}),)

    @display(description="")
    def preview(self, obj):
        return thumbnail(file_url(obj.image), 40, rounded=True)
