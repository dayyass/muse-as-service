import os
import sys

sys.path.append("../muse_as_service")

from muse_as_service import MUSEClient  # noqa: E402

# params
ip = os.environ["IP"]
port = int(os.environ["PORT"])
token = os.environ["TOKEN"]

# sentence
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


# tests
import numpy as np  # noqa: E402

np.testing.assert_equal(
    tokenized_sentence,
    ["▁This", "▁is", "▁sentence", "▁example", "."],
)
np.testing.assert_equal(
    embedding.shape,
    (512,),
)
