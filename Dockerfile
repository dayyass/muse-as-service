FROM python:3.7-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>
WORKDIR /app
COPY . .

# environment variables
ARG SECRET_KEY
RUN test -n "$SECRET_KEY"  # mandating the variable to be passed as the build time argument
ENV SECRET_KEY=$SECRET_KEY

ARG JWT_SECRET_KEY
RUN test -n "$SECRET_KEY"  # mandating the variable to be passed as the build time argument
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY

# instal dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# download MUSE from tfhub
RUN python models/download_muse.py

# run gunicorn server
CMD gunicorn --config gunicorn.conf.py app:app
