from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path
from django.views.i18n import set_language

from apps.core.sitemaps import sitemaps

admin_prefix = f"admin-{settings.ADMIN_URL_SUFFIX}" if settings.ADMIN_URL_SUFFIX else "admin"

urlpatterns = [
    path(f"{admin_prefix}/rosetta/", include("rosetta.urls")),
    path(f"{admin_prefix}/", admin.site.urls),
    path("_media-library/", include("apps.media_library.urls")),
    path("i18n/setlang/", set_language, name="set_language"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("healthz", lambda request: HttpResponse("ok", content_type="text/plain"), name="healthz"),
]

urlpatterns += i18n_patterns(
    path("", include("apps.pages.urls")),
    path("", include("apps.news.urls")),
    path("", include("apps.academy.urls")),
    path("", include("apps.education.urls")),
    path("", include("apps.science.urls")),
    path("", include("apps.seminars.urls")),
    path("", include("apps.documents.urls")),
    path("", include("apps.profiles.urls")),
    prefix_default_language=False,
)

if settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
