# Engineering Academy Of RUDN (engr.rudn.ru)

<div align="center">
</div>

---

<p align="center">Сайт Инженерной Академии РУДН<br></p>

![Статус](https://img.shields.io/badge/status-active-success.svg)

## Содержание

- [О проекте](#-о-проекте)
- [Начало работы](#getting_started)
- [Развертывание](#deployment)
- [Применение](#usage)
- [Построен с использованием](#built_using)
- [To Do](../TODO.md)
- [Участие](../CONTRIBUTING.md)
- [Авторы](#authors)
- [Благодарности](#acknowledgement)

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

### Среда разработки

```
$ git remote add origin https://github.com/EfremovEgor/engr.rudn.ru
```

## After setup

`$ git checkout -b feature_name`

### Create .env file with:

`$ make create_env`

then fill .env with your database credentials

### Migrate database:

`$ cd src`

`$ python3 manage.py migrate`

### Create super user:

`$ python3 manage.py createsuperuser`

### Run local server:

`$ python3 manage.py runserver`

## Push changes

`$ git push origin feature_name`