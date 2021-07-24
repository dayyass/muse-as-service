from typing import List

import numpy as np
import requests
from requests import Response


def _http_error_message(response: Response) -> str:
    """
    Helper function to make requests.HTTPError message.

    :param Response response: HTTP response.
    :return: requests.HTTPError message.
    :rtype: str
    """

    return f"{response.status_code}: {response.json()['msg']}"


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
        self.url_service = f"http://{self.ip}:{self.port}"

        self.session = requests.Session()

    def login(self, username: str, password: str) -> None:
        """
        Login to access service for tokenization and embedding.

        :param str username: username.
        :param str password: password.
        """

        response = self.session.post(
            url=f"{self.url_service}/login",
            json={"username": username, "password": password},
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))

    def logout(self) -> None:
        """
        Logout with access and refresh tokens.
        """

        response = self.session.post(
            url=f"{self.url_service}/logout",
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))

    def _token_refresh(self) -> None:
        """
        Refresh access token.
        """

        response = self.session.post(
            url=f"{self.url_service}/token/refresh",
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))

    def tokenize(self, sentences: List[str]) -> List[List[str]]:
        """
        Sentences tokenization using MUSE.

        :param List[str] sentences: sentences for tokenization.
        :return: tokenized sentences.
        :rtype: List[List[str]]
        """

        response = self.session.get(
            url=f"{self.url_service}/tokenize",
            params={"sentence": sentences},
        )

        # JWT access token expiration handler
        if (response.status_code == 401) and (
            response.json()["msg"] == "Token has expired"
        ):
            print("JWT access token has expired. Reissue access token.")
            self._token_refresh()
            return self.tokenize(sentences)

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))
        else:
            return response.json()["tokens"]

    def embed(self, sentences: List[str]) -> np.ndarray:
        """
        Sentences embedding using MUSE.

        :param List[str] sentences: sentences for embedding.
        :return: sentences embeddings.
        :rtype: np.ndarray
        """

        response = self.session.get(
            url=f"{self.url_service}/embed",
            params={"sentence": sentences},
        )

        # JWT access token expiration handler
        if (response.status_code == 401) and (
            response.json()["msg"] == "Token has expired"
        ):
            print("JWT access token has expired. Reissue access token.")
            self._token_refresh()
            return self.embed(sentences)

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))
        else:
            return np.array(response.json()["embedding"])
