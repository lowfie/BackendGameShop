import smtplib
from email.message import EmailMessage

from celery import Celery
from app.settings.config import (
    SMTP_MAIL,
    SMTP_PASSWORD,
    SMTP_HOST,
    SMTP_PORT,
    HOST_REDIS,
    PORT_REDIS
)


celery = Celery('tasks', broker=f'redis://{HOST_REDIS}:{PORT_REDIS}')


def get_email_game_discount_info(game_data: dict, to_addr: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'GameShopApi: discount notification'
    email['From'] = SMTP_MAIL
    email['To'] = to_addr
    email.set_content(
        'В вашей корзине появилась игра со скидкой!\n'
        f'Скидка на игру {game_data["title"]} в {game_data["discount"]*100}%, теперь она стоит {game_data["price"]} рублей\n'
        'Успей купить!',
    )
    return email


@celery.task
def send_mail_game_discount(game_data: dict, to_email: str):
    email = get_email_game_discount_info(game_data, to_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_MAIL, SMTP_PASSWORD)
        server.send_message(email)
