from flask import Flask
from flask_restful import Api

from muse_embedder.endpoints import Embedder, Tokenizer


def create_app() -> Flask:
    """
    Creape MUSE Rest Api embedder and muse_tokenizer

    :return: flask app
    :rtype: Flask
    """
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Embedder, "/embed")
    api.add_resource(Tokenizer, "/tokenize")

    return app
