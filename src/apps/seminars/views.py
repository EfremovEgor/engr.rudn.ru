from itertools import chain
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from requests import get
from .models import Seminar, SeminarReport
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import gettext as _
from datetime import date


def seminars(request):
    seminars = Seminar.objects.order_by("position").all()

    return render(
        request,
        "seminars/seminars.html",
        {"title": _("Научные семинары"), "seminars": seminars},
    )


def seminar_detail(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    
    all_reports = seminar.reports.order_by("-date_start").all()
    today = date.today()
    
    past_reports = [r for r in all_reports if r.date_start and r.date_start < today]
    upcoming_reports = [r for r in all_reports if not r.date_start or r.date_start >= today]

    return render(
        request,
        "seminars/seminar_item.html",
        {
            "title": seminar.name,
            "seminar": seminar,
            "reports": all_reports,
            "past_reports": past_reports,
            "upcoming_reports": upcoming_reports,
        },
    )


def seminar_report_detail(request, seminar_id, report_uuid):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    report = get_object_or_404(seminar.reports.all(), uuid=report_uuid)

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
