FROM python:3.9.5-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>
WORKDIR /app
COPY . .

# instal dependencies
RUN pip install -r requirements.txt

# download MUSE from tfhub
RUN python -c "from muse_as_service import download_thhub_model; download_thhub_model()"

# run gunicorn server
RUN chmod 777 gunicorn.sh
CMD ./gunicorn.sh
