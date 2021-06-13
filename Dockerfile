FROM python:3.9.5-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python -c "from muse_embedder import download_thhub_model; download_thhub_model()"
CMD gunicorn --bind 0.0.0.0:$PORT --workers $WORKERS --threads $THREADS --timeout 0 app:app
