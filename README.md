# Сервис авторизации. Проектная работа 7 спринта.
[![Generic badge](https://img.shields.io/badge/Changelog-<COLOR>.svg)](./CHANGELOG.md)
[![Generic badge](https://img.shields.io/badge/Our-Team-<COLOR>.svg)](#команда)


Этот сервис будет аутентифицировать всех пользователей кинотеатра. Реализована возможность создать аккаунт используя учетную запись Yandex или VK.
[Ссылка на приватный репозиторий с командной работой.](https://github.com/Riyce/Auth_sprint_2)

## Используемые технологии
- Код приложения на Python + Flask.
- Регистрация с помощью социальных сетей (OAuth2).
- Приложение запускается под управлением сервера gunicorn и использует Jaeger трассировку.
- В качестве хранилища используется Postgres и Redis.
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Клонировать репозиторий
    git clone https://github.com/Riyce/Auth_sprint_2.git

## Подготовить .env файл с переменными окружения
TODO: Актуализировать под текущий проект
    POSTGRES_USER=auth_user
    POSTGRES_PASSWORD=secret
    POSTGRES_DB=auth_db
    POSTGRES_HOST=postgres

    REDIS_HOST=redis
    FLASK_APP=app flask run --with-threads

    #JTW config
    SECRET_KEY=secretkeysecretkey
    ACCESS_TOKEN_EXPIRES_MINUTES=30
    REFRESH_TOKEN_EXPIRES_DAYS=30

## Запуск компонентов системы
Перейти в каталог `docker`

    cd docker

### Для продакшен среды

    DOCKER_BUILDKIT=1 docker-compose -f prod.yaml up --build

### Для среды разработки
    DOCKER_BUILDKIT=1 docker-compose -f prod.yaml -f dev-override.yaml up --build --force-recreate

## Документация сервиса Auth доступна по ссылке
- http://127.0.0.1:8000/apidocs/

## Трассировщик доступен по ссылке
- http://127.0.0.1:16686/search

## Тестирование
TODO: Актуализировать под текущий проект
Тесты содержаться в диретории `tests/functional`. Для их запуска необходимо выполнить команду:

    cd tests/functional && docker-compose -f "docker-compose.yml" up -d --build

Результат тестирования будет сформирован в директории `tests/tests_result` и будет доступен в 2 видах:
- [как текстовый вывод pytest](tests/tests_result/tests_result.txt)
- [как HTML-отчет](tests/tests_result/report.html)

# Команда
- [Ruslan Sibgatulin (lead)](https://github.com/RuslanSibgatulin)
- [Fedor Kuzminov](https://github.com/Riyce)