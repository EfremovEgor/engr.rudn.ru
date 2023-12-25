from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.news, name="news"),
    path("academy", views.academy, name="academy"),
    path("academy/administration", views.administration, name="administration"),
    path("academy/history", views.history, name="history"),
    path("science/directions", views.science_directions, name="science_directions"),
    path("science/journals", views.science_journals, name="science_journals"),
    path(
        "science/scientific_student_clubs",
        views.scientific_student_clubs,
        name="scientific_student_clubs",
    ),
    path("science/seminars", views.science_seminars, name="science_seminars"),
    path("directions/<int:id>", views.directions, name="directions"),
]
