import uuid

from flask import Flask
from flask_restful import Api

from muse_as_service.client import MUSEClient  # noqa: F401
from muse_as_service.endpoints import Embedder, Tokenizer
from muse_as_service.utils import get_argparse  # noqa: F401
from muse_as_service.utils import download_thhub_tar_model, unpack_tar


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

    return app


def download_thhub_model(
    thhub_model_url: str = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
    save_model_path: str = ".cache/universal-sentence-encoder-multilingual_3",
    verbose: bool = True,
) -> None:
    """
    Download tf hub .tar model given URL and unpack it.

    :param str thhub_model_url: tf hub model URL.
    :param str save_model_path: path to save model.
    :param bool verbose: verbose.
    """

    download_thhub_tar_model(
        thhub_model_url=thhub_model_url,
        save_model_path=save_model_path,
        verbose=verbose,
    )
    unpack_tar(path=save_model_path + ".tar", remove=True, verbose=verbose)  # hardcode
