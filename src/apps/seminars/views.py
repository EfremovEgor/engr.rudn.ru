from datetime import date

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from .models import Seminar, SeminarReport


def seminars(request):
    return render(
        request,
        "seminars/seminars.html",
        {"title": _("Научные семинары"), "seminars": Seminar.objects.published().order_by("position")},
    )


def seminar_detail(request, seminar_id):
    seminar = get_object_or_404(
        Seminar.objects.published().select_related("chair", "organizer", "department"), pk=seminar_id
    )
    reports = list(seminar.reports.select_related("speaker").order_by("-date_start"))
    today = date.today()
    return render(
        request,
        "seminars/seminar_item.html",
        {
            "title": seminar.name,
            "seminar": seminar,
            "reports": reports,
            "past_reports": [r for r in reports if r.date_start and r.date_start < today],
            "upcoming_reports": sorted(
                (r for r in reports if not r.date_start or r.date_start >= today),
                key=lambda r: (r.date_start is None, r.date_start or today),
            ),
        },
    )


def report_detail(request, seminar_id, report_uuid):
    report = get_object_or_404(SeminarReport.objects.select_related("seminar", "speaker"), uuid=report_uuid)
    if report.seminar_id is None or not report.seminar.is_published:
        raise Http404
    if report.seminar_id != seminar_id:
        return redirect(report.get_absolute_url(), permanent=True)
    return render(
        request,
        "seminars/seminar_report.html",
        {"title": report.name, "seminar": report.seminar, "report": report},
    )


def get_reports(request, pk):
    seminar = get_object_or_404(Seminar.objects.published(), pk=pk)
    reports = list(seminar.reports.select_related("speaker").exclude(date_start=None).order_by("date_start", "week"))
    if not reports:
        return JsonResponse({"reports": [], "dates": None})
    first, last = reports[0].date_start, reports[-1].date_start
    payload = []
    for report in reports:
        speaker = report.speaker
        payload.append(
            {
                "id": report.pk,
                "uuid": str(report.uuid),
                "name": report.name,
                "date_start": report.date_start.isoformat(),
                "week": report.week,
                "time_start": report.time_start.isoformat() if report.time_start else None,
                "time_end": report.time_end.isoformat() if report.time_end else None,
                "speaker": {
                    "first_name": speaker.first_name,
                    "last_name": speaker.last_name,
                    "middle_name": speaker.middle_name,
                }
                if speaker
                else None,
            }
        )
    return JsonResponse(
        {
            "reports": payload,
            "dates": {
                "year_start": first.year,
                "month_start": first.month,
                "year_end": last.year,
                "month_end": last.month,
            },
        }
    )
