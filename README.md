# Engineering Academy Of RUDN (engr.rudn.ru)

<div align="center">
</div>

---

<p align="center">Сайт Инженерной Академии РУДН<br></p>

![Статус](https://img.shields.io/badge/status-active-success.svg)

## Содержание

- [О проекте](#-о-проекте)
- [Начало работы](#-начало-работы)
  - [Основные требования](#основные-требования)
  - [Начальная установка](#начальная-установка)
  - [Запуск локального сервера](#запуск-локального-сервера)
- [Развертывание](#-развертывание)
- [Примененные технологии](#%EF%B8%8F-примененные-технологии)

## 🧐 О проекте

Сайт Инженерной Академии РУДН, написанный на Python, Django.
База данных - PostgreSQL.
Для сбора статистики используются Prometheus(django-prometheus), Grafana.
В качестве прокси-сервера используется nginx.
WSGI HTTP сервер - gunicorn

## 🏁 Начало работы

Эти инструкции позволят вам запустить копию проекта на локальном компьютере в целях разработки и тестирования. К ак развернуть проект в действующей системе описано в разделе Развертывание.

### Основные требования

- [Python 3.11+](https://www.python.org/)
- [PostgreSQL Latest](https://www.postgresql.org/)

### Начальная установка

Инициализировать локальный репозиторий

```
$ git init
```

Добавить удаленный репозиторий:

```
$ git remote add origin https://github.com/EfremovEgor/engr.rudn.ru
```

Загрузить проект с удаленного репозитория:

```
$ git pull origin main
```

Создать виртуальное окружение:

```
$ python3 -m venv .venv
```

Включить виртуальное окружение:

```
$ .venv/bin/activate
```

Установить зависимости:

```
$ pip install -r requirements.txt
```

Создать .env файл и заполнить его:

```
$ make create_env
```

Пример:

```
DJANGO_DATABASE_HOST= localhost
DJANGO_DATABASE_PORT= 5432
DJANGO_DATABASE_NAME= engr.rudn.ru
DJANGO_DATABASE_USER= postgres
DJANGO_DATABASE_PASSWORD= postgres
PROMETHEUS_URL_SUFFIX= random_base64_string_url_safe
```

### Запуск локального сервера

Изменить директорию:

```
$ cd src
```

Применить миграции:

```
$ python3 manage.py migrate
```

Создать профиль администратора:

```
$ python3 manage.py createsuperuser
```

Запустить сервер:

```
$ python3 manage.py runserver
```

Сайт будет доступен по ссылке <http://127.0.0.1:8000/>
Доступ к админке по ссылке <http://127.0.0.1:8000/admin>

## 🚀 Развертывание

[Ссылка на руководство](/documentation/deployment/Deployment.md)

## ⛏️ Примененные технологии

- [PostgreSQL](https://www.postgresql.org/) - База данных
- [Django](https://www.djangoproject.com/) - Веб фреймворк
- [Nginx](https://www.nginx.com/) - Прокси-сервер
