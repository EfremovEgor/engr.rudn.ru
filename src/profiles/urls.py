from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path("profile/<int:id>", views.profiles, name="profiles"),
]
