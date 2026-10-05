from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "pages"


def static(route, name):
    return path(route, views.static_page, {"page": name}, name=name)


urlpatterns = [
    path("", views.index, name="index"),
    path("academy", RedirectView.as_view(pattern_name="academy:administration"), name="academy"),
    static("academy/history", "history"),
    static("academy/contacts", "contacts"),
    static("applicants/committee", "committee"),
    static("applicants/additional_education", "additional_education"),
    static("science/directions", "science_directions"),
    static("science/journals", "science_journals"),
    static("science/scientific_student_society", "scientific_student_society"),
    static("science/events", "science_events"),
    static("science/cits", "science_cits"),
    static("science/scitechforum", "science_scitechforum"),
    static("science/digital_library", "digital_library"),
    static("graduates/contacts", "graduates_contacts"),
    static("graduates/topics_of_dissertation_research", "graduates_topics_of_dissertation_research"),
    static("students/schedule", "students_schedule"),
]
