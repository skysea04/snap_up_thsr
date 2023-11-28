FROM python:3.10.12-slim

WORKDIR /src

COPY ./src .

ADD requirements/local.txt /tmp/

RUN apt update && \
    apt install -y libpq5 procps && \
    pip install -r /tmp/local.txt && \
    rm -r /tmp/local.txt

WORKDIR /src
