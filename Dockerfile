FROM python:3.9.5-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN python -c "from muse_embedder import download_thhub_model; download_thhub_model()"
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers $WORKERS app:app
