import uuid

from flask import Flask
from flask_restful import Api

from muse_as_service.endpoints import Embedder, Tokenizer


def create_app() -> Flask:
    """
    Creape MUSE RESR API embedder and tokenizer.

    :return: flask app
    :rtype: Flask
    """

    app = Flask(__name__)
    api = Api(app)

    with app.app_context():
        api.add_resource(Embedder, "/embed")
        api.add_resource(Tokenizer, "/tokenize")

    # auth
    app.token = str(uuid.uuid4())
    print(f" * Token: {app.token}")

    return app
