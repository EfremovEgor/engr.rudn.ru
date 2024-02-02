```
<p align="center"><a href="" rel="noopener">  </a><img width="200px" height="200px" src="https://i.imgur.com/6wj0hh6.jpg" alt="Логотип проекта"></p>

<h3 align="center">Название Проекта</h3>

<div align="center">
</div>

[]()![Статус](https://img.shields.io/badge/status-active-success.svg)
```

# #Development

## Initial Setup

`$ git remote add origin https://github.com/EfremovEgor/engr.rudn.ru`

## Update repo

`$ git pull origin main`

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