from django.urls import path

from . import views

app_name = "education"

urlpatterns = [
    path("applicants/study_directions", views.study_directions, name="study_directions"),
    path("applicants/study_directions/<int:pk>", views.program_detail, name="program_detail"),
    path("applicants/study_directions/<str:level>", views.levels_of_study, name="level"),
    path(
        "applicants/additional_education/translator_module",
        views.translator_module,
        name="translator_module",
    ),
    path(
        "applicants/additional_education/additional_professional_education",
        views.additional_programs,
        name="additional_programs",
    ),
    path(
        "applicants/additional_education/additional_professional_education/<int:pk>",
        views.additional_program_detail,
        name="additional_program_detail",
    ),
]
