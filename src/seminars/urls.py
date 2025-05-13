from django.urls import path
from . import views

app_name = "seminars"
urlpatterns = [
    path(
        "science/seminars/",
        views.seminars,
        name="seminars_list" 
    ),

    path(
        "science/seminars/<int:id>/",
        views.get_seminar,
        name="seminar_detail"
    ),

    path(
        "science/seminars/<int:seminar_id>/reports/<int:id>/",
        views.get_seminar_report,
        name="seminar_report_detail"
    ),

    path(
        "science/seminars/<int:id>/get_reports/",
        views.get_reports,
        name="seminar_reports_json"
    ),
]
