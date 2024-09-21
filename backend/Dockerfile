FROM python:3.10-alpine

COPY req.txt /temp/req.txt

RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password service-user

RUN pip install -r /temp/req.txt

WORKDIR /app

COPY core .

EXPOSE 8000
USER service-user