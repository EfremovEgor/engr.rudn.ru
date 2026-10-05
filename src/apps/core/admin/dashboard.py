from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.views.generic import TemplateView
from modeltranslation.translator import translator
from unfold.views import UnfoldSiteViewMixin

from apps.core.i18n import translation_status_q


def environment_callback(request):
    if settings.DEBUG:
        return ["Разработка", "warning"]
    return None


def _changelist_url(model, query=""):
    try:
        url = reverse(f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist")
    except NoReverseMatch:
        return None
    return f"{url}?{query}" if query else url


def translation_overview(request):
    """Статистика перевода на английский по всем переводимым моделям."""
    rows = []
    for model in translator.get_registered_models(abstract=False):
        opts = model._meta
        if not request.user.has_perm(f"{opts.app_label}.view_{opts.model_name}"):
            continue
        conditions = translation_status_q(model, "en")
        if not conditions:
            continue
        qs = model._base_manager.all()
        total = qs.count()
        missing = qs.filter(conditions["missing"]).count()
        partial = qs.filter(conditions["partial"]).count()
        done = total - missing - partial
        rows.append(
            {
                "app": opts.app_config.verbose_name,
                "name": opts.verbose_name_plural,
                "total": total,
                "done": done,
                "partial": partial,
                "missing": missing,
                "percent": round(done * 100 / total) if total else 100,
                "url": _changelist_url(model),
                "missing_url": _changelist_url(model, "translation_en=missing"),
                "partial_url": _changelist_url(model, "translation_en=partial"),
            }
        )
    rows.sort(key=lambda r: (r["percent"], r["app"], str(r["name"])))
    return rows


def dashboard_callback(request, context):
    from apps.education.models import Program
    from apps.media_library.models import MediaFile
    from apps.news.models import NewsItem
    from apps.seminars.models import SeminarReport

    translations = translation_overview(request)
    total = sum(r["total"] for r in translations)
    done = sum(r["done"] for r in translations)
    today = timezone.localdate()

    def add_url(label):
        app_label, model_name = label.split(".")
        if not request.user.has_perm(f"{app_label}.add_{model_name}"):
            return None
        return reverse(f"admin:{app_label}_{model_name}_add")

    context.update(
        {
            "stats": [
                {"title": "Новости", "value": NewsItem.objects.count(), "icon": "newspaper", "url": _changelist_url(NewsItem)},
                {"title": "Программы", "value": Program.objects.count(), "icon": "menu_book", "url": _changelist_url(Program)},
                {
                    "title": "Ближайшие доклады",
                    "value": SeminarReport.objects.filter(date_start__gte=today).count(),
                    "icon": "co_present",
                    "url": _changelist_url(SeminarReport, "upcoming=1"),
                },
                {"title": "Файлы в медиатеке", "value": MediaFile.objects.count(), "icon": "perm_media", "url": _changelist_url(MediaFile)},
            ],
            "quick_actions": [
                action
                for action in [
                    {"title": "Новость", "icon": "newspaper", "url": add_url("news.newsitem")},
                    {"title": "Доклад семинара", "icon": "co_present", "url": add_url("seminars.seminarreport")},
                    {"title": "Страница", "icon": "article", "url": add_url("pages.page")},
                    {"title": "Документ", "icon": "description", "url": add_url("documents.document")},
                    {
                        "title": "Загрузить файлы",
                        "icon": "upload",
                        "url": reverse("admin:media_library_mediafile_upload")
                        if request.user.has_perm("media_library.add_mediafile")
                        else None,
                    },
                ]
                if action["url"]
            ],
            "translation_rows": [r for r in translations if r["missing"] or r["partial"]][:8],
            "translation_percent": round(done * 100 / total) if total else 100,
            "recent_news": NewsItem.objects.order_by("-creation_date")[:5],
            "recent_actions": LogEntry.objects.select_related("user", "content_type").order_by("-action_time")[:8],
        }
    )
    return context


class TranslationsOverviewView(UnfoldSiteViewMixin, TemplateView):
    title = "Переводы контента"
    permission_required = ()
    template_name = "admin/translations_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = translation_overview(self.request)
        total = sum(r["total"] for r in rows)
        done = sum(r["done"] for r in rows)
        context.update(
            {
                "rows": rows,
                "total": total,
                "done": done,
                "percent": round(done * 100 / total) if total else 100,
                "rosetta_url": reverse("rosetta-file-list", kwargs={"po_filter": "project"}),
            }
        )
        return context
