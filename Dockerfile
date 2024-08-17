FROM python:3.10.12-slim

WORKDIR /src

COPY ./src .

ADD requirements /requirements

RUN mkdir -p logs/ && \
    apt update && \
    apt install -y libpq5 procps cron && \
    pip install -r /requirements/live.txt && \
    chmod -R 755 /src/jobs/ && \
    (crontab -l 2>/dev/null; echo "30 */8 * * * /src/jobs/health_check.sh >> /src/logs/cron.log 2>&1") | crontab - && \
    (crontab -l 2>/dev/null; echo "0 18 * * * /src/jobs/remind_snap_up.sh >> /src/logs/cron.log 2>&1") | crontab -

CMD nohup python manage.py continue_snap_up & printenv > /etc/environment && cron && gunicorn --bind=0.0.0.0:8000 --timeout=300 --keep-alive=60 src.wsgi:application
