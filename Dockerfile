FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# gettext — для compilemessages (переводы интерфейса)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && useradd --uid 1000 --create-home app \
    && mkdir -p /app/src/uploads /app/src/staticfiles \
    && cd /app/src \
    && export DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=0 \
    && python manage.py collectstatic --noinput \
    && python manage.py compilemessages \
    && chown -R app:app /app

WORKDIR /app/src
USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8000') + '/healthz')" || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn"]
