import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config.from_json("config.json")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]


db: SQLAlchemy = SQLAlchemy(app)
jwt: JWTManager = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return RevokedTokenModel.is_jti_blocklisted(jti)


from muse_as_service.auth import (  # noqa: E402
    TokenRefresh,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh,
)
from muse_as_service.database import RevokedTokenModel  # noqa: E402
from muse_as_service.endpoints import Embedder, Tokenizer  # noqa: E402

# auth
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogoutAccess, "/logout/access")
api.add_resource(UserLogoutRefresh, "/logout/refresh")
api.add_resource(TokenRefresh, "/token/refresh")


# tokenize and embed
api.add_resource(Embedder, "/embed")
api.add_resource(Tokenizer, "/tokenize")
