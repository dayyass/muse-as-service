import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY", default=os.urandom(24).hex())
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default=os.urandom(24).hex())

PROPAGATE_EXCEPTIONS = True

SQLALCHEMY_DATABASE_URI = "sqlite:///database/app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False
