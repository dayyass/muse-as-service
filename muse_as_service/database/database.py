from __future__ import annotations

from passlib.hash import pbkdf2_sha256 as sha256

from muse_as_service.app import db


class UserModel(db.Model):
    """
    SQLAlchemy user model.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @staticmethod
    def generate_hash(password: str) -> str:
        """
        Generate hash for password.

        :param str password: password.
        :return: hash.
        :rtype: str
        """

        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        """
        Verify hash given hash and password.

        :param str password: password.
        :param str hash: hash.
        :return: is hash corresponds to password.
        :rtype: bool
        """

        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username: str) -> UserModel:
        """
        Find user in database given username.

        :param str username: username.
        :return: user.
        :rtype: UserModel
        """

        return cls.query.filter_by(username=username).first()


class RevokedTokenModel(db.Model):
    """
    SQLAlchemy model for revoked tokens.
    """

    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self) -> None:
        """
        Add and commit token to database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blocklisted(cls, jti: str) -> bool:
        """
        Check if jti unique identifier of the token in blocklist.

        :param str jti: jti unique identifier of the token.
        :return: is jti in blocklist.
        :rtype: bool
        """

        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
