FROM lab4-system as system
FROM python:3.9-alpine

WORKDIR /app

COPY --from=system /opt/venv /opt/venv
COPY --from=system /app .

ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_APP=project/app.py
ENV FLASK_ENV=production

RUN addgroup -S flaskgroup && \
    adduser -S flaskuser -G flaskgroup && \
    chown -R flaskuser:flaskgroup /app
USER flaskuser

EXPOSE 5000

CMD sh -c "flask db init && flask db upgrade && flask --app project.app init-db && flask run --host 0.0.0.0"