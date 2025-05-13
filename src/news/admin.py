from django.contrib import admin
from .models import Tag, NewsItem

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Just a basic admin for tags
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "title_en", "creation_date")
    search_fields = ("title_ru", "title_en", "content_ru", "content_en")
    # remove or rename content references, e.g.:
    # fields = ("title_ru", "content") -> fields = ("title_ru", "content_ru") 