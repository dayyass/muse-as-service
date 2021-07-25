import unittest

from src.muse_as_service.app import app  # noqa: F401
from src.muse_as_service.database import UserModel


class TestDatabase(unittest.TestCase):
    """
    Class for testing database.
    """

    def test_hash(self) -> None:
        """
        Testing hash verification.
        """

        password = "password"
        password_hash = UserModel.generate_hash(password)

        self.assertTrue(UserModel.verify_hash(password, password_hash))


if __name__ == "__main__":
    unittest.main()
