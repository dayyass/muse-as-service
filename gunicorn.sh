#!/bin/sh

gunicorn --config gunicorn.conf.py app:app
