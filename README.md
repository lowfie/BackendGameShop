# GameWebShop

----------------------------------------
## Что это?

- Прежде всего это пет-проект. Он представляет из себя REST приложение - апи магазина по продаже игр. В нем реализована система аутентификации, карточки игр, покупка, корзина, отзывы, пользовательская библиотека, уведомления об играх со скидкой в корзине.
----------------------------------------
## Как запустить?

1. Клонируйте репозиторий `$ git clone https://github.com/lowfie/BackendGameShop.git`
2. Создайте файл конфигурации `.env` и заполните его
3. Билд проекта `$ docker compose build`
4. Запуск контейнера `$ docker compose up`
----------------------------------------
## Файл конфигурации

```
USER_POSTGRES=
PASSWORD_POSTGRES=
HOST_POSTGRES=
PORT_POSTGRES=
DATABASE_POSTGRES=

SMTP_HOST=
SMTP_PORT=
SMTP_MAIL=
SMTP_PASSWORD=

HOST_REDIS=
PORT_REDIS=

SECRET=
```
----------------------------------------
## Технологии
----------------------------------------
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- Celery
- Redis
- Docker
----------------------------------------
