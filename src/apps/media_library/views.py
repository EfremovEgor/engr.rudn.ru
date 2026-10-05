from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import MediaFile, MediaFolder
from .services import EDITOR_FOLDER, get_folder, human_size, store_upload


def _serialize(media: MediaFile) -> dict:
    return {
        "id": media.pk,
        "title": str(media),
        "alt": media.alt or "",
        "url": media.url,
        "kind": media.kind,
        "extension": media.extension,
        "size": human_size(media.size),
        "is_image": media.is_image,
    }


def _forbidden():
    return JsonResponse({"error": {"message": "Недостаточно прав для загрузки файлов."}}, status=403)


@staff_member_required
@require_POST
def editor_upload(request):
    """Загрузка из CKEditor 5: файл сразу попадает в медиатеку."""
    if not request.user.has_perm("media_library.add_mediafile"):
        return _forbidden()
    uploaded = request.FILES.get("upload")
    if uploaded is None:
        return JsonResponse({"error": {"message": "Файл не передан."}}, status=400)
    try:
        media = store_upload(uploaded, request.user, folder=get_folder(EDITOR_FOLDER))
    except ValidationError as exc:
        return JsonResponse({"error": {"message": " ".join(exc.messages)}}, status=400)
    return JsonResponse({"url": media.url, **_serialize(media)})


@staff_member_required
@require_POST
def upload(request):
    """Загрузка со страницы «Загрузить файлы» (по одному файлу на запрос)."""
    if not request.user.has_perm("media_library.add_mediafile"):
        return _forbidden()
    uploaded = request.FILES.get("file")
    if uploaded is None:
        return JsonResponse({"error": {"message": "Файл не передан."}}, status=400)
    folder = MediaFolder.objects.filter(pk=request.POST.get("folder") or None).first()
    try:
        media = store_upload(uploaded, request.user, folder=folder)
    except ValidationError as exc:
        return JsonResponse({"error": {"message": " ".join(exc.messages)}}, status=400)
    return JsonResponse(_serialize(media))


@staff_member_required
@require_GET
def picker(request):
    """Список файлов для окна «Вставить из медиатеки»."""
    if not request.user.has_perm("media_library.view_mediafile"):
        return _forbidden()
    qs = MediaFile.objects.all()
    if query := request.GET.get("q", "").strip():
        qs = qs.filter(Q(title_ru__icontains=query) | Q(title_en__icontains=query) | Q(file__icontains=query))
    if kind := request.GET.get("kind"):
        qs = qs.filter(kind=kind)
    page = Paginator(qs.order_by("-created_at"), 48).get_page(request.GET.get("page"))
    return JsonResponse(
        {
            "items": [_serialize(m) for m in page.object_list],
            "page": page.number,
            "pages": page.paginator.num_pages,
            "total": page.paginator.count,
        }
    )
