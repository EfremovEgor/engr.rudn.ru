from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from apps.core.i18n import current_language, localized

from .models import NewsItem, Tag


def visible_news():
    news = NewsItem.objects.published().prefetch_related("tags").order_by("-creation_date")
    if current_language() == "ru":
        # Новости, опубликованные только на английском, в русской версии не показываем
        news = news.exclude(Q(title_ru=None) | Q(title_ru=""))
    return news


def news_list(request):
    lang = current_language()
    title_query = request.GET.get("title", "").strip()
    tag_query = request.GET.get("tag", "").strip()

    news = visible_news()
    if title_query:
        news = news.filter(**{f"{localized('title', lang)}__icontains": title_query})
    if tag_query:
        news = news.filter(**{f"tags__{localized('name', lang)}": tag_query}).distinct()

    tag_field = localized("name", lang)
    tags = (
        Tag.objects.filter(news_items__is_published=True)
        .exclude(Q(**{tag_field: None}) | Q(**{tag_field: ""}))
        .distinct()
        .order_by(tag_field)
    )
    return render(
        request,
        "news/news_list.html",
        {
            "title": _("Новости"),
            "news": news,
            "tags": tags,
            "searched_title": title_query,
            "searched_tags": tag_query,
        },
    )


def news_detail(request, pk):
    item = get_object_or_404(NewsItem.objects.published().prefetch_related("tags"), pk=pk)
    tag_field = localized("name", current_language())
    tags = [tag for tag in item.tags.all() if getattr(tag, tag_field)]
    return render(
        request,
        "news/news_detail.html",
        {"title": item.title or _("Без названия"), "content": item, "tags": tags},
    )
