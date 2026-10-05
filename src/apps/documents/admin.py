from django.contrib import admin
from django.utils.html import format_html
from unfold.decorators import display

from apps.core.admin.base import PublishableAdmin, file_url

from .models import Document


@admin.register(Document)
class DocumentAdmin(PublishableAdmin):
    list_display = ("name", "category", "file_link", "published")
    list_filter = ("category", "is_published")
    search_fields = ("name_ru", "name_en", "file_ru")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("category", "position")
    fieldsets = ((None, {"fields": ("category", "is_published", "position")}),)

    @display(description="Файл")
    def file_link(self, obj):
        url = file_url(obj.file_ru)
        if not url:
            return "—"
        return format_html('<a href="{}" target="_blank">{}</a>', url, (obj.extension or "файл").upper())
