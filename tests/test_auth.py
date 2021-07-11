import unittest

import flask_testing
import requests
from flask import Flask

from muse_as_service import MUSEClient
from muse_as_service.app import app


class TestAuth(flask_testing.TestCase):
    """
    Class for testing authorization.
    """

    def create_app(self) -> Flask:
        """
        Create Flask app for testing.

        :return: Flask app.
        :rtype: Flask
        """

        app.config["TESTING"] = True
        return app

    def test_requests(self) -> None:
        """
        Testing authorization via requests library.
        """

        # login
        response = self.client.post(
            "/login",
            json={"username": "admin", "password": "admin"},
        )
        access_token = response.json["access_token"]
        refresh_token = response.json["refresh_token"]

        # logout access token
        response = self.client.post(
            "/logout/access",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)

        # token refresh
        response = self.client.post(
            "/token/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        access_token = response.json["access_token"]

        # logout access token
        response = self.client.post(
            "/logout/access",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(response.status_code, 200)

        # logout refresh token
        response = self.client.post(
            "/logout/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        self.assertEqual(response.status_code, 200)

    def test_client(self) -> None:
        """
        Testing authorization usage via built-in client.
        """

        # init client
        client = MUSEClient(ip="localhost", port=5000)

        # login
        client.login(username="admin", password="admin")

        # logout
        client.logout()

    def test_requests_access_denied(self) -> None:
        """
        Testing 401 HTTP error handler via requests library.
        """

        # login
        response_wrong_password = self.client.post(
            "/login",
            json={"username": "admin", "password": "password"},
        )

        response_wrong_username = self.client.post(
            "/login",
            json={"username": "username", "password": "admin"},
        )

        response_wrong_username_and_password = self.client.post(
            "/login",
            json={"username": "username", "password": "password"},
        )

        # tests
        self.assertEqual(response_wrong_password.status_code, 401)
        self.assertEqual(response_wrong_username.status_code, 401)
        self.assertEqual(response_wrong_username_and_password.status_code, 401)

    def test_client_access_denied(self) -> None:
        """
        Testing 401 HTTP error handler via built-in client.
        """

        # init client
        client = MUSEClient(ip="localhost", port=5000)

        # login
        try:
            client.login(username="admin", password="password")
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        try:
            client.login(username="username", password="admin")
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        try:
            client.login(username="username", password="password")
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

    def test_client_errors(self) -> None:
        """
        Testing error handler via built-in client.
        """

        # sentences
        sentences = [
            "This is sentence example.",
            "This is yet another sentence example.",
        ]

        # init client
        client = MUSEClient(ip="localhost", port=5000)

        # logout access token
        try:
            client._logout_access()
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        # logout refresh token
        try:
            client._logout_refresh()
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        # logout
        try:
            client.logout()
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        # token refresh
        try:
            client._token_refresh()
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        # tokenizer
        try:
            client.tokenize(sentences)
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")

        # embedder
        try:
            client.embed(sentences)
        except requests.exceptions.HTTPError:
            pass
        except Exception:
            raise Exception("Something went wrong.")


if __name__ == "__main__":
    unittest.main()
