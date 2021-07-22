### Client
MUSE as Service has the following endpoints:
<pre>
- /login          - POST request with `username` and `password` to get tokens (access and refresh)
- /logout         - POST request to remove tokens (access and refresh)
- /token/refresh  - POST request to refresh access token (refresh token required)
- /tokenize       - GET request for `sentence` tokenization (access token required)
- /embed          - GET request for `sentence` embedding (access token required)
</pre>

You can use python **requests** package to work with HTTP requests:
```python3
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
```

However it is better to use built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the python **requests** package and provides user with a simpler interface.

Instead of using endpoints, listed above, directly, **MUSEClient** provides the following methods to work with:
<pre>
- login         - method to login with `username` and `password`
- logout        - method to logout (login required)
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
