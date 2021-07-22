import numpy as np
import requests

# params
ip = "localhost"
port = 5000

sentences = ["This is sentence example.", "This is yet another sentence example."]

# start session
session = requests.Session()

# login
response = session.post(
    url=f"http://{ip}:{port}/login",
    json={"username": "admin", "password": "admin"},
)

# tokenizer
response = session.get(
    url=f"http://{ip}:{port}/tokenize",
    params={"sentence": sentences},
)
tokenized_sentence = response.json()["tokens"]

# embedder
response = session.get(
    url=f"http://{ip}:{port}/embed",
    params={"sentence": sentences},
)
embedding = np.array(response.json()["embedding"])

# logout
response = session.post(
    url=f"http://{ip}:{port}/logout",
)

# close session
session.close()

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
