### Client
Built-in client **MUSEClient** for sentence tokenization and embedding, that wraps the functionality of the python **requests** package and provides a user with a simpler interface:
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
