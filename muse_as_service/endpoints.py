import tensorflow_hub as hub
from flask import Response, abort, current_app, jsonify
from flask_restful import Resource, reqparse

from muse_as_service.muse_tokenizer.tokenizer import (
    get_tokenizer_from_saved_model,
    parse_saved_model,
    tokenize,
)


def unauthorized():
    return Response(
        "Access denied! Use token for authorization.",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
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

    def get(self) -> Response:
        """
        GET request method.

        :return: embedding and status code.
        :rtype: Response
        """

        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=str)  # auth
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        if current_app.token != args.token:
            abort(unauthorized())
        else:
            embedding = self.embedder(args["sentence"]).numpy().tolist()
            return jsonify(embedding=embedding)


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
        :rtype: Response
        """

        # add sentence argument
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, type=str)  # auth
        parser.add_argument("sentence", required=True, type=str)
        args = parser.parse_args()

        if current_app.token != args.token:
            abort(unauthorized())
        else:
            tokenized_sentence = tokenize(
                sentence=args["sentence"],
                tokenizer=self.tokenizer,
            )
            return jsonify(tokens=tokenized_sentence)
