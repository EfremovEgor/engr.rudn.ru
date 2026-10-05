from django.urls import path

from . import views

app_name = "academy"

urlpatterns = [
    path("academy/administration", views.administration, name="administration"),
    path("academy/departments", views.departments, name="departments"),
    path("academy/departments/<slug:slug>", views.department_detail, name="department_detail"),
]
