FROM python:3.10.6

COPY . .
WORKDIR .
EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
