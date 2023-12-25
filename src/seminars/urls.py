from django.urls import path
from . import views


urlpatterns = [
    path("seminars", views.seminars, name="seminars"),
]
