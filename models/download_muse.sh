#!/usr/bin/env bash

DOWNLOAD_LINK="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3?tf-hub-format=compressed"
MODEL_NAME="universal-sentence-encoder-multilingual_3"

curl $DOWNLOAD_LINK -L -o models/${MODEL_NAME}.tar.gz
mkdir models/${MODEL_NAME}
tar xvzf models/${MODEL_NAME}.tar.gz -C models/${MODEL_NAME}
rm models/${MODEL_NAME}.tar.gz
