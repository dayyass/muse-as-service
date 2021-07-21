from flask import Response, abort, jsonify, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_restful import Resource, reqparse

from muse_as_service.database.database import UserModel


def unauthorized() -> Response:
    """
    401 error handler.

    :return: response.
    :rtype: Response
    """

    response = make_response(jsonify(msg="Unauthorized"), 401)
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

            response = jsonify(message="Logged in")

            # set cookies
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response


class UserLogout(Resource):
    """
    User logout API resource.
    """

    def post(self) -> Response:

        response = jsonify(message="Logged out")
        unset_jwt_cookies(response)

        return response


class TokenRefresh(Resource):
    """
    Token refresh API resource.
    """

    @jwt_required(refresh=True)
    def post(self) -> Response:

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        response = jsonify(message="Access token has been refreshed")

        set_access_cookies(response, access_token)

        return response
