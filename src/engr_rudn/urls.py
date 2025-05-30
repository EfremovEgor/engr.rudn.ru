from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path(f"admin-{settings.ADMIN_SITE}/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(f"admin_utilities-{settings.ADMIN_SITE}/", include("admin_utilities.urls")),
    path(
        f"prometheus-{settings.PROMETHEUS_URL_SUFFIX}/",
        include("django_prometheus.urls"),
    ),
    path('i18n/setlang/', set_language, name='set_language'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("news.urls")),
    path("", include("pages.urls")),
    path("", include("profiles.urls")),
    path("", include("seminars.urls")),
    prefix_default_language=False
)