FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /mailing_service

WORKDIR /mailing_service

COPY requirements.txt /mailing_service/
RUN pip install -r requirements.txt

COPY . /mailing_service/
