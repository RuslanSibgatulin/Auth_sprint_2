from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api

from api.base import BaseView, requires_actions
from db.controllers.actions import ActionController
from db.redis import TokenStorage
from models.actions import Action, ActionCreate

action_blueprint = Blueprint("action", __name__)
api = Api(action_blueprint)


class ActionView(BaseView):
    FIELDS = ["name", "id"]

    @jwt_required()
    @requires_actions(["action_create"])
    def post(self):
        request_args = self.PARSER.parse_args()
        action = ActionCreate.parse_obj(request_args)
        if ActionController.get_by_name(action.name):
            return {"message": "Action already created"}, HTTPStatus.BAD_REQUEST
        action = ActionController.create(action)
        return {"message": "Action created.", "action": action.dict()}, HTTPStatus.CREATED

    @jwt_required()
    @requires_actions(["action_read"])
    def get(self):
        request_args = self.PARSER.parse_args()
        if request_args["id"]:
            action = ActionController.get_by_id(request_args["id"])
            if action:
                return {"action": Action.from_orm(action).dict()}, HTTPStatus.OK
            else:
                return {"message": f"Action with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        elif request_args["name"]:
            action = ActionController.get_by_name(request_args["name"])
            if action:
                return {"action": Action.from_orm(action).dict()}, HTTPStatus.OK
            else:
                return {"message": f"Action with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "You should pass action id or name"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @requires_actions(["action_delete"])
    def delete(self):
        request_args = self.PARSER.parse_args()
        action = ActionController.get_by_id(request_args["id"])
        if not action:
            return {"message": f"Action with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        action = ActionController.delete_role(action)
        return {"message": "Action deleted.", "action": Action.from_orm(action).dict()}, HTTPStatus.OK


class ActionsCheckView(BaseView):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        access_token = self.get_token(request)
        agent = request.user_agent.string
        if TokenStorage().is_valid_token(user_id, agent, access_token):
            return {"actions": identity.get("action_ids")}, HTTPStatus.OK
        else:
            return {"message": "Your token has expired"}, HTTPStatus.BAD_REQUEST


api.add_resource(ActionView, "/v1/access/action")
api.add_resource(ActionsCheckView, "/v1/check/action")
