from django.urls import path

from . import views

app_name = "seminars"

urlpatterns = [
    path("science/seminars/", views.seminars, name="seminars_list"),
    path("science/seminars/<int:seminar_id>/", views.seminar_detail, name="seminar_detail"),
    path(
        "science/seminars/<int:seminar_id>/reports/<uuid:report_uuid>/",
        views.report_detail,
        name="report_detail",
    ),
    path("science/seminars/<int:pk>/get_reports/", views.get_reports, name="seminar_reports_json"),
]
