import unittest

import requests

from muse_as_service import MUSEClient


class TestAuth(unittest.TestCase):
    """
    Class for testing authorization.
    """

    ip = "localhost"
    port = 5000

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

    def test_requests(self) -> None:
        """
        Testing authorization via requests library.
        """

        # start session
        session = requests.Session()

        self.assertTrue("access_token_cookie" not in session.cookies)
        self.assertTrue("refresh_token_cookie" not in session.cookies)

        # login
        response = session.post(
            url=f"http://{self.ip}:{self.port}/login",
            json={"username": "admin", "password": "admin"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(session.cookies, requests.cookies.RequestsCookieJar)
        self.assertTrue("access_token_cookie" in session.cookies)
        self.assertTrue("refresh_token_cookie" in session.cookies)

        access_token = session.cookies["access_token_cookie"]

        # token refresh
        response = session.post(
            url=f"http://{self.ip}:{self.port}/token/refresh",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token_cookie" in session.cookies)
        self.assertTrue("refresh_token_cookie" in session.cookies)

        new_access_token = session.cookies["access_token_cookie"]

        self.assertNotEqual(access_token, new_access_token)

        # logout access token
        response = session.post(
            url=f"http://{self.ip}:{self.port}/logout",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access_token_cookie" not in session.cookies)
        self.assertTrue("refresh_token_cookie" not in session.cookies)

        # close session
        session.close()

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

        # start session
        session = requests.Session()

        # logout
        response_logout_before_login = session.post(
            url=f"http://{self.ip}:{self.port}/logout",
        )

        # login
        response_wrong_password = session.post(
            url=f"http://{self.ip}:{self.port}/login",
            json={"username": "admin", "password": "password"},
        )

        response_wrong_username = session.post(
            url=f"http://{self.ip}:{self.port}/login",
            json={"username": "username", "password": "admin"},
        )

        response_wrong_username_and_password = session.post(
            url=f"http://{self.ip}:{self.port}/login",
            json={"username": "username", "password": "password"},
        )

        # close session
        session.close()

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
