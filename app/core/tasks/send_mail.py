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


def get_email_game_discount_info(to_addr: str, game_data: dict) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'GameShopApi: discount notification'
    email['From'] = SMTP_MAIL
    email['To'] = SMTP_MAIL
    email.set_content(
        'В вашей корзине появилась игра со скидкой!\n'
        ''
    )
    return email


@celery.task
def send_mail_game_discount(user_mail: str, game_data: dict):
    email = get_email_game_discount_info(user_mail, game_data)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_MAIL, SMTP_PASSWORD)
        server.sendmail(email)
