from django.conf import settings
from django.http import Http404

from .views import page_detail


class PageFallbackMiddleware:
    """Если адрес не найден (404), пробуем показать страницу Page с таким путём.

    Так страницы, созданные в админке, не перекрывают существующие разделы сайта
    и не ломают перенаправление на адрес со слэшем (APPEND_SLASH).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code != 404:
            return response
        path = request.path_info
        lang = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
        if lang != settings.LANGUAGE_CODE and path.startswith(f"/{lang}/"):
            path = path[len(lang) + 1 :]
        try:
            return page_detail(request, path)
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
