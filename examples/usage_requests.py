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
