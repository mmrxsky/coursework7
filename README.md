# Проект бэкенд части SPA веб-приложения треекер "Полезных привычек"

## Для работы необходимо установить зависимости из файла [requirements.txt](https://github.com/mmrxsky/coursework7/blob/main/requirements.txt) и заполнить [.env.sample](https://github.com/mmrxsky/coursework7/blob/main/.env.sample) 

# Структура проекта:
## Описаны модели для пользователей (Users),
### Привычка:

Пользователь — создатель привычки.

Место — место, в котором необходимо выполнять привычку.

Время — время, когда необходимо выполнять привычку.

Действие — действие, которое представляет собой привычка.

Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.

Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.

Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.

Вознаграждение — чем пользователь должен себя вознаградить после выполнения.

Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.

Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.

## Описан контроллер для создания пользователя и CRUD для привычек
## Реализована пагинация:
Для вывода списка привычек реализована пагинация с выводом по 5 привычек на страницу.
## Описаны права доступа:
Каждый пользователь имеет доступ только к своим привычкам по механизму CRUD.

Пользователь может видеть список публичных привычек без возможности их как-то редактировать или удалять.

## Добавлена валидация
## Настроили отложенную задачу через Celery.
## Проект покрыт тестами([.coverage](https://github.com/mmrxsky/coursework7/blob/main/.coverage))
## Оформлена документация drf-yasg
## Настроена интеграция с Telegram для уведомлений
## Настроен CORS
=======
