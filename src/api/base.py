from functools import wraps
from http import HTTPStatus
from typing import List

from db.controllers.actions import ActionController
from flask_jwt_extended import verify_jwt_in_request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser


class BaseView(Resource):
    PARSER: RequestParser
    FIELDS: list[str] = None

    def __init__(self):
        self.PARSER = RequestParser()
        if self.FIELDS:
            for field in self.FIELDS:
                self.PARSER.add_argument(field)

    @staticmethod
    def get_token(request) -> str:
        token = request.headers.get("Authorization").replace("Bearer ", "")
        return token


def requires_actions(actions: List[str]):
    action_ids = set([action.id for action in ActionController.get_by_names(actions)])

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            _, jwt_data = verify_jwt_in_request()
            if not action_ids.intersection(jwt_data["sub"]["action_ids"]):
                return {"message": "Not authorized"}, HTTPStatus.FORBIDDEN
            return fn(*args, **kwargs)

        return decorator

    return wrapper
