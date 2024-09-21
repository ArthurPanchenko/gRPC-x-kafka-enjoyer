FROM python:3.10-alpine

WORKDIR /service

RUN apk add postgresql-client build-base postgresql-dev 
RUN adduser --disabled-password service-user

COPY req.txt /temp/req.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /temp/req.txt --no-cache-dir

COPY core .

EXPOSE 50051