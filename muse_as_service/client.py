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
        Init MUSEClient with ip and port.

        :param str token: token for authorization.
        :param str ip: address where service was created (default: "localhost").
        :param int port: port where service launched (default: 5000).
        """

        self.ip = ip
        self.port = port
        self.token = token

        self.url_service = f"http://{self.ip}:{self.port}"
        self.url_tokenize = f"{self.url_service}/tokenize"
        self.url_embed = f"{self.url_service}/embed"

    def tokenize(self, sentence: str) -> List[str]:
        """
        Sentence tokenization using MUSE.

        :param str sentence: sentence for tokenization.
        :return: tokenized sentence.
        :rtype: List[str]
        """

        response = requests.get(
            url=self.url_tokenize,
            params={"token": self.token, "sentence": sentence},
        )

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

        response = requests.get(
            url=self.url_embed,
            params={"token": self.token, "sentence": sentence},
        )

        if response.status_code != 200:
            raise requests.HTTPError(f"{response.status_code}: {response.text}")
        else:
            return np.array(response.json()["embedding"][0])
