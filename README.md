![License](https://img.shields.io/github/license/dayyass/muse_as_service)
![release (latest by date)](https://img.shields.io/github/v/release/dayyass/muse_as_service)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### What is MUSE?
**MUSE** stands for **Multilingual Universal Sentence Encoder** - multilingual extension (16 languages) of **Universal Sentence Encoder** (**USE**).<br>
**MUSE/USE** models encode sentences into embedding vectors of fixed size.

**MUSE** paper: [link](https://arxiv.org/abs/1907.04307). <br>
**USE** paper: [link](https://arxiv.org/abs/1803.11175). <br>
**USE** Visually Explainer article: [link](https://amitness.com/2020/06/universal-sentence-encoder/).

### What is MUSE as Service?
**MUSE as Service** is REST API for sentence tokenization and embedding using MUSE.<br>
It is written on **flask + gunicorn**.<br>

### Installation
```
# clone repo
git clone https://github.com/dayyass/muse_as_service.git

# install dependencies
cd muse_as_service
pip install -r requirements.txt
```

### Run Service
To build a **docker image** with a service (parametrized with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file) run:
```
docker build -t muse_as_service .
```
**NOTE**: instead of building a docker image, you can pull it from [Docker Hub](https://hub.docker.com/r/dayyass/muse_as_service): `docker pull dayyass/muse_as_service`

To launch the service (either locally or on a server) use a **docker container**:
```
docker run -d -p {HOST_PORT}:{CONTAINER_PORT} --name muse_as_service muse_as_service
```
**NOTE**: `CONTAINER_PORT` should be equal to `PORT` in [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file.

You can also launch a service without docker using:
- *gunicorn*: `./gunicorn.sh` (you can configure **gunicorn** with [gunicorn.conf.py](https://github.com/dayyass/muse_as_service/blob/main/gunicorn.conf.py) file)
- *flask*: `python app.py --host {HOST} --port {PORT}` (default `host 0.0.0.0` and `port 5000`)<br>
But it is preferable to launch the service inside the docker container.

### Usage
After you launch the service, you can tokenize and embed any {*sentence*} using **GET requests** ({*ip*} is the address where the service was launched):
```
http://{ip}:5000/tokenize?sentence={sentence}
http://{ip}:5000/embed?sentence={sentence}
```

You can use python **requests** library to work with GET requests (example [notebook](https://github.com/dayyass/muse_as_service/blob/main/examples/usage_requests.ipynb)):
```python3
import numpy as np
import requests

ip = "localhost"
port = 5000
token = "TOKEN"

url_service = f"http://{ip}:{port}"
url_tokenize = f"{url_service}/tokenize"
url_embed = f"{url_service}/embed"

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

But it is better to use the built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the **requests** library and provides a user with a simpler interface (example [notebook](https://github.com/dayyass/muse_as_service/blob/main/examples/usage_client.ipynb)):
```python3
from muse_as_service import MUSEClient

ip = "localhost"
port = 5000
token = "TOKEN"

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
