from django.urls import path
from . import views

app_name = "seminars"
urlpatterns = [
    path("science/seminars", views.seminars, name="sciene_seminars"),
    path("science/seminars/<int:id>", views.get_seminar, name="get_seminar"),
    path(
        "science/seminars/<int:seminar_id>/reports/<int:id>",
        views.get_seminar_report,
        name="get_seminar_report",
    ),
    path(
        "science/seminar/<int:id>/get_reports",
        views.get_reports,
        name="get_reports_by_seminar_id",
    ),
]
