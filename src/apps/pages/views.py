from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from apps.news.views import visible_news

from .models import IndexContact, MainSlider, Page


def index(request):
    return render(
        request,
        "pages/index.html",
        {
            "title": _("Инженерная академия РУДН"),
            "contacts": IndexContact.objects.all(),
            "news": visible_news()[:10],
            "slider_images": MainSlider.objects.published(),
        },
    )


#: Информационные страницы, свёрстанные в шаблонах (тексты переводятся в «Строках интерфейса»).
STATIC_PAGES = {
    "history": ("pages/academy/history.html", _("История")),
    "contacts": ("pages/academy/contacts.html", _("Контакты")),
    "committee": ("pages/applicants/committee.html", _("Приемная комиссия")),
    "additional_education": ("pages/applicants/additional_education.html", _("Дополнительное образование")),
    "science_directions": ("pages/science/directions.html", _("Научные направления")),
    "science_journals": ("pages/science/journals.html", _("Научные журналы")),
    "scientific_student_society": (
        "pages/science/scientific_student_society.html",
        _("Научное студенческое общество"),
    ),
    "science_events": ("pages/science/events.html", _("Научные мероприятия")),
    "science_cits": ("pages/science/cits.html", _("Конференция по информационным и техническим системам")),
    "science_scitechforum": (
        "pages/science/scitechforum.html",
        _(
            "Международный научно-технический форум по механике космического полета "
            "и космическим конструкциям и материалам"
        ),
    ),
    "digital_library": ("pages/science/digital_library.html", _("Электронная библиотека")),
    "graduates_contacts": ("pages/graduates/contacts.html", _("Контакты")),
    "graduates_topics_of_dissertation_research": (
        "pages/graduates/topics_of_dissertation_research.html",
        _("Тематики диссертационных исследований"),
    ),
    "students_schedule": ("pages/students/schedule.html", _("Расписание")),
}


def static_page(request, page):
    template, title = STATIC_PAGES[page]
    return render(request, template, {"title": title})


def page_detail(request, path):
    """Страница, созданная в админке (модель Page)."""
    path = (path or "").strip("/")
    if not path:
        raise Http404
    page = get_object_or_404(Page.objects.published(), path=path)
    return render(request, "pages/page.html", {"title": page.title, "page": page})
