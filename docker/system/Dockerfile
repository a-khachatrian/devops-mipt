FROM python:3.9-alpine

WORKDIR /app

COPY flaskr-tdd/requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY flaskr-tdd .
