from django.contrib import admin
from .models import Tag, NewsItem

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Just a basic admin for tags
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "title_en", "creation_date")
    search_fields = ("title", "title_en", "content", "content_en")
