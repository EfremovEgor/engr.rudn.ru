from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.NewsView.as_view(), name="news"),
    path("news/<int:id>", views.NewsItemView.as_view(), name="news_item"),
    path("academy", views.academy, name="academy"),
    path("academy/administration", views.administration, name="administration"),
    path(
        "applicants/reference", views.applicants_reference, name="applicants_reference"
    ),
    path("applicants/open_days", views.open_days, name="applicants_open_days"),
    path(
        "applicants/study_directions",
        views.study_directions,
        name="applicants_study_directions",
    ),
    path("applicants/study_directions/<int:id>", views.directions),
    path("applicants/study_directions/<str:level>", views.levels_of_study),
    path("academy/history", views.history, name="history"),
    path("science/directions", views.science_directions, name="science_directions"),
    path("science/journals", views.science_journals, name="science_journals"),
    path(
        "science/scientific_student_clubs",
        views.scientific_student_clubs,
        name="scientific_student_clubs",
    ),
    path("science/seminars", views.science_seminars, name="science_seminars"),
    path("graduates/contacts", views.graduates_contacts, name="graduates_contacts"),
    path(
        "graduates/digital_library",
        views.graduates_digital_library,
        name="graduates_digital_library",
    ),
    path(
        "graduates/topics_of_dissertation_research",
        views.graduates_topics_of_dissertation_research,
        name="graduates_topics_of_dissertation_research",
    ),
    path(
        "students/appplications",
        views.students_applications,
        name="students_applications",
    ),
    path("students/schedule", views.students_schedule, name="students_schedule"),
    path(
        "students/student_committee",
        views.students_student_committee,
        name="students_student_committee",
    ),
]
