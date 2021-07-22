import unittest
from typing import List

import flask_testing
import requests
from flask import Flask

from muse_as_service import MUSEClient
from muse_as_service.app import app


class TestAuth(flask_testing.TestCase):
    """
    Class for testing authorization.
    """

    ip = "localhost"
    port = 5000

    def create_app(self) -> Flask:
        """
        Create Flask app for testing.

        :return: Flask app.
        :rtype: Flask
        """

        app.config["TESTING"] = True
        return app

    def exception_block(self, client: MUSEClient, method_name: str, **kwargs) -> None:
        """
        Exception block for errors testing.

        :param MUSEClient client: MUSEClient.
        :param str method_name: method name.
        :param kwargs: kwargs.
        """

        method = getattr(client, method_name)

        try:
            method(**kwargs)
            self.assertTrue(False)
        except requests.exceptions.HTTPError:
            self.assertTrue(True)
        except Exception:
            self.assertTrue(False)

    def _get_cookies_names(self) -> List[str]:
        """
        Helper function to get cookies names.

        :return: cookies names.
        :rtype: List[str]
        """

        return [cookie.name for cookie in self.client.cookie_jar]

    def _get_access_token_cookie(self) -> str:
        """
        Helper function to get access_token_cookie.

        :return: access_token_cookie.
        :rtype: str
        """

        return next(
            (
                cookie.value
                for cookie in self.client.cookie_jar
                if cookie.name == "access_token_cookie"
            )
        )

    def test_requests(self) -> None:
        """
        Testing authorization via requests library.
        """

        cookies = self._get_cookies_names()

        self.assertTrue("access_token_cookie" not in cookies)
        self.assertTrue("refresh_token_cookie" not in cookies)

        # login
        response = self.client.post(
            "/login",
            json={"username": "admin", "password": "admin"},
        )

        cookies = self._get_cookies_names()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token_cookie" in cookies)
        self.assertTrue("refresh_token_cookie" in cookies)

        access_token = self._get_access_token_cookie()

        # token refresh
        response = self.client.post(
            "/token/refresh",
        )

        cookies = self._get_cookies_names()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token_cookie" in cookies)
        self.assertTrue("refresh_token_cookie" in cookies)

        new_access_token = self._get_access_token_cookie()

        self.assertNotEqual(access_token, new_access_token)

        # logout access token
        response = self.client.post(
            "/logout",
        )

        cookies = self._get_cookies_names()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token_cookie" not in cookies)
        self.assertTrue("refresh_token_cookie" not in cookies)

    def test_client(self) -> None:
        """
        Testing authorization usage via built-in client.
        """

        # init client
        client = MUSEClient(ip=self.ip, port=self.port)

        # login
        client.login(username="admin", password="admin")

        # logout
        client.logout()

    def test_requests_access_denied(self) -> None:
        """
        Testing 401 HTTP error handler via requests library.
        """

        # logout
        response_logout_before_login = self.client.post(
            "/logout",
        )

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
        self.assertEqual(response_logout_before_login.status_code, 200)
        self.assertEqual(response_wrong_password.status_code, 401)
        self.assertEqual(response_wrong_username.status_code, 401)
        self.assertEqual(response_wrong_username_and_password.status_code, 401)

    def test_client_access_denied(self) -> None:
        """
        Testing 401 HTTP error handler via built-in client.
        """

        # init client
        client = MUSEClient(ip=self.ip, port=self.port)

        # login
        self.exception_block(
            client, method_name="login", username="admin", password="password"
        )
        self.exception_block(
            client, method_name="login", username="username", password="admin"
        )
        self.exception_block(
            client, method_name="login", username="username", password="password"
        )

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
        client = MUSEClient(ip=self.ip, port=self.port)

        # logout
        client.logout()

        # token refresh
        self.exception_block(client, method_name="_token_refresh")

        # tokenizer
        self.exception_block(client, method_name="tokenize", sentences=sentences)

        # embedder
        self.exception_block(client, method_name="embed", sentences=sentences)


if __name__ == "__main__":
    unittest.main()
