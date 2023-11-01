from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.news, name="news"),
    path("academy", views.academy, name="academy"),
    path("academy/administration", views.administration, name="administration"),
    path("academy/history", views.history, name="history"),
    path("directions/<int:id>", views.directions, name="directions"),
]
