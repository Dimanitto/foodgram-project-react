# Проект Foodgram - продуктовый помощник

## Технологии:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

## Описание проекта
Сервис Foodgram - это продуктовый помощник, который создан для тех кто любит готовить и готов поделиться рецептами с другими. Гости сервиса могут просматривать рецепты, а после регистрации пользователи смогут создавать собственный рецепты, подписываться на других пользователей, добавлять понравившиеся рецепты в избранное и создавать список покупок, по выбранным рецептам.

Проект разворачивается в Docker контейнерах: backend-приложение API, PostgreSQL-база данных, nginx-сервер и frontend-контейнер.

## Как запустить проект

Клонируйте репозиторий, перейдите в папку, создайте виртуальное окружение, установите docker и docker-compose

Создать файл окружения и заполнить необходимыми параметрами

```
touch .env
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=postgres >> .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres  >> .env
echo DB_HOST=db  >> .env
echo DB_PORT=5432  >> .env
echo SECRET_KEY=************ >> .env
echo DEBUG=0 >> .env
```
вместо * необходимо указать секретный ключ django из settings.
При отключенном дебаге базой данных будет Postgres, в противном случае будет SQLite

Установить и запустить приложения в контейнерах:
```
$ cd infra
$ docker-compose up --build
```

Запустить миграции, создать суперюзера, собрать статику и заполнить БД ингредиентами:
```
$ docker-compose exec backend python manage.py migrate
$ docker-compose exec backend python manage.py createsuperuser
$ docker-compose exec backend python manage.py collectstatic --no-input 
$ docker-compose exec backend python manage.py load_data
```

## Остановить контейнер:
```
$ docker-compose stop
```

### Автор
Selivanov Dmitry
