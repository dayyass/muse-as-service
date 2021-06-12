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
You can configure *gunicorn* with [env.list](env.list) file.

To create service use docker container:
```
docker build -t muse_embedder .
docker run -d --env-file env.list -p 5000:5000 --name muse_embedder muse_embedder
```
**Note** *-p* attribute should be equal to variable *PORT* in [env.list](env.list).<br>

### Usage
After you create service, you can tokenize and embed any {sentence} using GET requests:
```
http://{ip}:5000/tokenize?sentence={sentence}
http://{ip}:5000/embed?sentence={sentence}
```

You can use python **requests** library to work with GET requests:
```python3
import requests

ip = "127.0.0.1"
sentence = "This is sentence example."

# tokenizer
response = requests.get(f"http://{ip}:5000/tokenize", params={"sentence": f"{sentence}"})
tokenized_sentence = response.json()["content"]

# embedder
response = requests.get(f"http://{ip}:5000/embed", params={"sentence": f"{sentence}"})
embedding = response.json()["content"]
```
