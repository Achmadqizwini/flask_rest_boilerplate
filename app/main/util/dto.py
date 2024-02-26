from flask_restx import fields
from app.extensions import api

"""
DTO (Data Transfer Object) is a simple object which is used to pass data between software components.
"""


class UserDto:
    user = api.model(
        "user",
        {
            "username": fields.String(required=True, description="username"),
            "email": fields.String(required=True, description="user email"),
            "password": fields.String(required=True, description="user password"),
        },
    )
    login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email for login"),
            "password": fields.String(
                required=True, description="user password for login"
            ),
        },
    )