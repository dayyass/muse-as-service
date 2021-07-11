### Client
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

sentences = ["This is sentence example.", "This is yet another sentence example."]

# login
response = requests.post(
    url=f"http://{ip}:{port}/login",
    json={"username": "admin", "password": "admin"},
)
token = response.json()["access_token"]

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

sentences = ["This is sentence example.", "This is yet another sentence example."]

# init client
client = MUSEClient(ip=ip, port=port)

# login
client.login(username="admin", password="admin")

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
