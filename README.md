[![tests](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/tests.yml)
[![linter](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml/badge.svg)](https://github.com/dayyass/muse_as_service/actions/workflows/linter.yml)
[![codecov](https://codecov.io/gh/dayyass/muse_as_service/branch/main/graph/badge.svg?token=RRSTQY2R2Y)](https://codecov.io/gh/dayyass/muse_as_service)
[![license](https://img.shields.io/github/license/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/blob/main/LICENSE)
[![release (latest by date)](https://img.shields.io/github/v/release/dayyass/muse_as_service)](https://github.com/dayyass/muse_as_service/releases/latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/dayyass/muse_as_service/blob/main/.pre-commit-config.yaml)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What is MUSE?
**MUSE** stands for Multilingual Universal Sentence Encoder - multilingual extension ([16 languages](https://github.com/dayyass/muse_as_service#muse-supported-languages)) of Universal Sentence Encoder (USE).<br>
MUSE model encodes sentences into embedding vectors of fixed size.

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
```shell script
# clone repo (https/ssh)
git clone https://github.com/dayyass/muse_as_service.git
# git clone git@github.com:dayyass/muse_as_service.git

# install dependencies (preferable in venv)
cd muse_as_service
pip install --upgrade pip && pip install -r requirements.txt
```

Before using the service you need to:
- download MUSE model with following command:<br>
`
python models/download_muse.py
`
- set up two environment variables `SECRET_KEY` and `JWT_SECRET_KEY` (for security):<br>
`
export SECRET_KEY={SECRET_KEY} JWT_SECRET_KEY={JWT_SECRET_KEY}
`

To generate these keys you can use [this](https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask/34903502) for `SECRET_KEY` and [this](https://mkjwk.org) for `JWT_SECRET_KEY`.

### Launch the Service
To build a **docker image** with a service parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file run:
```shell script
docker build --build-arg SECRET_KEY="${SECRET_KEY}" --build-arg JWT_SECRET_KEY="${JWT_SECRET_KEY}" -t muse_as_service .
```
**NOTE**: instead of building a docker image, you can pull it from [Docker Hub](https://hub.docker.com/r/dayyass/muse_as_service).

To launch the service (either locally or on a server) use a **docker container**:
```shell script
docker run -d -p {host_port}:{container_port} --name muse_as_service muse_as_service
```
**NOTE**: `container_port` should be equal to `port` in [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file.

You can also launch a service without docker, but it is preferable to launch the service inside the docker container:
- **Gunicorn**: `./gunicorn.sh` (parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file)
- **Flask**: `python app.py --host {host} --port {port}` (default `host 0.0.0.0` and `port 5000`)

#### GPU support
MUSE as Service supports **GPU** inference. To launch the service with GPU support use `CUDA_VISIBLE_DEVICES` environment variable to specify GPU device (`CUDA_VISIBLE_DEVICES=""` disables GPU support and uses only CPU).

You can set it up as environment variables with: `export CUDA_VISIBLE_DEVICES=0`

**NOTE**: from **TensorFlow2.0** `tensorflow` and `tensorflow-gpu` packages are not separated. Therefore `tensorflow>=2.0.0` is placed in [requirements.txt](https://github.com/dayyass/muse_as_service/blob/main/requirements.txt).

**NOTE**: depending on installed **CUDA** version you may need different `tensorflow` versions. See [table](https://www.tensorflow.org/install/source#gpu) with TF/CUDA compatibility to choose the right one and `pip install` it.

### Usage
Since the service is usually running on the server, it is important to restrict access to the service.

For this reason, MUSE as Service uses **token-based authorization** with [JWT](https://jwt.io) for users in sqlite database [app.db](https://github.com/dayyass/muse_as_service/tree/main/muse_as_service/database/app.db).

Initially database has only one user with:
- **username**: "admin"
- **password**: "admin"

To add new user with `username` and `password` run:
```shell script
python muse_as_service/database/add_user.py --username {username} --password {password}
```
**NOTE**: no passwords are stored in the database, only their hashes.

MUSE as Service has next endpoints:
<pre>
- /login          - POST request with `username` and `password` to get JWT tokens (access and refresh)
- /logout/access  - POST request to remove JWT access token (JWT access token required)
- /logout/refresh - POST request to remove JWT refresh token (JWT refresh token required)
- /token/refresh  - POST request to refresh JWT access token (JWT refresh token required)
- /tokenize       - GET request for `sentence` tokenization (JWT access token required)
- /embed          - GET request for `sentence` embedding (JWT access token required)
</pre>

You can use python **requests** package to work with HTTP requests:
```python3
import numpy as np
import requests

# params
ip = "localhost"
port = 5000

# login
response = requests.post(
    url=f"http://{ip}:{port}/login",
    json={"username": "admin", "password": "admin"},
)
token = response.json()["access_token"]

# sentences
sentences = ["This is sentence example.", "This is yet another sentence example."]

# tokenizer
response = requests.get(
    url=f"http://{ip}:{port}/tokenize",
    params={"sentence": sentences},
    headers={"Authorization": f"Bearer {token}"},
)
tokenized_sentence = response.json()["tokens"]

# embedder
response = requests.get(
    url=f"http://{ip}:{port}/embed",
    params={"sentence": sentences},
    headers={"Authorization": f"Bearer {token}"},
)
embedding = np.array(response.json()["embedding"])

# results
print(tokenized_sentence)  # [
# ["▁This", "▁is", "▁sentence", "▁example", "."],
# ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]
# ]
print(embedding.shape)  # (2, 512)
```

But it is better to use the built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the python **requests** package and provides a user with a simpler interface.

Instead of using endpoints, listed above, directly, **MUSEClient** provides the following methods to work with:
<pre>
- login         - method to login with `username` and `password`
- logout        - method to logout (login required)
- token_refresh - method to refresh JWT access token (login required)
- tokenize      - method for `sentence` tokenization (login required)
- embed         - method for `sentence` embedding (login required)
</pre>

Usage example:
```python3
from muse_as_service import MUSEClient

# params
ip = "localhost"
port = 5000

# init client
client = MUSEClient(ip=ip, port=port)

# login
client.login(username="admin", password="admin")

# sentences
sentences = ["This is sentence example.", "This is yet another sentence example."]

# tokenizer
tokenized_sentence = client.tokenize(sentences)

# embedder
embedding = client.embed(sentences)

# logout
client.logout()

# results
print(tokenized_sentence)  # [
# ["▁This", "▁is", "▁sentence", "▁example", "."],
# ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]
# ]
print(embedding.shape)  # (2, 512)
```

### Tests
To use [**pre-commit**](https://pre-commit.com) hooks run:<br>
`
pre-commit install
`

Before running tests and code coverage, you need:
- set up two environment variables `SECRET_KEY` and `JWT_SECRET_KEY` (for security):<br>
`
export SECRET_KEY=test JWT_SECRET_KEY=test
`
- run [app.py](https://github.com/dayyass/muse_as_service/blob/main/app.py) in background:<br>
`
python app.py &
`

To launch [**tests**](https://github.com/dayyass/muse_as_service/tree/main/tests) run:<br>
`
python -m unittest discover
`

To measure [**code coverage**](https://coverage.readthedocs.io) run:<br>
`
coverage run -m unittest discover && coverage report -m
`

**NOTE**: since we launched Flask application in background, we need to stop it after running tests and code coverage with following command:
```shell script
kill $(ps aux | grep '[a]pp.py' | awk '{print $2}')
```

### MUSE supported languages
MUSE model supports next languages:
- Arabic
- Chinese-simplified
- Chinese-traditional
- English
- French
- German
- Italian
- Japanese
- Korean
- Dutch
- Polish
- Portuguese
- Spanish
- Thai
- Turkish
- Russian

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
