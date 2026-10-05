from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "documents"

urlpatterns = [
    path("applicants/reference", views.reference, name="reference"),
    path("applicants/open_days", views.open_days, name="open_days"),
    # Исторический адрес с опечаткой сохранён, чтобы не ломать внешние ссылки
    path("students/appplications", views.student_applications, name="student_applications"),
    path("students/applications", RedirectView.as_view(pattern_name="documents:student_applications")),
]
