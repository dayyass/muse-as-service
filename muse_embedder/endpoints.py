from typing import Dict, Tuple

import numpy as np
import tensorflow_hub as hub
from flask_restful import Resource, reqparse

from muse_embedder.muse_tokenizer.tokenizer import (
    get_tokenizer_from_saved_model,
    parse_saved_model,
    tokenize,
)


class Embedder(Resource):
    """
    MUSE Embedder API resource.
    """

    def __init__(
        self,
        model_path: str = ".cache/universal-sentence-encoder-multilingual_3",
    ) -> None:
        """
        Init Embedder class with tfhub downloaded MUSE model.

        :param str model_path: path to downloaded MUSE model.
        """

        self.embedder = hub.KerasLayer(model_path)

    def get(self) -> Tuple[Dict[str, np.ndarray], int]:
        """
        GET request method.

        :return: embedding and status code.
        :rtype: Tuple[Dict[str, np.ndarray], int]
        """

        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        # embed
        embedding = self.embedder(args["sentence"]).numpy().tolist()

        return {"content": embedding}, 200


class Tokenizer(Resource):
    """
    MUSE Tokenizer API resource.
    """

    def __init__(
        self,
        model_path: str = ".cache/universal-sentence-encoder-multilingual_3",
    ) -> None:
        """
        Init Tokenizer class with tfhub downloaded MUSE model.

        :param str model_path: path to downloaded MUSE model.
        """

        self.tokenizer = get_tokenizer_from_saved_model(parse_saved_model(model_path))

    def get(self):
        """
        GET request method.

        :return: tokenized sentence and status code.
        :rtype: Tuple[Dict[str, np.ndarray], int]
        """

        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        # tokenize
        tokenized_sentence = tokenize(
            sentence=args["sentence"],
            tokenizer=self.tokenizer,
        )

        return {"content": tokenized_sentence}, 200
