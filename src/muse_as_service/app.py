from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


app.config.from_pyfile("config.py")


db: SQLAlchemy = SQLAlchemy(app)
jwt: JWTManager = JWTManager(app)


from .auth import TokenRefresh, UserLogin, UserLogout  # noqa: E402
from .endpoints import Embedder, Tokenizer  # noqa: E402

# auth
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/token/refresh")


# tokenize and embed
model_path = "models/universal-sentence-encoder-multilingual_3"

api.add_resource(
    Embedder,
    "/embed",
    resource_class_kwargs={"model_path": model_path},
)
api.add_resource(
    Tokenizer,
    "/tokenize",
    resource_class_kwargs={"model_path": model_path},
)
