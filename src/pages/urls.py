from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("news", views.news, name="news"),
    path("academy", views.academy, name="academy"),
    path("academy/administration", views.administration, name="administration"),
    path("profile/<int:id>", views.profile, name="profile"),
]
