# Инженерная академия РУДН (academy.rudn.ru)

Сайт Инженерной академии РУДН на Django 5.2 и PostgreSQL. Админка на [django-unfold](https://unfoldadmin.com/),
переводы контента — [django-modeltranslation](https://django-modeltranslation.readthedocs.io/),
редактор — CKEditor 5 со встроенной медиатекой. В продакшене сайт работает в Docker за nginx.

- [Развёртывание и обновление продакшена](documentation/deployment/Deployment.md)
- [Руководство редактора](documentation/ADMIN_GUIDE.md)
- [Ревью проекта и список изменений](documentation/REVIEW.md)

## Структура

```
src/
  config/            настройки (всё из переменных окружения), корневые URL
  apps/
    core/            общие классы админки, переводы, фильтры шаблонов, sitemap
    media_library/   медиатека: файлы, папки, загрузка из редактора, поиск использований
    pages/           главная, информационные страницы, страницы из админки (Page)
    news/            новости и тэги
    academy/         кафедры и дирекция
    education/       направления, программы, условия приёма, баллы, ДПО
    science/         научные центры, диссоветы, оборудование, партнёры
    seminars/        научные семинары, доклады, докладчики
    profiles/        сотрудники, сотрудники кафедр, студенческий комитет
    documents/       документы для абитуриентов и студентов
  templates/         общие шаблоны (шапка, подвал) и шаблоны админки
  static/            статика сайта и админки
  locale/            переводы интерфейсных строк (.po)
```

Каждый сервис — отдельное Django-приложение со своими моделями, админкой, views, URL и шаблонами.

## Локальный запуск

### Вариант 1. Всё в Docker

```bash
docker compose -f docker-compose.dev.yml up --build
```

Сайт: http://localhost:8000, админка: http://localhost:8000/admin-dev/.
Суперпользователь: `docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser`.

### Вариант 2. Python на машине

Требуется Python 3.12+ и PostgreSQL.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt     # Windows: .venv\Scripts\pip
cp .env.example .env                           # заполнить, для разработки DJANGO_DEBUG=1
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Админка открывается по адресу `/admin-<DJANGO_ADMIN_URL_SUFFIX>/` (или `/admin/`, если суффикс пуст).

## Тесты

```bash
cd src && python manage.py test apps
```

Тесты используют PostgreSQL (ArrayField). В наборе есть тест миграций: база откатывается
до схемы, которая была до реструктуризации, заполняется данными в старом формате и мигрирует вперёд.

## Переводы

- **Контент** (новости, программы, сотрудники и т. д.) переводится в админке: у каждой записи
  вкладки «Русский» и «English», пустое английское поле показывается на сайте по-русски.
  Сводка — «Переводы контента» в меню админки.
- **Строки интерфейса** (меню, кнопки, тексты свёрстанных страниц) — `src/locale/*/django.po`,
  редактируются в админке через «Строки интерфейса (.po)» (Rosetta) или в репозитории.
  После изменения шаблонов: `make messages`.

## Технологии

Django 5.2 · PostgreSQL · django-unfold · django-modeltranslation · CKEditor 5 · Rosetta ·
whitenoise · gunicorn · Docker · nginx
