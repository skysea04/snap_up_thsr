FROM python:3.10.12-slim

WORKDIR /src

COPY ./src .

ADD requirements /requirements

RUN mkdir -p logs/ && \
    apt update && \
    apt install -y libpq5 procps && \
    pip install -r /requirements/live.txt

CMD nohup python manage.py continue_snap_up & gunicorn --bind=0.0.0.0:8000 --timeout=300 --keep-alive=60 src.wsgi:application
