import logging as log

from app.main.model.user import User

from ..util.helper import error_handler

log.basicConfig(level=log.ERROR)

user_model = User()


def register_user(data):
    try:
        result = user_model.register_user(data)
        response_object = {
            "status": "success",
            "message": "Register User Success.",
            "data": result,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Error in register_user: {str(e)}")
        return error_handler(e)


def get_all_users(page, count):
    try:
        users = user_model.get_all_users(page, count)
        if not users:
            return {"status": "success", "message": "No users found", "data": []}, 200

        response_object = {
            "status": "success",
            "message": "Successfully retrieved users.",
            "data": users,
        }
        return response_object, 200
    except Exception as e:
        log.error(f"Error in get user lists: {str(e)}")
        return error_handler(e)


def user_auth(data):
    try:
        auth = user_model.user_auth(data)
        response_object = {
            "status": "success",
            "message": "Login Success",
            "token": auth,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Login Error: {str(e)}")
        return error_handler(e)


def user_auth(data):
    try:
        auth = user_model.user_auth(data)
        response_object = {
            "status": "success",
            "message": "Login Success",
            "token": auth,
        }
        return response_object, 201
    except Exception as e:
        log.error(f"Login Error: {str(e)}")
        return error_handler(e)
