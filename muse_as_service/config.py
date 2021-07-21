import os

SECRET_KEY = os.getenv("SECRET_KEY", default=os.urandom(24).hex())
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default=os.urandom(24).hex())

PROPAGATE_EXCEPTIONS = True

SQLALCHEMY_DATABASE_URI = "sqlite:///database/app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = 86400
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False
JWT_ACCESS_COOKIE_PATH = ["/tokenize", "/embed"]
JWT_REFRESH_COOKIE_PATH = ["/token/refresh"]
