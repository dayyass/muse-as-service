FROM python:3.9.5-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers $WORKERS app:app
