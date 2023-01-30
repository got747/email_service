# Сервис отправки email рассылок.

Сервис разработан на django rest framework с celery


## Установка и запуск


1. Склонировать репозиторий с Github
```
https://github.com/got747/email_service.git
```
2. Перейти в директорию проекта
3. В файле .evn заполнить данные
4. Запустить контейнеры
```
sudo docker-compose up -d
 ```
5. Остановка работы контейнеров
```
sudo docker-compose stop
```
***
```http://0.0.0.0:8000/api/``` - api проекта

```http://0.0.0.0:8000/api/subscriber/``` - подписчики

```http://0.0.0.0:8000/api/mailing/``` - рассылки

```http://0.0.0.0:8000/api/subscription``` - подписки на рассылки

```http://0.0.0.0:8000/swagger/``` - документация проекта
