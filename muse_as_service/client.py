from typing import List

import numpy as np
import requests


class MUSEClient:
    """
    MUSE Client for tokenization and embedding.
    It is wrapper over requests.get method.
    """

    def __init__(self, ip: str = "localhost", port: int = 5000) -> None:
        """
        Init MUSEClient with ip and port.

        :param str ip: address where service was created (default: "localhost").
        :param int port: port where service launched (default: 5000).
        """

        self.ip = ip
        self.port = port

    def tokenize(self, sentence: str) -> List[str]:
        """
        Sentence tokenization using MUSE.

        :param str sentence: sentence for tokenization.
        :return: tokenized sentence.
        :rtype: List[str]
        """

        response = requests.get(
            f"http://{self.ip}:{self.port}/tokenize", params={"sentence": sentence}
        )
        tokenized_sentence = response.json()["content"]
        return tokenized_sentence

    def embed(self, sentence: str) -> np.ndarray:
        """
        Sentence embedding using MUSE.

        :param str sentence: sentence for embedding.
        :return: sentence embedding.
        :rtype: np.ndarray
        """

        response = requests.get(
            f"http://{self.ip}:{self.port}/embed", params={"sentence": sentence}
        )
        embedding = response.json()["content"][0]
        return np.array(embedding)
