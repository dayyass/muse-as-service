import os
import tarfile
from argparse import ArgumentParser
from contextlib import closing
from pathlib import Path

import requests


def get_argparse() -> ArgumentParser:
    """
    Helper function to get ArgumentParser.
    """

    parser = ArgumentParser()

    parser.add_argument(
        "--thhub_model_url",
        type=str,
        required=False,
        default="https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
        help="TF Hub model URL",
    )
    parser.add_argument(
        "--save_model_path",
        type=str,
        required=False,
        default="models/universal-sentence-encoder-multilingual_3",
        help="Path to save model",
    )
    parser.add_argument(
        "--verbose",
        type=bool,
        required=False,
        default=True,
        help="Verbose",
    )

    return parser


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
    thhub_model_url: str, save_model_path: str, verbose: bool = True
) -> None:
    """
    Download TH Hub .tar model given URL.

    :param str thhub_model_url: TF Hub model URL.
    :param str save_model_path: path to save model.
    :param bool verbose: verbose.
    """

    if (
        not Path(save_model_path).exists()
        and not Path(save_model_path + ".tar").exists()
    ):

        if verbose:
            print("downloading '.tar' model ...")

        # download compressed model
        response = requests.get(f"{thhub_model_url}?tf-hub-format=compressed")

        # make dir if not exists
        # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
        Path(save_model_path).parent.absolute().mkdir(parents=True, exist_ok=True)

        # save compressed model
        with open(save_model_path + ".tar", mode="wb") as fp:
            fp.write(response.content)


def download_thhub_model(
    thhub_model_url: str, save_model_path: str, verbose: bool = True
) -> None:
    """
    Download TF Hub .tar model given URL and unpack it.

    :param str thhub_model_url: TF Hub model URL.
    :param str save_model_path: path to save model.
    :param bool verbose: verbose.
    """

    download_thhub_tar_model(
        thhub_model_url=thhub_model_url,
        save_model_path=save_model_path,
        verbose=verbose,
    )
    unpack_tar(path=save_model_path + ".tar", remove=True, verbose=verbose)  # hardcode


if __name__ == "__main__":

    # argparse
    parser = get_argparse()
    args = parser.parse_args()

    # download
    download_thhub_model(
        thhub_model_url=args.thhub_model_url,
        save_model_path=args.save_model_path,
        verbose=args.verbose,
    )
