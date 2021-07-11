import tensorflow_hub as hub
from flask import Response, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from muse_as_service.tokenizer.tokenizer import (
    get_tokenizer_from_saved_model,
    parse_saved_model,
    tokenize,
)


def get_sentence_parser() -> reqparse.RequestParser:
    """
    Get request parser.

    :return: request parser.
    :rtype: reqparse.RequestParser
    """

    parser = reqparse.RequestParser()

    parser.add_argument(
        "sentence",
        type=str,
        action="append",
        required=True,
        help="This field cannot be blank",
    )

    return parser


class Embedder(Resource):
    """
    MUSE Embedder API resource.
    """

    def __init__(self, model_path: str) -> None:
        """
        Init Embedder class with tfhub downloaded MUSE model.

        :param str model_path: path to downloaded MUSE model.
        """

        self.embedder = hub.KerasLayer(model_path)

    @jwt_required()
    def get(self) -> Response:
        """
        GET request method.

        :return: embedding and status code.
        :rtype: Response
        """

        parser = get_sentence_parser()
        args = parser.parse_args()

        embedding = self.embedder(args["sentence"]).numpy().tolist()
        return jsonify(embedding=embedding)


class Tokenizer(Resource):
    """
    MUSE Tokenizer API resource.
    """

    def __init__(self, model_path: str) -> None:
        """
        Init Tokenizer class with tfhub downloaded MUSE model.

        :param str model_path: path to downloaded MUSE model.
        """

        self.tokenizer = get_tokenizer_from_saved_model(parse_saved_model(model_path))

    @jwt_required()
    def get(self) -> Response:
        """
        GET request method.

        :return: tokenized sentence and status code.
        :rtype: Response
        """

        parser = get_sentence_parser()
        args = parser.parse_args()

        tokenized_sentence = tokenize(
            sentences=args["sentence"],
            tokenizer=self.tokenizer,
        )
        return jsonify(tokens=tokenized_sentence)
