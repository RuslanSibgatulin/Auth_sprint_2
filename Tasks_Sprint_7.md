# Задачи на спринт 7

## Упростите регистрацию и аутентификацию пользователей.
[Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/a5022019-8fe6-438a-9fce-9d0d2acbf902/lessons/5d652865-4bd6-4822-b6e3-35847bf53023/)
Добавить VK, Google, Yandex или Mail. Библиотека [OAuthLib](https://oauthlib.readthedocs.io/en/latest/index.html)
* Реализуйте возможность открепить аккаунт в соцсети от личного кабинета.

## Документация
[Документация контракта сервисов.](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/132b9dd4-6c3e-4b29-aeda-30bd7b289a5c/lessons/ef1e42a8-b712-4b5c-bfae-11dc53781305/)
Подготовьте Auth сервис к интеграции с другими сервисами вашего сайта. Сгенерируйте схему взаимодействия с Auth сервисом в формате, который используется в вашем сервисе.
https://python-jsonschema.readthedocs.io/en/stable/#

## Интеграция Auth-сервиса и AsyncAPI-сервиса
[Создание интеграции Auth-сервиса и AsyncAPI-сервиса, используя контракт, который вы сделали в прошлом задании.](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/132b9dd4-6c3e-4b29-aeda-30bd7b289a5c/lessons/a92ab4ab-2e57-4f7c-9c78-e30da3533840/)
При создании интеграции не забудьте учесть изящную деградацию Auth-сервиса. Как вы уже выяснили ранее, Auth сервис один из самых нагруженных, потому что в него ходят большинство сервисов сайта. И если он откажет, сайт отказать не должен. Обязательно учтите этот сценарий в интеграциях с Auth-сервисом.
Добавить функцию в Movies-API для проверки доступности Auth-API.

## Трассировка. 
[Добавьте в Auth трасcировку и подключите к Jaeger](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/132b9dd4-6c3e-4b29-aeda-30bd7b289a5c/lessons/21882374-e443-4904-8dc2-a663e596afb6/). Для этого вам нужно добавить работу с заголовком x-request-id и отправку трасировок в Jaeger. 

Docker image `jaegertracing/all-in-one:latest`. https://www.jaegertracing.io/

* Задание со звёздочкой - Сделайте декоратор @trace для трассировок любых функций.

## Лимитер.
[Реализуйте алгоритм Leaky bucket или Token bucket, используя Redis для синхронизации реплик](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/132b9dd4-6c3e-4b29-aeda-30bd7b289a5c/lessons/971e63bb-2c07-4f47-8d14-906596e853a2/)

- https://flask-limiter.readthedocs.io/en/stable/
- https://nginx.org/ru/docs/http/ngx_http_limit_req_module.html


## Партицирование таблиц
[Партицируйте таблицу с пользователями](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/132b9dd4-6c3e-4b29-aeda-30bd7b289a5c/lessons/e0c19137-e6dd-4912-8657-0aabbe0c53c3/). Подумайте, по каким критериям вы бы разделили её. Важно посмотреть на таблицу не только в текущем времени, но и заглядывая в некое будущее, когда в ней будут миллионы записей. Пользователи могут быть из одной страны, но из разных регионов. А еще пользователи могут использовать разные устройства для входа и иметь разные возрастные ограничения. 
- https://habr.com/ru/post/273933/
- https://alexey-soshin.medium.com/dealing-with-partitions-in-postgres-11-fa9cc5ecf466


## Фильтрация ботов для Smart TV. Задание со звёздочкой.
[Реализуйте свой вариант фильтрации ботов для Smart TV](https://practicum.yandex.ru/learn/middle-python/courses/bee501cd-0824-4f5a-8072-8641b4e954e9/sprints/40562/topics/c35d278c-12a8-46a2-b244-e9cb5dfdf53c/lessons/f3e5061b-be5d-43f1-ba6a-c19d19d787da/). На Smart TV не будет работать noCaptcha, потому что в нём вряд ли есть история, а анализировать поведение пользователя очень сложно из-за механики работы умного телевизора. Вам придётся реализовать каптчу на математических примерах: генерировать простую задачку и отправлять её пользователю.
Подумайте, в какой из баз данных вы будете хранить правильный ответ. Дадите ли вы только один шанс ввести правильный ответ или позволите пользователю ошибаться несколько минут подряд? Станете ли с подозрением относиться к ответам, которые приходят слишком часто для человека? 