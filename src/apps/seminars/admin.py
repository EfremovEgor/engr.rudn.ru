from django.contrib import admin
from django.utils import timezone
from unfold.decorators import display

from apps.core.admin.base import BaseAdmin, BaseTabularInline, PublishableAdmin, file_url, thumbnail

from .models import Seminar, SeminarReport, SeminarSpeaker


class UpcomingFilter(admin.SimpleListFilter):
    title = "Когда"
    parameter_name = "upcoming"

    def lookups(self, request, model_admin):
        return [("1", "Предстоящие"), ("0", "Прошедшие"), ("none", "Без даты")]

    def queryset(self, request, queryset):
        today = timezone.localdate()
        if self.value() == "1":
            return queryset.filter(date_start__gte=today)
        if self.value() == "0":
            return queryset.filter(date_start__lt=today)
        if self.value() == "none":
            return queryset.filter(date_start=None)
        return queryset


class SeminarReportInline(BaseTabularInline):
    model = SeminarReport
    fields = ("name", "date_start", "time_start", "speaker")
    autocomplete_fields = ("speaker",)
    ordering = ("-date_start",)
    show_change_link = True
    verbose_name_plural = "Доклады (аннотация, материалы и видео — по ссылке «Изменить»)"


@admin.register(Seminar)
class SeminarAdmin(PublishableAdmin):
    list_display = ("cover", "name", "chair", "reports_count", "published")
    list_display_links = ("cover", "name")
    list_filter = ("is_published", "department")
    search_fields = ("name_ru", "name_en")
    autocomplete_fields = ("chair", "organizer", "department")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = (
        (None, {"fields": ("image", ("chair", "organizer"), "department", "is_published", "position")}),
    )
    inlines = [SeminarReportInline]

    @display(description="")
    def cover(self, obj):
        return thumbnail(file_url(obj.image), 48)

    @display(description="Докладов")
    def reports_count(self, obj):
        return obj.reports.count()


@admin.register(SeminarReport)
class SeminarReportAdmin(BaseAdmin):
    list_display = ("name", "seminar", "date_start", "time_start", "speaker")
    list_filter = (UpcomingFilter, "seminar", ("seminar", admin.EmptyFieldListFilter))
    search_fields = ("name_ru", "name_en", "speaker__last_name_ru", "speaker__last_name_en")
    autocomplete_fields = ("seminar", "speaker")
    list_select_related = ("seminar", "speaker")
    date_hierarchy = "date_start"
    fieldsets = (
        (None, {"fields": ("seminar", "speaker", ("date_start", "week"), ("time_start", "time_end"))}),
        ("Трансляция и запись", {"fields": ("online_meeting_url", "video_recording", "video", "presentation_file")}),
    )


@admin.register(SeminarSpeaker)
class SeminarSpeakerAdmin(BaseAdmin):
    list_display = ("photo", "__str__", "academic_degree", "reports_count")
    list_display_links = ("photo", "__str__")
    search_fields = ("last_name_ru", "last_name_en", "first_name_ru", "first_name_en")
    fieldsets = ((None, {"fields": ("image",)}),)

    @display(description="")
    def photo(self, obj):
        return thumbnail(file_url(obj.image), 40, rounded=True)

    @display(description="Докладов")
    def reports_count(self, obj):
        return obj.reports.count()
