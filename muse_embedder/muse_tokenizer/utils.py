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


def unpack_tar(path: str) -> None:
    """
    Unpack .tar file given path.

    :param str path: path to .tar file.
    """

    path_without_extension = get_path_without_extension(path)

    if not path_without_extension.exists():

        # https://stackoverflow.com/questions/6086603/statement-with-and-tarfile
        with closing(tarfile.open(path)) as fp:
            fp.extractall(path_without_extension)


def download_thhub_model(
    thhub_model_url: str,
    save_model_path: str,
) -> None:
    """
    Download th hub model given URL.

    :param str thhub_model_url: tf hub model URL.
    :param str save_model_path: path to save model.
    """

    if not Path(save_model_path).exists():

        # download compressed model
        response = requests.get(f"{thhub_model_url}?tf-hub-format=compressed")

        # make dir if not exists
        # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
        Path(save_model_path).parent.absolute().mkdir(parents=True, exist_ok=True)

        # save compressed model
        with open(save_model_path, mode="wb") as fp:
            fp.write(response.content)
