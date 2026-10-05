import logging
import os
import signal

from django.conf import settings
from django.dispatch import receiver
from rosetta.signals import post_save as rosetta_post_save

logger = logging.getLogger(__name__)


@receiver(rosetta_post_save)
def reload_workers_after_translation(sender, language_code=None, request=None, **kwargs):
    """После сохранения перевода в Rosetta перезапускаем воркеры gunicorn (HUP мастеру),
    иначе остальные воркеры продолжат отдавать старые строки из кэша gettext."""
    if not settings.RELOAD_WORKERS_ON_TRANSLATION:
        return
    try:
        os.kill(os.getppid(), signal.SIGHUP)
        logger.info("Перевод %s сохранён, воркеры gunicorn перезапускаются", language_code)
    except (OSError, AttributeError) as exc:  # SIGHUP нет на Windows
        logger.warning("Не удалось перезапустить воркеры: %s", exc)
