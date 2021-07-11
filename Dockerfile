FROM python:3.9.5-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>
WORKDIR /app
COPY . .

# environment variables
ARG SECRET_KEY
RUN test -n "$SECRET_KEY"
ENV SECRET_KEY=$SECRET_KEY

ARG JWT_SECRET_KEY
RUN test -n "$SECRET_KEY"
ENV JWT_SECRET_KEY=$JWT_SECRET_KEY

# instal dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# download MUSE from tfhub
RUN python models/download_muse.py

# run gunicorn server
RUN chmod 777 gunicorn.sh
CMD ./gunicorn.sh
