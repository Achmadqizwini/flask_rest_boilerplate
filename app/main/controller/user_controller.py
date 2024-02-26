from flask import request
from flask_restx import Resource

from ...extensions import ns
from ..service.user_service import get_all_users, register_user, user_auth
from ..util.dto import UserDto
from ..util.helper import error_handler
from ..util.token_verify import token_required

user_dto = UserDto()
_user = user_dto.user
_login = user_dto.login


@ns.route("/user/signup")
class UserSignUp(Resource):
    @ns.expect(_user, validate=True)
    def post(self):
        """Register a new user"""
        return register_user(ns.payload)


@ns.route("/user")
class UserList(Resource):
    @ns.param("page", "Page of data you want to retrieve")
    @ns.param("count", "How many items you want to include in each page")
    @ns.doc(security="bearer")
    @token_required
    def get(self, decoded_token):
        """List all users"""
        page = request.args.get("page", default=1, type=int)
        count = request.args.get("count", default=50, type=int)
        return get_all_users(page, count)


@ns.route("/user/login")
class UserLogin(Resource):
    @ns.expect(_login, validate=True)
    def post(self):
        """User Authentication"""
        return user_auth(ns.payload)
