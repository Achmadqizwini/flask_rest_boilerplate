from ..util.dto import UserDto
from ..util.helper import error_handler
from flask import request
from flask_restx import Resource
from ..service.user_service import (
    register_user,
    get_all_users,
)
from ...extensions import ns
# from ..util.token_verify import token_required

user_dto = UserDto()
_user = user_dto.user
# _login = user_dto.login

@ns.route("/user/signup")
class UserSignUp(Resource):
    @ns.expect(_user, validate=True)
    def post(self):
        """Register a new user"""
        print("payload: ")
        print(ns.payload)
        print("\n\n================\n\n")
        return register_user(ns.payload)


@ns.route("/user")
class UserList(Resource):
    @ns.param("page", "Page of data you want to retrieve")
    @ns.param("count", "How many items you want to include in each page")
    # @token_required
    def get(self):
        """List all users"""
        page = request.args.get('page', default=1, type=int)
        count = request.args.get('count', default=50, type=int)
        return get_all_users(page, count)

