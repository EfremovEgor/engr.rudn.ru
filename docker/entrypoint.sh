#!/bin/sh
set -e

cd /app/src

if [ "${RUN_MIGRATIONS:-1}" = "1" ]; then
    echo "Применение миграций..."
    python manage.py migrate --noinput
fi

# Переводы интерфейса могли измениться (Rosetta / git pull) — перекомпилируем .mo
python manage.py compilemessages >/dev/null 2>&1 || echo "compilemessages: пропущено"

if [ "$1" = "gunicorn" ]; then
    exec gunicorn config.wsgi:application \
        --bind "${GUNICORN_BIND:-0.0.0.0:8000}" \
        --workers "${GUNICORN_WORKERS:-3}" \
        --timeout "${GUNICORN_TIMEOUT:-60}" \
        --max-requests 1000 --max-requests-jitter 100 \
        --access-logfile - --error-logfile -
fi

exec "$@"
