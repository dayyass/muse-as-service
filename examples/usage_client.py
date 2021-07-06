import os
import sys

sys.path.append("../muse_as_service")

from muse_as_service import MUSEClient  # noqa: E402

# params
ip = os.environ["IP"]
port = int(os.environ["PORT"])
token = os.environ["TOKEN"]

# sentences
sentences = ["This is sentence example.", "This is yet another sentence example."]

# init client
client = MUSEClient(
    ip=ip,
    port=port,
    token=token,
)

# tokenizer
tokenized_sentence = client.tokenize(sentences)

# embedder
embedding = client.embed(sentences)

# results
print(
    tokenized_sentence
)  # [["▁This", "▁is", "▁sentence", "▁example", "."], ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."]]
print(embedding.shape)  # (2, 512)


# tests
import numpy as np  # noqa: E402

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
