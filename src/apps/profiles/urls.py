from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/<int:pk>", views.profile, name="profile"),
    path("profile/<int:pk>/", views.profile),
    path("students/student_committee", views.student_committee, name="student_committee"),
]
