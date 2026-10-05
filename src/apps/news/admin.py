from django.contrib import admin, messages
from django.db.models import Count
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin, PublishableAdmin, file_url, thumbnail

from .models import NewsItem, Tag


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ("__str__", "name_ru", "name_en", "news_count")
    list_editable = ("name_ru", "name_en")
    search_fields = ("name_ru", "name_en")
    actions = ["merge_tags"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_news=Count("news_items"))

    @display(description="Новостей", ordering="_news")
    def news_count(self, obj):
        return obj._news

    @admin.action(description="Объединить выбранные тэги в один")
    def merge_tags(self, request, queryset):
        tags = list(queryset.order_by("pk"))
        if len(tags) < 2:
            self.message_user(request, "Выберите хотя бы два тэга.", messages.WARNING)
            return
        target, rest = tags[0], tags[1:]
        for tag in rest:
            target.name_ru = target.name_ru or tag.name_ru
            target.name_en = target.name_en or tag.name_en
            for news in tag.news_items.all():
                news.tags.add(target)
            tag.delete()
        target.save()
        self.message_user(request, f"Тэги объединены в «{target}».")


@admin.register(NewsItem)
class NewsItemAdmin(PublishableAdmin):
    list_display = ("cover", "title", "creation_date", "tag_list", "published")
    list_display_links = ("cover", "title")
    list_filter = ("is_published", "tags", "creation_date")
    search_fields = ("title_ru", "title_en", "content_ru", "content_en")
    date_hierarchy = "creation_date"
    autocomplete_fields = ("tags",)
    fieldsets = ((None, {"fields": ("preview_image", "tags", ("creation_date", "is_published"))}),)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @display(description="")
    def cover(self, obj):
        return thumbnail(file_url(obj.preview_image), 56)

    @display(description="Тэги")
    def tag_list(self, obj):
        return ", ".join(str(tag) for tag in obj.tags.all()) or "—"
