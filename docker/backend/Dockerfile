FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y gcc build-essential libpq-dev python3-dev

WORKDIR /code

COPY ../../requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY ../.. /code/
