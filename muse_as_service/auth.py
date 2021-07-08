from flask import Response, abort, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource, reqparse

from muse_as_service.database import RevokedTokenModel, UserModel


def unauthorized() -> Response:
    """
    401 error handler.

    :return: response.
    :rtype: Response
    """

    response = make_response(jsonify(message="Access denied!"), 401)
    response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'

    return response


def get_auth_parser() -> reqparse.RequestParser:
    """
    Get request parser.

    :return: request parser.
    :rtype: reqparse.RequestParser
    """

    parser = reqparse.RequestParser()

    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank"
    )

    return parser


class UserLogin(Resource):
    """
    User login API resource.
    """

    def post(self) -> Response:

        parser = get_auth_parser()
        args = parser.parse_args()

        current_user = UserModel.find_by_username(args["username"])

        if not current_user:
            abort(unauthorized())

        if not UserModel.verify_hash(args["password"], current_user.password):
            abort(unauthorized())
        else:
            access_token = create_access_token(identity=args["username"])
            refresh_token = create_refresh_token(identity=args["username"])

            return jsonify(
                message=f"Logged in as {current_user.username}",
                access_token=access_token,
                refresh_token=refresh_token,
            )


class UserLogoutAccess(Resource):
    """
    User logout API resource.
    """

    @jwt_required()
    def post(self) -> Response:

        jti = get_jwt()["jti"]

        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()

        return jsonify(message="Access token has been revoked")


class UserLogoutRefresh(Resource):
    """
    User logout API resource.
    """

    @jwt_required(refresh=True)
    def post(self) -> Response:

        jti = get_jwt()["jti"]

        revoked_token = RevokedTokenModel(jti=jti)
        revoked_token.add()

        return jsonify(message="Refresh token has been revoked")


class TokenRefresh(Resource):
    """
    Token refresh API resource.
    """

    @jwt_required(refresh=True)
    def post(self) -> Response:

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        return jsonify(
            message="Access token has been refreshed", access_token=access_token
        )
