import unittest

import flask_testing
import numpy as np
from flask import Flask

from muse_as_service.app import app


class TestUsage(flask_testing.TestCase):
    """
    Class for testing usage via requests library and built-in client.
    """

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

        query_string = {"sentence": self.sentences}

        # login
        response = self.client.post(
            "/login",
            data={"username": "admin", "password": "admin"},
        )
        token = response.json["access_token"]

        # tokenizer
        response = self.client.get(
            "/tokenize",
            query_string=query_string,
            headers={"Authorization": f"Bearer {token}"},
        )
        tokenized_sentence_pred = response.json["tokens"]

        # embedder
        response = self.client.get(
            "/embed",
            query_string=query_string,
            headers={"Authorization": f"Bearer {token}"},
        )
        embedding_pred = np.array(response.json["embedding"])

        # tests
        self.assertListEqual(tokenized_sentence_pred, self.tokenized_sentence_true)
        self.assertEqual(embedding_pred.shape, self.embedding_true_shape)


if __name__ == "__main__":
    unittest.main()
