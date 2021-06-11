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
    """TODO"""

    def __init__(
        self,
        embedder_url: str = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
    ) -> None:
        """
        Init Embedder class with tfhub MUSE embedder.
        """

        self.embedder = hub.load(embedder_url)

    def get(self):
        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        # embed
        embedding = self.embedder(args["sentence"]).numpy().tolist()

        return {"content": embedding}, 200


class Tokenizer(Resource):
    """TODO"""

    def __init__(
        self,
        thhub_model_url="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
        save_model_path=".cache/universal-sentence-encoder-multilingual_3.tar",
    ) -> None:
        """
        Init Embedder class with tfhub muse embedder.
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
        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        # embed
        tokenized_sentence = tokenize(
            sentence=args["sentence"],
            tokenizer=self.tokenizer,
        )

        return {"content": tokenized_sentence}, 200
