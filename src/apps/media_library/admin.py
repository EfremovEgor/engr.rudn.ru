from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from unfold.decorators import action, display

from apps.core.admin.base import BaseAdmin, thumbnail

from .models import MediaFile, MediaFolder
from .services import find_usages, human_size, index_existing_files

KIND_ICONS = {
    MediaFile.Kind.VIDEO: "movie",
    MediaFile.Kind.AUDIO: "music_note",
    MediaFile.Kind.DOCUMENT: "description",
    MediaFile.Kind.ARCHIVE: "folder_zip",
    MediaFile.Kind.OTHER: "draft",
}


@admin.register(MediaFolder)
class MediaFolderAdmin(BaseAdmin):
    list_display = ("__str__", "files_count")
    search_fields = ("name",)
    autocomplete_fields = ("parent",)

    @display(description="Файлов")
    def files_count(self, obj):
        return obj.files.count()


@admin.register(MediaFile)
class MediaFileAdmin(BaseAdmin):
    list_display = ("preview", "title_column", "kind", "size_display", "dimensions", "folder", "created_at", "copy_link")
    list_display_links = ("preview", "title_column")
    list_filter = ("kind", "folder", "created_at")
    search_fields = ("title_ru", "title_en", "alt_ru", "file")
    autocomplete_fields = ("folder",)
    date_hierarchy = "created_at"
    readonly_fields = ("large_preview", "file_link", "meta", "usages", "uploaded_by", "created_at")
    fieldsets = (
        (None, {"fields": ("large_preview", "file", "file_link", "folder")}),
        ("Сведения", {"fields": ("meta", "uploaded_by", "created_at"), "classes": ["collapse"]}),
        ("Где используется", {"fields": ("usages",)}),
    )
    actions_list = ["upload_files", "index_files"]
    list_per_page = 60

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "upload/",
                self.admin_site.admin_view(self.upload_view),
                name="media_library_mediafile_upload",
            ),
        ]
        return custom + urls

    def upload_view(self, request):
        if not self.has_add_permission(request):
            return redirect("admin:media_library_mediafile_changelist")
        context = {
            **self.admin_site.each_context(request),
            "title": "Загрузка файлов",
            "opts": self.model._meta,
            "folders": MediaFolder.objects.all(),
            "upload_url": reverse("media_library:upload"),
            "changelist_url": reverse("admin:media_library_mediafile_changelist"),
        }
        return TemplateResponse(request, "admin/media_library/upload.html", context)

    @action(description="Загрузить файлы", icon="upload", url_path="upload-files", permissions=["add"])
    def upload_files(self, request):
        return redirect("admin:media_library_mediafile_upload")

    @action(description="Найти файлы на диске", icon="travel_explore", url_path="index-files", permissions=["add"])
    def index_files(self, request):
        created = index_existing_files()
        messages.success(request, f"Добавлено в медиатеку файлов, загруженных ранее: {created}")
        return redirect("admin:media_library_mediafile_changelist")

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def _delete_file_if_unused(self, obj):
        if obj.file and not find_usages(obj, limit=1):
            obj.file.delete(save=False)

    def delete_model(self, request, obj):
        self._delete_file_if_unused(obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self._delete_file_if_unused(obj)
        super().delete_queryset(request, queryset)

    @display(description="")
    def preview(self, obj):
        if obj.is_image:
            return thumbnail(obj.url, 56)
        return format_html(
            '<span class="material-symbols-outlined" style="font-size:36px;color:var(--color-base-400)">{}</span>',
            KIND_ICONS.get(obj.kind, "draft"),
        )

    @display(description="Название", ordering="title_ru")
    def title_column(self, obj):
        return format_html("{}<br><span class='academy-muted'>{}</span>", obj, obj.filename)

    @display(description="Размер", ordering="size")
    def size_display(self, obj):
        return human_size(obj.size)

    @display(description="Габариты")
    def dimensions(self, obj):
        return f"{obj.width}×{obj.height}" if obj.width else "—"

    @display(description="Ссылка")
    def copy_link(self, obj):
        return format_html(
            '<button type="button" class="media-copy" data-copy="{}" title="Скопировать ссылку">'
            '<span class="material-symbols-outlined">content_copy</span></button>',
            obj.url,
        )

    @display(description="Предпросмотр")
    def large_preview(self, obj):
        if not obj.pk:
            return "—"
        if obj.is_image:
            return format_html('<img src="{}" style="max-width:420px;max-height:320px;border-radius:8px">', obj.url)
        if obj.kind == MediaFile.Kind.VIDEO:
            return format_html('<video src="{}" controls style="max-width:420px;border-radius:8px"></video>', obj.url)
        return self.preview(obj)

    @display(description="Ссылка на файл")
    def file_link(self, obj):
        if not obj.pk:
            return "—"
        return format_html(
            '<a href="{0}" target="_blank">{0}</a> '
            '<button type="button" class="media-copy" data-copy="{0}" title="Скопировать">'
            '<span class="material-symbols-outlined">content_copy</span></button>',
            obj.url,
        )

    @display(description="Параметры")
    def meta(self, obj):
        parts = [obj.get_kind_display(), human_size(obj.size), obj.mime_type]
        if obj.width:
            parts.append(f"{obj.width}×{obj.height}px")
        return " · ".join(p for p in parts if p)

    @display(description="Используется")
    def usages(self, obj):
        if not obj.pk:
            return "—"
        found = find_usages(obj)
        if not found:
            return "Файл нигде не используется — его можно удалить."
        return format_html(
            "<ul>{}</ul>",
            format_html_join(
                "",
                '<li>{}: <a href="{}">{}</a></li>',
                ((u["model"], u["admin_url"] or "#", u["object"]) for u in found),
            ),
        )
