FROM python:3.10.12-slim

WORKDIR /src

COPY ./src .

ADD requirements /requirements

RUN mkdir -p logs/ && \
    apt update && \
    apt install -y libpq5 procps cron && \
    pip install -r /requirements/live.txt && \
    chmod -R 755 /src/jobs/ && \
    echo "30 */8 * * * su root /src/jobs/health_check.sh >> /src/logs/cron.log 2>&1" >> /var/spool/cron/crontabs/root && \
    echo "0 18 * * * su root /src/jobs/remind_snap_up.sh >> /src/logs/cron.log 2>&1" >> /var/spool/cron/crontabs/root

CMD nohup python manage.py continue_snap_up & set > /etc/environment && cron && gunicorn --bind=0.0.0.0:8000 --timeout=300 --keep-alive=60 src.wsgi:application
