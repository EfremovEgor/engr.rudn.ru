# Engineering Academy Of RUDN (engr.rudn.ru)

<div align="center">
</div>

---

<p align="center">Сайт Инженерной Академии РУДН<br></p>
[]()![Статус](https://img.shields.io/badge/status-active-success.svg)

## Development

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