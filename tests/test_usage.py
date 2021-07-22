import unittest

import numpy as np
import requests

from muse_as_service import MUSEClient


class TestUsage(unittest.TestCase):
    """
    Class for testing usage via requests library and built-in client.
    """

    ip = "localhost"
    port = 5000

    sentences = ["This is sentence example.", "This is yet another sentence example."]

    tokenized_sentence_true = [
        ["▁This", "▁is", "▁sentence", "▁example", "."],
        ["▁This", "▁is", "▁yet", "▁another", "▁sentence", "▁example", "."],
    ]
    embedding_true_shape = (2, 512)

    def test_requests(self) -> None:
        """
        Testing usage via requests library.
        """

        # start session
        session = requests.Session()

        # login
        response = session.post(
            f"http://{self.ip}:{self.port}/login",
            json={"username": "admin", "password": "admin"},
        )

        self.assertEqual(response.status_code, 200)

        # tokenizer
        response = session.get(
            f"http://{self.ip}:{self.port}/tokenize",
            params={"sentence": self.sentences},
        )

        self.assertEqual(response.status_code, 200)

        tokenized_sentence_pred = response.json()["tokens"]

        # embedder
        response = session.get(
            f"http://{self.ip}:{self.port}/embed",
            params={"sentence": self.sentences},
        )

        self.assertEqual(response.status_code, 200)

        embedding_pred = np.array(response.json()["embedding"])

        # logout
        response = session.post(
            url=f"http://{self.ip}:{self.port}/logout",
        )

        self.assertEqual(response.status_code, 200)

        # close session
        session.close()

        # tests
        self.assertListEqual(tokenized_sentence_pred, self.tokenized_sentence_true)
        self.assertEqual(embedding_pred.shape, self.embedding_true_shape)

    def test_client(self) -> None:
        """
        Testing usage via built-in client.
        """

        # init client
        client = MUSEClient(ip=self.ip, port=self.port)

        # login
        client.login(username="admin", password="admin")

        # tokenizer
        tokenized_sentence_pred = client.tokenize(self.sentences)

        # embedder
        embedding_pred = client.embed(self.sentences)

        # logout
        client.logout()

        # tests
        self.assertListEqual(tokenized_sentence_pred, self.tokenized_sentence_true)
        self.assertEqual(embedding_pred.shape, self.embedding_true_shape)


if __name__ == "__main__":
    unittest.main()
