FROM python:3.10.6

EXPOSE 8000

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["celery", "-A", "app.core.tasks.send_mail:celery", "worker", "--loglevel=INFO"]
