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

        self._access_token = ""
        self._refresh_token = ""

    def login(self, username: str, password: str) -> None:
        """
        Login to access service for tokenization and embedding.

        :param str username: username.
        :param str password: password.
        """

        response = requests.post(
            url=f"{self.url_service}/login",
            json={"username": username, "password": password},
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))
        else:
            self._access_token = response.json()["access_token"]
            self._refresh_token = response.json()["refresh_token"]

    def _logout_access(self) -> None:
        """
        Logout with access token.
        """

        response = requests.post(
            url=f"{self.url_service}/logout/access",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )

        # JWT access token expiration handler
        if (response.status_code == 401) and (
            response.json()["msg"] == "Token has expired"
        ):
            self._token_refresh()
            return

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))

    def _logout_refresh(self) -> None:
        """
        Logout with refresh token.
        """

        response = requests.post(
            url=f"{self.url_service}/logout/refresh",
            headers={"Authorization": f"Bearer {self._refresh_token}"},
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))

    def logout(self) -> None:
        """
        Logout with access and refresh tokens.
        """

        self._logout_access()
        self._logout_refresh()

    def _token_refresh(self) -> None:
        """
        Refresh access token.
        """

        response = requests.post(
            url=f"{self.url_service}/token/refresh",
            headers={"Authorization": f"Bearer {self._refresh_token}"},
        )

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))
        else:
            self._access_token = response.json()["access_token"]

    def tokenize(self, sentences: List[str]) -> List[List[str]]:
        """
        Sentences tokenization using MUSE.

        :param List[str] sentences: sentences for tokenization.
        :return: tokenized sentences.
        :rtype: List[List[str]]
        """

        response = requests.get(
            url=f"{self.url_service}/tokenize",
            params={"sentence": sentences},
            headers={"Authorization": f"Bearer {self._access_token}"},
        )

        # JWT access token expiration handler
        if (response.status_code == 401) and (
            response.json()["msg"] == "Token has expired"
        ):
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

        response = requests.get(
            url=f"{self.url_service}/embed",
            params={"sentence": sentences},
            headers={"Authorization": f"Bearer {self._access_token}"},
        )

        # JWT access token expiration handler
        if (response.status_code == 401) and (
            response.json()["msg"] == "Token has expired"
        ):
            self._token_refresh()
            return self.embed(sentences)

        if response.status_code != 200:
            raise requests.HTTPError(_http_error_message(response))
        else:
            return np.array(response.json()["embedding"])
