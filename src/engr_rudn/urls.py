from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("admin_utilities/", include("admin_utilities.urls")),
    path("", include("news.urls")),
    path("", include("pages.urls")),
    path("", include("profiles.urls")),
    path("", include("seminars.urls")),
    path(
        f"prometheus-{settings.PROMETHEUS_URL_SUFFIX}/",
        include("django_prometheus.urls"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
