FROM python:3.8-slim

WORKDIR /app

COPY ./scripts-python/. /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
