from django.urls import path
from . import views


urlpatterns = [
    path(
        "update_study_profiles",
        views.UpdateStudyProfilesView.as_view(),
        name="update_study_profiles",
    ),
]
