FROM python:3.10.12-slim

WORKDIR /src

COPY ./src .

ADD requirements /requirements

RUN apt update && \
    apt install -y libpq5 procps && \
    pip install -r /requirements/live.txt

CMD ["gunicorn", "--timeout=300", "--workers=2", "--threads=8", "--keep-alive=60", "src.wsgi:application"]