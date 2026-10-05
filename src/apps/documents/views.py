from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .models import Document


def _documents(category):
    return Document.objects.published().filter(category=category).order_by("position", "name_ru")


def reference(request):
    return render(
        request,
        "documents/reference.html",
        {
            "title": _("Справочная информация"),
            "cis": _documents(Document.Category.APPLICANTS_CIS),
            "foreign": _documents(Document.Category.APPLICANTS_FOREIGN),
        },
    )


def open_days(request):
    return render(
        request,
        "documents/open_days.html",
        {
            "title": _("Дни открытых дверей"),
            "presentations": _documents(Document.Category.OPEN_DAYS_PRESENTATION),
            "photos": _documents(Document.Category.OPEN_DAYS_PHOTO),
        },
    )


def student_applications(request):
    return render(
        request,
        "documents/applications.html",
        {"title": _("Образцы заявлений"), "applications": _documents(Document.Category.STUDENT_APPLICATION)},
    )
