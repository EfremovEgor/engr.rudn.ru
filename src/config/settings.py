"""
Настройки проекта «Инженерная академия РУДН».

Все параметры окружения читаются из переменных среды (см. .env.example в корне репозитория).
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

load_dotenv(PROJECT_DIR / ".env")
load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    return default if value in (None, "") else value.strip()


def env_bool(name: str, default: bool = False) -> bool:
    value = env(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on", "debug"}


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in (env(name, default) or "").split(",") if item.strip()]


# --- Основное -------------------------------------------------------------------------

# Совместимость со старым .env: ENVIRONMENT=DEBUG включал режим отладки.
DEBUG = env_bool("DJANGO_DEBUG", env("ENVIRONMENT", "") == "DEBUG")

SECRET_KEY = env("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Задайте DJANGO_SECRET_KEY в переменных окружения.")
    SECRET_KEY = "dev-only-insecure-secret-key"

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "academy.rudn.ru,localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS", "https://academy.rudn.ru,http://academy.rudn.ru"
)
SITE_URL = env("SITE_URL", "https://academy.rudn.ru")

# Секретный суффикс адреса админки: /admin-<suffix>/
ADMIN_URL_SUFFIX = env("DJANGO_ADMIN_URL_SUFFIX", "")

# --- Приложения ---------------------------------------------------------------------

INSTALLED_APPS = [
    # modeltranslation должен идти до django.contrib.admin
    "modeltranslation",
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sitemaps",
    # Сторонние
    "django_ckeditor_5",
    "django_jsonform",
    "phonenumber_field",
    "rosetta",
    # Сервисы проекта
    "apps.core",
    "apps.media_library",
    "apps.profiles",
    "apps.academy",
    "apps.education",
    "apps.science",
    "apps.seminars",
    "apps.news",
    "apps.documents",
    "apps.pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.pages.middleware.PageFallbackMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site",
            ],
            # Фильтры сайта доступны во всех шаблонах без {% load %}
            "builtins": ["apps.core.templatetags.custom_tags"],
        },
    },
]

# --- База данных ------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DJANGO_DATABASE_NAME", "academy"),
        "USER": env("DJANGO_DATABASE_USER", "postgres"),
        "PASSWORD": env("DJANGO_DATABASE_PASSWORD", ""),
        "HOST": env("DJANGO_DATABASE_HOST", "localhost"),
        "PORT": env("DJANGO_DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": int(env("DJANGO_DATABASE_CONN_MAX_AGE", "60")),
        "CONN_HEALTH_CHECKS": True,
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

LOGIN_URL = reverse_lazy("admin:login")
LOGIN_REDIRECT_URL = reverse_lazy("admin:index")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Интернационализация ----------------------------------------------------------------

LANGUAGE_CODE = "ru"
LANGUAGES = (
    ("ru", _("Русский")),
    ("en", _("English")),
)
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Переводы контента в БД: поля <field>_ru / <field>_en, при пустом EN показывается RU.
MODELTRANSLATION_DEFAULT_LANGUAGE = "ru"
MODELTRANSLATION_LANGUAGES = ("ru", "en")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("ru",)
MODELTRANSLATION_CUSTOM_FIELDS = ("ArrayField",)

# Переводы интерфейсных строк (.po) через Rosetta
ROSETTA_SHOW_AT_ADMIN_PANEL = False
ROSETTA_MESSAGES_PER_PAGE = 25
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = False
ROSETTA_EXCLUDED_APPLICATIONS = ("unfold", "rosetta", "modeltranslation")
ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_UWSGI_AUTO_RELOAD = False
# В Docker (gunicorn) после сохранения перевода воркеры перезапускаются, чтобы подхватить .mo
RELOAD_WORKERS_ON_TRANSLATION = env_bool("RELOAD_WORKERS_ON_TRANSLATION", False)

# --- Статика и медиа --------------------------------------------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(env("DJANGO_STATIC_ROOT", str(BASE_DIR / "staticfiles")))

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("DJANGO_MEDIA_ROOT", str(BASE_DIR / "uploads")))

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedStaticFilesStorage"
        )
    },
}
# В режиме отладки медиа раздаёт Django, в проде — nginx.
SERVE_MEDIA = env_bool("DJANGO_SERVE_MEDIA", DEBUG)

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_PERMISSIONS = 0o644
MEDIA_LIBRARY_MAX_UPLOAD_SIZE = int(env("MEDIA_LIBRARY_MAX_UPLOAD_MB", "200")) * 1024 * 1024

# --- Безопасность -------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = env_bool("DJANGO_USE_X_FORWARDED_HOST", False)
SESSION_COOKIE_SECURE = env_bool("DJANGO_SECURE_COOKIES", not DEBUG)
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "SAMEORIGIN"

# --- Логирование ----------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": env("DJANGO_LOG_LEVEL", "INFO")},
}

# --- Редактор контента (CKEditor 5) -------------------------------------------------

CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME = "media_library:editor_upload"
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True
CKEDITOR_5_UPLOAD_FILE_TYPES = [
    "jpeg", "jpg", "png", "gif", "webp", "svg", "pdf", "doc", "docx", "xls", "xlsx",
    "ppt", "pptx", "zip", "mp4", "webm",
]
CKEDITOR_5_CUSTOM_CSS = "academy_admin/css/editor.css"
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "ru",
        "toolbar": {
            "items": [
                "heading", "|", "bold", "italic", "underline", "strikethrough", "link",
                "|", "fontColor", "fontBackgroundColor", "removeFormat",
                "|", "alignment", "bulletedList", "numberedList", "outdent", "indent",
                "|", "insertImage", "mediaEmbed", "insertTable", "blockQuote", "htmlEmbed",
                "horizontalLine", "specialCharacters",
                "|", "undo", "redo", "findAndReplace", "sourceEditing", "showBlocks",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Абзац", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Заголовок 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Заголовок 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Заголовок 4", "class": "ck-heading_heading4"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "|", "imageStyle:alignLeft", "imageStyle:alignCenter",
                "imageStyle:alignRight", "imageStyle:side", "|", "toggleImageCaption", "linkImage",
            ],
            "styles": ["alignLeft", "alignCenter", "alignRight", "side", "full"],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties",
            ]
        },
        "mediaEmbed": {"previewsInData": True},
        "link": {"addTargetToExternalLinks": True},
        # Сохраняем произвольную разметку старого контента (div, style, iframe, video...)
        "htmlSupport": {
            "allow": [{"name": "/.*/", "attributes": True, "classes": True, "styles": True}]
        },
        "htmlEmbed": {"showPreviews": False},
    },
}

# --- Админка (Unfold) ---------------------------------------------------------------


def _admin_url(name: str):
    return reverse_lazy(f"admin:{name}")


UNFOLD = {
    "SITE_TITLE": "Инженерная академия РУДН",
    "SITE_HEADER": "Инженерная академия",
    "SITE_SUBHEADER": "Управление сайтом",
    "SITE_URL": "/",
    "SITE_SYMBOL": "school",
    "SITE_FAVICONS": [
        {"rel": "icon", "sizes": "any", "type": "image/png", "href": "/static/images/favicon.png"},
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": "apps.core.admin.dashboard.environment_callback",
    "DASHBOARD_CALLBACK": "apps.core.admin.dashboard.dashboard_callback",
    "SITE_VIEWS": [
        ("translations/", "translations_overview", "apps.core.admin.dashboard.TranslationsOverviewView"),
    ],
    "STYLES": [lambda request: STATIC_URL + "academy_admin/css/admin.css"],
    "SCRIPTS": [lambda request: STATIC_URL + "academy_admin/js/admin.js"],
    "COLORS": {
        "primary": {
            "50": "oklch(97.1% .013 17.38)",
            "100": "oklch(93.6% .032 17.717)",
            "200": "oklch(88.5% .062 18.334)",
            "300": "oklch(80.8% .114 19.571)",
            "400": "oklch(70.4% .191 22.216)",
            "500": "oklch(63.7% .237 25.331)",
            "600": "oklch(57.7% .245 27.325)",
            "700": "oklch(50.5% .213 27.518)",
            "800": "oklch(44.4% .177 26.899)",
            "900": "oklch(39.6% .141 25.723)",
            "950": "oklch(25.8% .092 26.042)",
        },
    },
    "COMMAND": {"search_models": True, "show_history": True},
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": "apps.core.admin.navigation.sidebar_navigation",
    },
}
