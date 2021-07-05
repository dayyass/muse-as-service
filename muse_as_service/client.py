from typing import List

import numpy as np
import requests


class MUSEClient:
    """
    MUSE Client for tokenization and embedding.
    It is wrapper over requests.get method.
    """

    def __init__(self, token: str, ip: str = "localhost", port: int = 5000) -> None:
        """
        Init MUSEClient with token, ip and port.

        :param str token: token for authorization.
        :param str ip: address where service was created (default: "localhost").
        :param int port: port where service launched (default: 5000).
        """

        self.ip = ip
        self.port = port
        self.token = token

        self.url_service = f"http://{self.ip}:{self.port}"

    def _tokenize_url(self, sentence: str) -> str:
        """
        HTTP GET url for tokenization.

        :param str sentence: sentence for tokenization.
        :return: HTTP GET url
        :rtype: str
        """

        request = requests.Request(
            method="GET",
            url=f"{self.url_service}/tokenize",
            params={"token": self.token, "sentence": f"{sentence}"},
        )
        url = request.prepare().url

        return url  # type: ignore

    def _embed_url(self, sentence: str) -> str:
        """
        HTTP GET url for embedding.

        :param str sentence: sentence for embedding.
        :return: HTTP GET url
        :rtype: str
        """

        request = requests.Request(
            method="GET",
            url=f"{self.url_service}/embed",
            params={"token": self.token, "sentence": f"{sentence}"},
        )
        url = request.prepare().url

        return url  # type: ignore

    def tokenize(self, sentence: str) -> List[str]:
        """
        Sentence tokenization using MUSE.

        :param str sentence: sentence for tokenization.
        :return: tokenized sentence.
        :rtype: List[str]
        """

        response = requests.get(self._tokenize_url(sentence))

        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}: {response.text}")
        else:
            return response.json()["tokens"]

    def embed(self, sentence: str) -> np.ndarray:
        """
        Sentence embedding using MUSE.

        :param str sentence: sentence for embedding.
        :return: sentence embedding.
        :rtype: np.ndarray
        """

        response = requests.get(self._embed_url(sentence))

        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}: {response.text}")
        else:
            return np.array(response.json()["embedding"][0])
