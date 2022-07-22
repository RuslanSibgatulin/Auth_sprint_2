from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api

from api.base import BaseView, requires_actions
from db.controllers.actions import ActionController
from models.actions import Action, ActionCreate

action_blueprint = Blueprint("action", __name__)
api = Api(action_blueprint)


class ActionView(BaseView):
    FIELDS = ["name", "id"]

    @jwt_required()
    @requires_actions(["action_create"])
    def post(self):
        """Add a new action.
        ---
        tags:
          - action
        parameters:
          - name: name
            in: body
            type: string
            required: true
        security:
          - bearerAuth: []
        responses:
          201:
            description: Action added
            schema:
              type: object
              properties:
                message:
                  type: string
                action:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
          400:
            description: Action already created
            schema:
              type: object
              properties:
                message:
                  type: string
          401:
            description: Unauthorized
            schema:
              type: object
              properties:
                message:
                  type: string
        """
        request_args = self.PARSER.parse_args()
        action = ActionCreate.parse_obj(request_args)
        if ActionController.get_by_name(action.name):
            return {"message": "Action already created"}, HTTPStatus.BAD_REQUEST
        action = ActionController.create(action)
        return {"message": "Action created.", "action": action.dict()}, HTTPStatus.CREATED

    @jwt_required()
    @requires_actions(["action_read"])
    def get(self):
        """Read an action.
        ---
        tags:
          - action
        parameters:
          - name: id
            in: query
            type: string
          - name: name
            in: query
            type: string
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          Action:
            type: object
            properties:
              action:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
        responses:
          200:
            description: Get action
            schema:
              $ref: '#/definitions/Action'
          400:
            description: Missing parameters
            schema:
              $ref: '#/definitions/Message'
          401:
            description: Unauthorized
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Not found
            schema:
              $ref: '#/definitions/Message'
        """
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
        """Delete an action.
        ---
        tags:
          - action
        parameters:
          - name: id
            in: query
            type: string
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          Action:
            type: object
            properties:
              action:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
        responses:
          200:
            description: Get action
            schema:
              type: object
              properties:
                message:
                  type: string
                action:
                  $ref: '#/definitions/Action'
          401:
            description: Unauthorized
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Not found
            schema:
              $ref: '#/definitions/Action'
        """
        request_args = self.PARSER.parse_args()
        action = ActionController.get_by_id(request_args["id"])
        if not action:
            return {"message": f"Action with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        action = ActionController.delete_role(action)
        return {"message": "Action deleted.", "action": Action.from_orm(action).dict()}, HTTPStatus.OK


api.add_resource(ActionView, "/v1/access/action")
