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
print(
    tokenized_sentence
)  # [["▁This", "▁is", "▁sentence", "▁example", "."], ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]]
print(embedding.shape)  # (2, 512)


# tests
np.testing.assert_equal(
    tokenized_sentence,
    [
        ["▁This", "▁is", "▁sentence", "▁example", "."],
        ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."],
    ],
)
np.testing.assert_equal(
    embedding.shape,
    (2, 512),
)
