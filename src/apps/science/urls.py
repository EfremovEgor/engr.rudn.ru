from django.urls import path

from . import views

app_name = "science"

urlpatterns = [
    path("science/scientific_centers", views.centers, name="centers"),
    path("science/scientific_centers/<str:slug>", views.center_detail, name="center_detail"),
    path("science/dissertation_committees", views.dissertation_committees, name="dissertation_committees"),
    path(
        "science/dissertation_committees/<int:pk>",
        views.dissertation_committee_detail,
        name="dissertation_committee_detail",
    ),
]
