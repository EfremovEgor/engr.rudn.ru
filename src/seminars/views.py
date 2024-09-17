from itertools import chain
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from requests import get
from .models import Seminar, SeminarReport
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models.fields.related import ManyToManyField


def seminars(request):
    seminars = Seminar.objects.all()

    return render(
        request,
        "seminars/seminars.html",
        {"title": "Научные семинары и симпозиумы", "seminars": seminars},
    )


def get_seminar(request, id):
    seminar = get_object_or_404(Seminar, id=id)

    return render(
        request,
        "seminars/seminar_item.html",
        {"title": seminar.name, "seminar": seminar},
    )


def get_seminar_report(request, seminar_id, id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    report = get_object_or_404(SeminarReport, id=id)

    return render(
        request,
        "seminars/seminar_report.html",
        {"title": report.name, "seminar": seminar, "report": report},
    )


def get_reports(request, id):
    seminar = get_object_or_404(Seminar, id=id)
    first_seminar = seminar.reports.order_by("date_start").first()
    year_start = first_seminar.date_start.year
    month_start = first_seminar.date_start.month
    last_seminar = seminar.reports.order_by("-date_start").first()
    year_end = last_seminar.date_start.year
    month_end = last_seminar.date_start.month
    reports = []
    for report in seminar.reports.order_by("date_start", "week").all():
        to_append = model_to_dict(report)
        to_append["speaker"] = model_to_dict(report.speaker, exclude=["image"])
        reports.append(to_append)
    return JsonResponse(
        {
            "reports": reports,
            "dates": {
                "year_start": year_start,
                "month_start": month_start,
                "year_end": year_end,
                "month_end": month_end,
            },
        },
    )
