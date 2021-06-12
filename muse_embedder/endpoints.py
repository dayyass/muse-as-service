from typing import Dict, Tuple

import numpy as np
import tensorflow_hub as hub
from flask_restful import Resource, reqparse

from muse_embedder.muse_tokenizer.tokenizer import (
    get_tokenizer_from_saved_model,
    parse_saved_model,
    tokenize,
)
from muse_embedder.muse_tokenizer.utils import (
    download_thhub_model,
    get_path_without_extension,
    unpack_tar,
)


class Embedder(Resource):
    """
    MUSE embedder api resource.
    """

    def __init__(
        self,
        embedder_url: str = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
    ) -> None:
        """
        Init Embedder class with tfhub MUSE embedder.
        """

        self.embedder = hub.load(embedder_url)

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
    MUSE tokenizer api resource.
    """

    def __init__(
        self,
        thhub_model_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
        save_model_path=".cache/universal-sentence-encoder-multilingual_3.tar",
    ) -> None:
        """
        Init Tokenizer class with tfhub muse embedder.
        """

        # load and unpack model
        download_thhub_model(
            thhub_model_url=thhub_model_url,
            save_model_path=save_model_path,
        )
        unpack_tar(path=save_model_path)

        # get muse_tokenizer
        self.tokenizer = get_tokenizer_from_saved_model(
            parse_saved_model(get_path_without_extension(save_model_path))
        )

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
