from django.urls import path

from . import views

app_name = "media_library"

urlpatterns = [
    path("editor-upload/", views.editor_upload, name="editor_upload"),
    path("upload/", views.upload, name="upload"),
    path("picker/", views.picker, name="picker"),
]
