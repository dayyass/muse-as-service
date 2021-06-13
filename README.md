### MUSE as Service

### What is MUSE?
MUSE stands for Multilingual Universal Sentence Encoder - multilingual extension (16 languages) of Universal Sentence Encoder (USE).<br>
MUSE/USE models encode sentences into embedding vectors of fixed size.

MUSE paper: [link](https://arxiv.org/abs/1907.04307). <br>
USE paper: [link](https://arxiv.org/abs/1803.11175). <br>
USE Visually Explainer article: [link](https://amitness.com/2020/06/universal-sentence-encoder/). <br>

### What is "MUSE as Service"?
*"MUSE as Service"* is REST API for sentence tokenization and embedding using MUSE.<br>
It is written on *Flask + gunicorn*.<br>
You can configure *gunicorn* with [*env.list*](env.list) file.

### Installation
```
# clone repo
git clone https://github.com/dayyass/muse_as_service.git

# install dependencies
cd muse_as_service
pip install -r requirements.txt
```

### Run Service
To launch service use docker container (either locally or on the server):
```
docker build -t muse_as_servece .
docker run -d --env-file env.list -p 5000:5000 --name muse_as_servece muse_as_servece
```
**Note**: *-p* attribute should be equal to variable *PORT* in [*env.list*](env.list).<br>
**Note**: you can launch service without docker using `python app.py`, but it is preferable to launch service inside docker container.<br>

### Usage
After you create service, you can tokenize and embed any {*sentence*} using GET requests ({*ip*} is address where service was created):
```
http://{ip}:5000/tokenize?sentence={sentence}
http://{ip}:5000/embed?sentence={sentence}
```

You can use python **requests** library to work with GET requests (example [notebook](examples/usage_requests.ipynb)):
```python3
import numpy as np
import requests

ip = "localhost"
port = 5000

sentence = "This is sentence example."

# tokenizer
response = requests.get(
    url=f"http://{ip}:{port}/tokenize",
    params={"sentence": f"{sentence}"},
)
tokenized_sentence = response.json()["content"]

# embedder
response = requests.get(
    url=f"http://{ip}:{port}/embed",
    params={"sentence": f"{sentence}"},
)
embedding = np.array(response.json()["content"][0])

# results
print(tokenized_sentence)  # ['▁This', '▁is', '▁sentence', '▁example', '.']
print(embedding.shape)  # (512,)
```

But it is better to use the built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the **requests** library and provides the user with a simpler interface (example [notebook](examples/usage_client.ipynb)):
```python3
from muse_as_service import MUSEClient

ip = "localhost"
port = 5000

sentence = "This is sentence example."

# init client
client = MUSEClient(
    ip=ip,
    port=port,
)

# tokenizer
tokenized_sentence = client.tokenize(sentence)

# embedder
embedding = client.embed(sentence)

# results
print(tokenized_sentence)  # ['▁This', '▁is', '▁sentence', '▁example', '.']
print(embedding.shape)  # (512,)
```