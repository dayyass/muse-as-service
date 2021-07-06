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

    def _tokenize_url(self, sentences: List[str]) -> str:
        """
        HTTP GET url for tokenization.

        :param List[str] sentences: sentences for tokenization.
        :return: HTTP GET url
        :rtype: str
        """

        request = requests.Request(
            method="GET",
            url=f"{self.url_service}/tokenize",
            params={"token": self.token, "sentence": sentences},
        )
        url = request.prepare().url

        return url  # type: ignore

    def _embed_url(self, sentences: List[str]) -> str:
        """
        HTTP GET url for embedding.

        :param List[str] sentences: sentences for embedding.
        :return: HTTP GET url
        :rtype: str
        """

        request = requests.Request(
            method="GET",
            url=f"{self.url_service}/embed",
            params={"token": self.token, "sentence": sentences},
        )
        url = request.prepare().url

        return url  # type: ignore

    def tokenize(self, sentences: List[str]) -> List[List[str]]:
        """
        Sentences tokenization using MUSE.

        :param List[str] sentences: sentences for tokenization.
        :return: tokenized sentences.
        :rtype: List[List[str]]
        """

        response = requests.get(self._tokenize_url(sentences))

        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}: {response.text}")
        else:
            return response.json()["tokens"]

    def embed(self, sentences: List[str]) -> np.ndarray:
        """
        Sentences embedding using MUSE.

        :param List[str] sentences: sentences for embedding.
        :return: sentences embeddings.
        :rtype: np.ndarray
        """

        response = requests.get(self._embed_url(sentences))

        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}: {response.text}")
        else:
            return np.array(response.json()["embedding"])
