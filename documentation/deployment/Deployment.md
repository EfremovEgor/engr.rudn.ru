# Развёртывание и обновление

Схема продакшена:

```
интернет → nginx (хост, :80/:443) → контейнер web (gunicorn, 127.0.0.1:8000) → PostgreSQL (хост)
                    └── /media/ отдаёт nginx напрямую из src/uploads
```

Сайт работает в Docker (`docker-compose.yml`, `network_mode: host`), PostgreSQL и nginx остаются
на хосте как раньше. Статику отдаёт приложение (whitenoise, со сжатием), загруженные файлы — nginx.
Миграции применяются автоматически при каждом старте контейнера.

## Требования

- Ubuntu 22.04+ с Docker Engine и плагином `docker compose`
- PostgreSQL (существующая база сайта)
- nginx

## Первый переход на новую версию (с systemd/gunicorn на Docker)

> Обязательно сделайте резервную копию базы — миграции меняют структуру таблиц.

1. **Резервная копия БД и файлов**

   ```bash
   cd /var/www/site
   pg_dump -Fc -h localhost -U postgres engr.rudn.ru > ~/backup-before-docker.dump
   tar czf ~/uploads-before-docker.tgz src/uploads
   ```

2. **Проверьте, что в базе применены все старые миграции.** На старой версии кода:

   ```bash
   cd src && python3 manage.py showmigrations | grep "\[ \]"
   ```

   Вывод должен быть пустым. Если на сервере были свои миграции, которых нет в репозитории
   (раньше `settings.py` был в `.gitignore`, и прод мог отличаться), сначала разберитесь с ними.

3. **Получите новую версию и создайте `.env`**

   ```bash
   git fetch && git checkout <ветка или тег новой версии>
   cp .env.example .env
   nano .env
   ```

   Перенесите параметры БД и `DJANGO_ADMIN_URL_SUFFIX` из старого `.env`, задайте новый
   `DJANGO_SECRET_KEY` (раньше ключ был в репозитории — его нужно сменить):

   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

4. **Права на каталоги** (контейнер работает от пользователя с uid 1000):

   ```bash
   sudo chown -R 1000:1000 src/uploads src/locale
   ```

5. **Остановите старый gunicorn и сервисы мониторинга**

   ```bash
   sudo systemctl disable --now gunicorn.socket gunicorn.service
   docker compose down --remove-orphans    # остановит prometheus и grafana
   ```

6. **Проверьте план миграций (ничего не меняет в БД):**

   ```bash
   docker compose build
   docker compose run --rm -e RUN_MIGRATIONS=0 web python manage.py migrate --plan
   ```

7. **Запустите сайт** — миграции применятся при старте:

   ```bash
   docker compose up -d
   docker compose logs -f web
   ```

   В логе миграций могут быть строки с «!» — это не ошибки, а отчёт о данных, которые были
   преобразованы особым образом (профиль в нескольких направлениях, доклад в нескольких
   семинарах, непривязанные условия приёма). Их стоит проверить в админке.

8. **Обновите конфигурацию nginx** (`nginx/engr` из репозитория — проксирование на 127.0.0.1:8000):

   ```bash
   sudo cp nginx/engr /etc/nginx/sites-available/engr
   sudo nginx -t && sudo systemctl reload nginx
   ```

9. **После запуска**
   - зайдите в админку, проверьте разделы «Образовательные программы», «Научные семинары»;
   - «Медиатека» → «Найти файлы на диске» — добавит в медиатеку уже загруженные ранее файлы;
   - при желании удалите тома мониторинга: `docker volume ls | grep -E "prometheus|grafana"`.

### Откат

```bash
docker compose down
pg_restore --clean --if-exists -d engr.rudn.ru ~/backup-before-docker.dump
git checkout <предыдущий коммит>
sudo systemctl enable --now gunicorn.socket gunicorn.service
```

## Обычное обновление

```bash
make backup     # резервная копия БД в backups/
make update     # git pull, сборка образа, перезапуск (миграции применятся сами)
```

## Полезные команды

| Команда | Что делает |
| --- | --- |
| `make logs` | логи сайта |
| `make createsuperuser` | создать администратора |
| `make shell` | Django shell в контейнере |
| `make migrate-plan` | какие миграции будут применены |

## Переменные окружения

См. `.env.example`. Основные:

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | секретный ключ (обязателен, если `DJANGO_DEBUG=0`) |
| `DJANGO_DEBUG` | `1` — режим разработки |
| `DJANGO_ALLOWED_HOSTS` | домены через запятую |
| `DJANGO_ADMIN_URL_SUFFIX` | админка доступна по `/admin-<суффикс>/` |
| `DJANGO_DATABASE_*` | подключение к PostgreSQL |
| `DJANGO_SECURE_COOKIES` | cookie только по HTTPS |
| `RUN_MIGRATIONS` | `0` — не применять миграции при старте |
| `GUNICORN_WORKERS` | число воркеров |
| `MEDIA_LIBRARY_MAX_UPLOAD_MB` | лимит размера файла в медиатеке |

## Переводы интерфейса на сервере

Каталог `src/locale` смонтирован в контейнер, поэтому правки из Rosetta сохраняются в файлах
на хосте (их можно закоммитить в репозиторий). После сохранения перевода воркеры gunicorn
перезапускаются автоматически.
