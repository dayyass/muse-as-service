import unittest
from typing import Dict
from urllib import parse

import flask_testing
import numpy as np
from flask import Flask

from muse_as_service import MUSEClient
from muse_as_service.flask_app import create_app as create_app_main
from muse_as_service.utils import download_thhub_model


def parse_get_request_url(url: str) -> Dict:
    """
    Helper function to parse GET request URL.

    :param str url: GET request URL
    :return: query parameters.
    :rtype: Dict
    """

    query_params = {"token": "", "sentence": []}

    query = parse.urlsplit(url).query
    for param in query.split("&"):
        name, value = param.split("=")

        if name == "token":
            query_params["token"] = value
        elif name == "sentence":
            query_params["sentence"].append(value.replace("+", " "))  # type: ignore
        else:
            raise KeyError(f"Unknown query parameter {name}.")

    return query_params


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

        query_string = {"token": self.app.token, "sentence": self.sentences}

        # tokenizer
        response = self.client.get("/tokenize", query_string=query_string)
        tokenized_sentence_pred = response.json["tokens"]

        # embedder
        response = self.client.get("/embed", query_string=query_string)
        embedding_pred = np.array(response.json["embedding"])

        # tests
        self.assertListEqual(tokenized_sentence_pred, self.tokenized_sentence_true)
        self.assertEqual(embedding_pred.shape, self.embedding_true_shape)

    def test_client(self) -> None:
        """
        Testing usage via built-in client.
        """

        # init client
        client = MUSEClient(
            ip="localhost",
            port=5000,
            token=self.app.token,
        )

        # tokenizer
        tokenize_url = client._tokenize_url(self.sentences)
        query_string = parse_get_request_url(tokenize_url)

        response = self.client.get("/tokenize", query_string=query_string)
        tokenized_sentence_pred = response.json["tokens"]

        # embedder
        embed_url = client._embed_url(self.sentences)
        query_string = parse_get_request_url(embed_url)

        response = self.client.get("/embed", query_string=query_string)
        embedding_pred = np.array(response.json["embedding"])

        # tests
        self.assertListEqual(tokenized_sentence_pred, self.tokenized_sentence_true)
        self.assertEqual(embedding_pred.shape, self.embedding_true_shape)


if __name__ == "__main__":
    unittest.main()
