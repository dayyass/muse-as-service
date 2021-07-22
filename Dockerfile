FROM python:3.7-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>
WORKDIR /app
COPY . .

# instal dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# download MUSE from tfhub
RUN python models/download_muse.py

# run gunicorn server
CMD gunicorn --config gunicorn.conf.py app:app
