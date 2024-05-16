from django.urls import include, path, re_path
from . import views

app_name = "pages"
urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.NewsView.as_view(), name="news"),
    path("news/<int:id>", views.NewsItemView.as_view(), name="news_item"),
    path("academy", views.academy, name="academy"),
    path("academy/administration", views.administration, name="administration"),
    path(
        "applicants/reference", views.applicants_reference, name="applicants_reference"
    ),
    path("academy/departments", views.departments, name="departments"),
    path(
        "academy/departments/<str:name>", views.department_item, name="department_item"
    ),
    path("applicants/open_days", views.open_days, name="applicants_open_days"),
    path("applicants/committee", views.committee, name="committee"),
    path("academy/contacts", views.contacts, name="contacts"),
    path(
        "applicants/study_directions",
        views.study_directions,
        name="applicants_study_directions",
    ),
    path("applicants/study_directions/<int:id>", views.directions),
    path(
        "applicants/study_directions/<str:level>",
        views.levels_of_study,
        name="study_direction_level",
    ),
    path("academy/history", views.history, name="history"),
    path("science/directions", views.science_directions, name="science_directions"),
    path("science/journals", views.science_journals, name="science_journals"),
    path(
        "science/scientific_student_society",
        views.scientific_student_society,
        name="scientific_student_society",
    ),
    path("science/events", views.science_events, name="science_events"),
    # path("science/seminars", views.science_seminars, name="science_seminars"),
    path("science/cits", views.science_cits, name="science_cits"),
    path(
        "science/scitechforum", views.science_scitechforum, name="science_scitechforum"
    ),
    path(
        "science/digital_library",
        views.digital_library,
        name="digital_library",
    ),
    path("graduates/contacts", views.graduates_contacts, name="graduates_contacts"),
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
        "science/dissertation_committees",
        views.dissertation_committees,
        name="dissertation_committees",
    ),
    path(
        "science/dissertation_committees/<int:id>",
        views.dissertation_committee,
        name="dissertation_committee_item",
    ),
    path(
        "science/scientific_centers",
        views.scientific_centers,
        name="scientific_centers",
    ),
    path(
        "science/scientific_centers/<str:name>",
        views.scientific_center_item,
        name="scientific_center_item",
    ),
    path(
        "students/student_committee",
        views.students_student_committee,
        name="students_student_committee",
    ),
]
