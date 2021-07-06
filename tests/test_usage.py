import unittest
from urllib import parse

import flask_testing
import numpy as np
from flask import Flask

from muse_as_service import MUSEClient
from muse_as_service.flask_app import create_app as create_app_main
from muse_as_service.utils import download_thhub_model


class TestUsage(flask_testing.TestCase):
    """
    Class for testing usage via requests library and built-in client.
    """

    def create_app(self) -> Flask:
        """
        Create Flask app for testing.

        :return: Flask app.
        :rtype: Flask
        """

        app = create_app_main()
        app.config["TESTING"] = True
        return app

    def setUp(self) -> None:
        """
        SetUp tests with downloading MUSE model.
        """

        # load model
        download_thhub_model()

    def test_requests(self) -> None:
        """
        Testing usage via requests library.
        """

        # sentence
        sentence = "This is sentence example."
        query_string = {"token": self.app.token, "sentence": sentence}

        # tokenizer
        response = self.client.get("/tokenize", query_string=query_string)
        tokenized_sentence = response.json["tokens"]

        # embedder
        response = self.client.get("/embed", query_string=query_string)
        embedding = np.array(response.json["embedding"][0])

        # tests
        self.assertListEqual(
            tokenized_sentence, ["▁This", "▁is", "▁sentence", "▁example", "."]
        )
        self.assertEqual(embedding.shape, (512,))

    def test_client(self) -> None:
        """
        Testing usage via built-in client.
        """

        # sentence
        sentence = "This is sentence example."

        # init client
        client = MUSEClient(
            ip="localhost",
            port=5000,
            token=self.app.token,
        )

        # tokenizer
        tokenize_url = client._tokenize_url(sentence)
        query_string = dict(parse.parse_qsl(parse.urlsplit(tokenize_url).query))

        response = self.client.get("/tokenize", query_string=query_string)
        tokenized_sentence = response.json["tokens"]

        # embedder
        embed_url = client._embed_url(sentence)
        query_string = dict(parse.parse_qsl(parse.urlsplit(embed_url).query))

        response = self.client.get("/embed", query_string=query_string)
        embedding = np.array(response.json["embedding"][0])

        # tests
        self.assertListEqual(
            tokenized_sentence, ["▁This", "▁is", "▁sentence", "▁example", "."]
        )
        self.assertEqual(embedding.shape, (512,))


if __name__ == "__main__":
    unittest.main()
