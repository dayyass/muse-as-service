import os
import tarfile
from contextlib import closing
from pathlib import Path

import requests


def get_path_without_extension(path: str) -> Path:
    """
    Get path without extension.

    :param str path: path.
    :return: path without extension.
    :rtype: Path
    """

    path = Path(path)  # type: ignore
    return path.parent.joinpath(path.stem)  # type: ignore


def unpack_tar(path: str, remove: bool = True, verbose: bool = True) -> None:
    """
    Unpack .tar file given path and remove.

    :param str path: path to .tar file.
    :param bool remove: remove .tar after unpack.
    :param bool verbose: verbose.
    """

    path_without_extension = get_path_without_extension(path)

    if not path_without_extension.exists():

        if verbose:
            print("unpacking '.tar' model ...")

        # extract tar
        # https://stackoverflow.com/questions/6086603/statement-with-and-tarfile
        with closing(tarfile.open(path)) as fp:
            fp.extractall(path_without_extension)

        if remove:
            # remove tar
            os.remove(path)


def download_thhub_tar_model(
    thhub_model_url: str = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
    save_model_path: str = ".cache/universal-sentence-encoder-multilingual_3",
    verbose: bool = True,
) -> None:
    """
    Download tf hub .tar model given URL.

    :param str thhub_model_url: tf hub model URL.
    :param str save_model_path: path to save model.
    :param bool verbose: verbose.
    """

    save_model_path = save_model_path + ".tar"

    if not Path(save_model_path).exists():

        if verbose:
            print("downloading '.tar' model ...")

        # download compressed model
        response = requests.get(f"{thhub_model_url}?tf-hub-format=compressed")

        # make dir if not exists
        # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
        Path(save_model_path).parent.absolute().mkdir(parents=True, exist_ok=True)

        # save compressed model
        with open(save_model_path, mode="wb") as fp:
            fp.write(response.content)
