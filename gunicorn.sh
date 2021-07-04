#!/usr/bin/env bash

gunicorn --config gunicorn.conf.py app:app
