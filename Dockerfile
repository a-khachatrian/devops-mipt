FROM python:3.9-alpine as build

WORKDIR /app

COPY flaskr-tdd/requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY flaskr-tdd .

FROM python:3.9-alpine

WORKDIR /app

COPY --from=build /opt/venv /opt/venv
COPY --from=build /app .

ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_APP=project/app.py
ENV FLASK_ENV=production

RUN addgroup -S flaskgroup && \
    adduser -S flaskuser -G flaskgroup && \
    chown -R flaskuser:flaskgroup /app
USER flaskuser

EXPOSE 5000

CMD sh -c "flask db init && flask db upgrade && flask --app project.app init-db && flask run --host 0.0.0.0"
