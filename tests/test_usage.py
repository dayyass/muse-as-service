import unittest

import flask_testing
import numpy as np
from flask import Flask

from muse_as_service import MUSEClient
from muse_as_service.app import app


class TestUsage(flask_testing.TestCase):
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

    def create_app(self) -> Flask:
        """
        Create Flask app for testing.

        :return: Flask app.
        :rtype: Flask
        """

        app.config["TESTING"] = True
        return app

    def test_requests(self) -> None:
        """
        Testing usage via requests library.
        """

        # login
        response = self.client.post(
            "/login",
            json={"username": "admin", "password": "admin"},
        )

        self.assertEqual(response.status_code, 200)

        # tokenizer
        response = self.client.get(
            "/tokenize",
            json={"sentence": self.sentences},
        )

        self.assertEqual(response.status_code, 200)

        tokenized_sentence_pred = response.json["tokens"]

        # embedder
        response = self.client.get(
            "/embed",
            json={"sentence": self.sentences},
        )

        self.assertEqual(response.status_code, 200)

        embedding_pred = np.array(response.json["embedding"])

        # logout
        response = self.client.post(
            "/logout",
        )

        self.assertEqual(response.status_code, 200)

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
