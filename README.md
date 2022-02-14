# Storage

Тестовое задание. Сервис для хранения данных о пользователях. Написано на django и drf.

Спецификация апи доступна по домашнему адресу, а так же в файле `swagger.yaml` .

Имеется make файл:

- make build - билд проекта используя docker-compose
- make start - поднимает в фоне docker-compose с заполненным приложением по адресу `localhost:88`
- make stop - остановка приложения
- make restart - рестарт приложения
- make admin - создания админа

Шаги запуска:

1. make build
2. make admin
3. make start
