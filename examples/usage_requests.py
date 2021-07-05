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


# tests
np.testing.assert_equal(
    tokenized_sentence,
    ["▁This", "▁is", "▁sentence", "▁example", "."],
)
np.testing.assert_equal(
    embedding.shape,
    (512,),
)
