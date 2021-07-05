[![tests](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml)
[![linter](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml)
[![codecov](https://codecov.io/gh/dayyass/muse_as_service/branch/main/graph/badge.svg?token=RRSTQY2R2Y)](https://codecov.io/gh/dayyass/muse_as_service)
[![license](https://img.shields.io/github/license/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/blob/main/LICENSE)
[![release (latest by date)](https://img.shields.io/github/v/release/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/releases/latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/dayyass/muse_as_service/blob/main/.pre-commit-config.yaml)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What is MUSE?
**MUSE** stands for *Multilingual Universal Sentence Encoder* - multilingual extension (16 languages) of *Universal Sentence Encoder* (USE).<br>
MUSE/USE models encode sentences into embedding vectors of fixed size.

- *MUSE* paper: [link](https://arxiv.org/abs/1907.04307).
- *USE* paper: [link](https://arxiv.org/abs/1803.11175).

### What is MUSE as Service?
**MUSE as Service** is REST API for sentence tokenization and embedding using MUSE from [TensorFlow Hub](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3).<br>
It is written with *flask* + *gunicorn* = ❤️.<br>

### Why I need it?
MUSE from [TensorFlow Hub](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3) requires to be installed:
- *tensorflow*
- *tensorflow-hub*
- *tensorflow-text*

These libraries take up more than **1GB** of memory. The model itself takes up **280MB** of memory.

For efficient memory usage when working with *MUSE* on several projects (several virtual environments) and with teammates (several model copies on different computers) it is better to deploy one instance of model with one virtual environment where all teammates have access to.<br>
This is why **MUSE as Service** was made!

### Installation
```
# clone repo (https/ssh)
git clone https://github.com/dayyass/muse_as_service.git
# git clone git@github.com:dayyass/muse_as_service.git

# install dependencies (preferable in venv)
cd calculus_of_variations
pip install -r requirements.txt
```

### Run Service
To build a **docker image** with a service (parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file) run:
```
docker build -t muse_as_service .
```
**NOTE**: instead of building a docker image, you can pull it from [Docker Hub](https://hub.docker.com/r/dayyass/muse_as_service):
```
docker pull dayyass/muse_as_service
```

To launch the service (either locally or on a server) use a **docker container**:
```
docker run -d -p {host_port}:{container_port} --name muse_as_service muse_as_service
```
**NOTE**: `container_port` should be equal to `port` in [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file.

You can also launch a service without docker using:
- *gunicorn*: `./gunicorn.sh` (you can configure *gunicorn* with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file)
- *flask*: `python app.py --host {host} --port {port}` (default `host 0.0.0.0` and `port 5000`)<br>
But it is preferable to launch the service inside the docker container.

### Usage
After you launch the service, you can tokenize and embed any {*sentence*} using **GET requests** (request parametrized with `ip` and `port` where the service was launched, and `token` for authentication):
```
http://{ip}:{port}/tokenize?token={token}&sentence={sentence}
http://{ip}:{port}/embed?token={token}&sentence={sentence}
```
**NOTE**: in all examples of using the service, *token authentication* is used.

You can use python **requests** library to work with GET requests (example [script](https://github.com/dayyass/muse_as_service/blob/main/examples/usage_requests.py)):
```python3
import os

import numpy as np
import requests

# params
ip = os.environ["IP"]
port = int(os.environ["PORT"])
token = os.environ["TOKEN"]

url_service = f"http://{ip}:{port}"
url_tokenize = f"{url_service}/tokenize"
url_embed = f"{url_service}/embed"

# sentence
sentence = "This is sentence example."

# tokenizer
response = requests.get(
    url=url_tokenize,
    params={"token": token, "sentence": sentence},
)
tokenized_sentence = response.json()["tokens"]

# embedder
response = requests.get(
    url=url_embed,
    params={"token": token, "sentence": sentence},
)
embedding = np.array(response.json()["embedding"][0])

# results
print(tokenized_sentence)  # ['▁This', '▁is', '▁sentence', '▁example', '.']
print(embedding.shape)  # (512,)
```

But it is better to use the built-in client [**MUSEClient**](https://github.com/dayyass/muse_as_service/blob/main/muse_as_service/client.py) for sentence tokenization and embedding, that wraps the functionality of the **requests** library and provides a user with a simpler interface (example [script](https://github.com/dayyass/muse_as_service/blob/main/examples/usage_client.py)):
```python3
import os
import sys

sys.path.append("../muse_as_service")

from muse_as_service import MUSEClient  # noqa: E402

# params
ip = os.environ["IP"]
port = int(os.environ["PORT"])
token = os.environ["TOKEN"]

# sentence
sentence = "This is sentence example."

# init client
client = MUSEClient(
    ip=ip,
    port=port,
    token=token,
)

# tokenizer
tokenized_sentence = client.tokenize(sentence)

# embedder
embedding = client.embed(sentence)

# results
print(tokenized_sentence)  # ['▁This', '▁is', '▁sentence', '▁example', '.']
print(embedding.shape)  # (512,)
```

### Tests
To launch [**tests**](https://github.com/dayyass/muse_as_service/tree/main/tests) run:<br>
`python -m unittest discover`

To use [**pre-commit**](https://pre-commit.com) hooks run:<br>
`pre-commit install`

To measure [**code coverage**](https://coverage.readthedocs.io) run:<br>
`coverage run -m unittest discover && coverage report -m`

### Citation
If you use **muse_as_service** in a scientific publication, we would appreciate references to the following BibTex entry:
```bibtex
@misc{dayyass2021muse,
    author       = {El-Ayyass, Dani},
    title        = {Multilingual Universal Sentence Encoder REST API},
    howpublished = {\url{https://github.com/dayyass/muse_as_service}},
    year         = {2021}
}
```
