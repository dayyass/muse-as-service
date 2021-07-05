import unittest
from urllib import parse

import flask_testing
import numpy as np

from muse_as_service import MUSEClient
from muse_as_service.flask_app import create_app as create_app_main
from muse_as_service.utils import download_thhub_model


class TestUsage(flask_testing.TestCase):
    def create_app(self):

        app = create_app_main()
        app.config["TESTING"] = True
        return app

    def setUp(self):

        # load model
        download_thhub_model()

    def test_requests(self):

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

    def test_client(self):

        # sentence
        sentence = "This is sentence example."

        # init client
        client = MUSEClient(
            ip="localhost",
            port=5000,
            token=self.app.token,
        )

        # tokenizer
        client_response = client._tokenizer(sentence)
        query_string = dict(parse.parse_qsl(parse.urlsplit(client_response.url).query))

        response = self.client.get("/tokenize", query_string=query_string)
        tokenized_sentence = response.json["tokens"]

        # embedder
        client_response = client._embedder(sentence)
        query_string = dict(parse.parse_qsl(parse.urlsplit(client_response.url).query))

        response = self.client.get("/embed", query_string=query_string)
        embedding = np.array(response.json["embedding"][0])

        # tests
        self.assertListEqual(
            tokenized_sentence, ["▁This", "▁is", "▁sentence", "▁example", "."]
        )
        self.assertEqual(embedding.shape, (512,))


if __name__ == "__main__":
    unittest.main()
