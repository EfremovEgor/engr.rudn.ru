COMPOSE = docker compose

# Обновление продакшена: свежий код, сборка образа, перезапуск (миграции применяются при старте)
update:
	git pull
	$(COMPOSE) build
	$(COMPOSE) up -d
	$(COMPOSE) logs --tail=50 web

logs:
	$(COMPOSE) logs -f web

shell:
	$(COMPOSE) exec web python manage.py shell

createsuperuser:
	$(COMPOSE) exec web python manage.py createsuperuser

# Резервная копия БД перед обновлением (рядом с проектом, в backups/)
backup:
	mkdir -p backups
	pg_dump -Fc -h $${DJANGO_DATABASE_HOST:-localhost} -U $${DJANGO_DATABASE_USER:-postgres} $${DJANGO_DATABASE_NAME:-engr.rudn.ru} > backups/db-$$(date +%Y%m%d-%H%M%S).dump

# Проверить, что миграции применятся к текущей БД (без изменений)
migrate-plan:
	$(COMPOSE) run --rm -e RUN_MIGRATIONS=0 web python manage.py migrate --plan

# Обновить .po после изменения шаблонов
messages:
	cd src && python manage.py makemessages -l en -l ru --ignore=.venv

dev:
	$(COMPOSE) -f docker-compose.dev.yml up --build

test:
	$(COMPOSE) -f docker-compose.dev.yml run --rm web python manage.py test
