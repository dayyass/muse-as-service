[![tests](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml)
[![linter](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml)
[![codecov](https://codecov.io/gh/dayyass/muse_as_service/branch/main/graph/badge.svg?token=RRSTQY2R2Y)](https://codecov.io/gh/dayyass/muse_as_service)
[![license](https://img.shields.io/github/license/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/blob/main/LICENSE)
[![release (latest by date)](https://img.shields.io/github/v/release/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/releases/latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/dayyass/muse_as_service/blob/main/.pre-commit-config.yaml)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What is MUSE?
**MUSE** stands for Multilingual Universal Sentence Encoder - multilingual extension (16 languages) of Universal Sentence Encoder (USE). MUSE model encodes sentences into embedding vectors of fixed size.

- MUSE paper: [link](https://arxiv.org/abs/1907.04307)
- USE paper: [link](https://arxiv.org/abs/1803.11175)

### What is MUSE as Service?
MUSE as Service is the **REST API** for sentence tokenization and embedding using MUSE model from [TensorFlow Hub](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3).

It is written using **Flask** and **Gunicorn**.

### Why I need it?
MUSE model from [TensorFlow Hub](https://tfhub.dev/google/universal-sentence-encoder-multilingual/3) requires next packages to be installed:
- tensorflow
- tensorflow-hub
- tensorflow-text

These packages take up more than **1GB** of memory. The model itself takes up **280MB** of memory.

For efficient memory usage when working with MUSE model on several projects (several virtual environments) or/and with teammates (several model copies on different computers) it is better to deploy one instance of the model in one virtual environment where all teammates have access to.

This is what **MUSE as Service** made for! ❤️

### Installation
```
# clone repo (https/ssh)
git clone https://github.com/dayyass/muse_as_service.git
# git clone git@github.com:dayyass/muse_as_service.git

# install dependencies (preferable in venv)
cd muse_as_service
pip install --upgrade pip && pip install -r requirements.txt
```

### Launch the Service
To build a **docker image** with a service parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file run:
```
docker build -t muse_as_service .
```
**NOTE**: instead of building a docker image, you can pull it from [Docker Hub](https://hub.docker.com/r/dayyass/muse_as_service).

To launch the service (either locally or on a server) use a **docker container**:
```
docker run -d -p {host_port}:{container_port} --name muse_as_service muse_as_service
```
**NOTE**: `container_port` should be equal to `port` in [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file.

You can also launch a service without docker using:
- **Gunicorn**: `./gunicorn.sh` (parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file)
- **Flask**: `python app.py --host {host} --port {port}` (default `host 0.0.0.0` and `port 5000`)

But it is preferable to launch the service inside the docker container.

#### GPU support
MUSE as Service supports **GPU** inference. To launch the service with GPU support use `CUDA_VISIBLE_DEVICES` environment variable to specify GPU device (`CUDA_VISIBLE_DEVICES=""` disables GPU support and uses only CPU):
- **Flask**: `CUDA_VISIBLE_DEVICES={device_number} python app.py --host {host} --port {port}` (default `host 0.0.0.0` and `port 5000`)

**NOTE**: from **TensorFlow2.0** `tensorflow` and `tensorflow-gpu` packages are not separated. Therefore `tensorflow>=2.0.0` is placed in [requirements.txt](https://github.com/dayyass/muse_as_service/blob/main/requirements.txt).<br>
**NOTE**: depending on **CUDA** version you may need different `tensorflow` versions. See [table](https://www.tensorflow.org/install/source#gpu) with TF/CUDA compatibility to choose the right one and `pip install` it.

#### Token Authentification
Since the service is usually running on the server, it is important to restrict access to the service. For this reason, MUSE as Service uses token-based authentication.

After you launch the service, you will receive UUID token to access the service.

### Usage
After you launch the service, you can tokenize and embed any sentences using **HTTP GET requests** (request parametrized with `ip` and `port` where the service has launched, and `token` for authentication):
```
http://{ip}:{port}/tokenize?token={token}&sentence={sentence_1}&sentence={sentence_2}
http://{ip}:{port}/embed?token={token}&sentence={sentence_1}&sentence={sentence_2}
```

You can use python **requests** package to work with HTTP GET requests:
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

# sentences
sentences = ["This is sentence example.", "This is yet another sentence example."]

# tokenizer
response = requests.get(
    url=url_tokenize,
    params={"token": token, "sentence": sentences},
)
tokenized_sentence = response.json()["tokens"]

# embedder
response = requests.get(
    url=url_embed,
    params={"token": token, "sentence": sentences},
)
embedding = np.array(response.json()["embedding"])

# results
print(tokenized_sentence)  # [
# ["▁This", "▁is", "▁sentence", "▁example", "."],
# ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]
# ]
print(embedding.shape)  # (2, 512)
```

But it is better to use the built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the python **requests** package and provides a user with a simpler interface:
```python3
import os

from muse_as_service import MUSEClient  # noqa: E402

# params
ip = os.environ["IP"]
port = int(os.environ["PORT"])
token = os.environ["TOKEN"]

# sentences
sentences = ["This is sentence example.", "This is yet another sentence example."]

# init client
client = MUSEClient(
    ip=ip,
    port=port,
    token=token,
)

# tokenizer
tokenized_sentence = client.tokenize(sentences)

# embedder
embedding = client.embed(sentences)

# results
print(tokenized_sentence)  # [
# ["▁This", "▁is", "▁sentence", "▁example", "."],
# ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]
# ]
print(embedding.shape)  # (2, 512)
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
