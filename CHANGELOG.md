# Список изменений

Все заметные изменения в этом проекте будут задокументированы в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) и придерживается [Семантического управления версиями](https://semver.org/spec/v2.0.0.html).

## [1.1.7] - 2022-07-31
- Исправления [Fedor Kuzminov](https://github.com/Riyce).
 
## [1.1.6] - 2022-07-30
- OAuth2 авторизация через VK [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin).

## [1.1.5] - 2022-07-26
- Jaeger трассировка [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin).
- Партицирование таблицы БД login_story [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin). Для обновлении существующей БД воспользуйтесь скриптом `updates/update_login_history_as_parted.sql`
- Контракт Auth-сервиса и AsyncAPI-сервиса [Fedor Kuzminov](https://github.com/Riyce).
- Лимитироване обращеиний к Auth-сервису [Fedor Kuzminov](https://github.com/Riyce).

## [1.1.1] - 2022-07-24
- OAuth2 авторизация через Yandex [Fedor Kuzminov](https://github.com/Riyce).

## [1.0.1] - 2022-07-22
### Добавлено
- Readme.md, Changelog.md [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin).

## [1.0.0] - 2022-07-17
### Добавлено
- Тесты [Fedor Kuzminov](https://github.com/Riyce).
- API CRUD ролей [Fedor Kuzminov](https://github.com/Riyce).
- API аутентификации [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin).
- Docker-инфраструктура проекта [Ruslan Sibgatulin](https://github.com/RuslanSibgatulin).