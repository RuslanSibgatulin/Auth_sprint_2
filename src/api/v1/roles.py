from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api

from api.base import BaseView, requires_actions
from db.controllers.actions import ActionController
from db.controllers.exceptions import AlreadyExistsError, NotFoundError
from db.controllers.role_assignment import UserRoleController
from db.controllers.roles import RoleController
from models.roles import Role, RoleCreate
from models.user_role import UserRoleCreate, UserRoleDelete

role_blueprint = Blueprint("role", __name__)
api = Api(role_blueprint)


class RoleView(BaseView):
    FIELDS = ["name", "actions", "id"]

    @jwt_required()
    @requires_actions(["role_create"])
    def post(self):
        """Add a new role.
        ---
        tags:
          - role
        parameters:
          - name: actions
            in: body
            type: string
            required: true
            default: action1,action2,action3
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          Role:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              actions:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
        responses:
          200:
            description: Role added
            schema:
              type: object
              properties:
                message:
                  type: string
                role:
                  $ref: '#/definitions/Role'
          400:
            description: Role already created
            schema:
              $ref: '#/definitions/Message'
          401:
            description: Unauthorized
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        if request_args["actions"]:
            request_args["actions"] = request_args["actions"].split(",")
        role = RoleCreate.parse_obj(request_args)

        if RoleController.get_by_name(role.name):
            return {"message": f"Role {role.name} already exists"}, HTTPStatus.BAD_REQUEST

        actions = ActionController.get_by_names(role.actions)
        if len(actions) != len(role.actions):
            missing = set(role.actions) ^ set(action.name for action in actions)
            missing = ",".join(sorted(missing))
            return {"message": f"Unknown actions: {missing}"}, HTTPStatus.BAD_REQUEST

        role.actions = actions
        role = RoleController.create(role)
        return {"message": "Role created.", "role": role.dict()}, HTTPStatus.CREATED

    @jwt_required()
    @requires_actions(["role_read"])
    def get(self):
        """Read a role.
        ---
        tags:
          - role
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
          Role:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              actions:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
        responses:
          200:
            description: Role read
            schema:
              $ref: '#/definitions/Role'
          400:
            description: Missing parameters
            schema:
              $ref: '#/definitions/Message'
          404:
            description: Not found
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        if request_args["id"]:
            role = RoleController.get_by_id(request_args["id"])
            if role:
                return {"role": Role.from_orm(role).dict()}, HTTPStatus.OK
            else:
                return {"message": f"Role with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        elif request_args["name"]:
            role = RoleController.get_by_name(request_args["name"])
            if role:
                return {"role": Role.from_orm(role).dict()}, HTTPStatus.OK
            else:
                return {"message": f"Role with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        else:
            return {"message": "You should pass role id or name"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    @requires_actions(["role_update"])
    def put(self):
        """Update a role.
        ---
        tags:
          - role
        parameters:
          - name: id
            in: query
            type: string
          - name: name
            in: query
            type: string
          - name: actions
            in: query
            type: string
            default: action1,action2,action3
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          Role:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              actions:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
        responses:
          202:
            description: Role updated
            schema:
              type: object
              properties:
                message:
                  type: string
                role:
                  $ref: '#/definitions/Role'
          400:
            description: Missing parameters
            schema:
              $ref: '#/definitions/Message'
          404:
            description: Not found
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        role = RoleController.get_by_id(request_args["id"])
        if not role:
            return {"message": f"Role with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        if request_args["actions"]:
            actions = request_args["actions"].split(",")
            request_args["actions"] = ActionController.get_by_names(actions)
            if len(request_args["actions"]) != len(actions):
                missing = set(actions) ^ set(action.name for action in request_args["actions"])
                missing = ",".join(sorted(missing))
                return {"message": f"Unknown actions: {missing}"}, HTTPStatus.BAD_REQUEST
        updated_role = RoleController.update_role(role, request_args["name"], request_args["actions"])
        return {"message": "Role updated.", "role": Role.from_orm(updated_role).dict()}, HTTPStatus.ACCEPTED

    @jwt_required()
    @requires_actions(["role_delete"])
    def delete(self):
        """Delete a role.
        ---
        tags:
          - role
        parameters:
          - name: id
            in: query
            type: string
            required: true
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          Role:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              actions:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
        responses:
          200:
            description: Role deleted
            schema:
              type: object
              properties:
                message:
                  type: string
                role:
                  $ref: '#/definitions/Role'
          400:
            description: Missing parameters
            schema:
              $ref: '#/definitions/Message'
          404:
            description: Not found
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        role = RoleController.get_by_id(request_args["id"])
        if not role:
            return {"message": f"Role with id {request_args['id']} not found"}, HTTPStatus.NOT_FOUND
        role = RoleController.delete_role(role)
        return {"message": "Role deleted.", "role": Role.from_orm(role).dict()}, HTTPStatus.OK


class RoleAssignmentView(BaseView):
    FIELDS = ["role_id", "user_id"]

    @jwt_required()
    @requires_actions(["role_assignment_create"])
    def post(self):
        """Assign a role to a user.
        ---
        tags:
          - role assignment
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
          - name: role_id
            in: query
            type: integer
            required: true
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          UserRole:
            type: object
            properties:
              user_id:
                type: integer
              role_id:
                type: integer
        responses:
          201:
            description: Role assigned
            schema:
              type: object
              properties:
                message:
                  type: string
                user_role:
                  $ref: '#/definitions/UserRole'
          400:
            description: Assignment already created
            schema:
              type: object
              properties:
                message:
                  type: string
                user_role:
                  $ref: '#/definitions/UserRole'
          401:
            description: Unauthorized
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        user_role = UserRoleCreate.parse_obj(request_args)
        try:
            user_role = UserRoleController.create(user_role)
        except AlreadyExistsError:
            user_role.user_id = str(user_role.user_id)
            return {"message": "Assignment already exists", "user_role": user_role.dict()}, HTTPStatus.BAD_REQUEST

        user_role.user_id = str(user_role.user_id)
        return {"message": "Role assigned to user.", "user_role": user_role.dict()}, HTTPStatus.CREATED

    @jwt_required()
    @requires_actions(["role_assignment_delete"])
    def delete(self):
        """Retract a role from a user.
        ---
        tags:
          - role assignment
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
          - name: role_id
            in: query
            type: integer
            required: true
        security:
          - bearerAuth: []
        definitions:
          Message:
            type: object
            properties:
              message:
                type: string
          UserRole:
            type: object
            properties:
              user_id:
                type: integer
              role_id:
                type: integer
        responses:
          202:
            description: Role assigned
            schema:
              type: object
              properties:
                message:
                  type: string
                user_role:
                  $ref: '#/definitions/UserRole'
          400:
            description: Assignment already created
            schema:
              type: object
              properties:
                message:
                  type: string
                user_role:
                  $ref: '#/definitions/UserRole'
          401:
            description: Unauthorized
            schema:
              $ref: '#/definitions/Message'
        """
        request_args = self.PARSER.parse_args()
        user_role = UserRoleDelete.parse_obj(request_args)
        try:
            user_role = UserRoleController.remove(user_role)
        except NotFoundError:
            user_role.user_id = str(user_role.user_id)
            return {"message": "Role not assigned to user", "user_role": user_role.dict()}, HTTPStatus.BAD_REQUEST

        user_role.user_id = str(user_role.user_id)
        return {"message": "Role removed from user.", "user_role": user_role.dict()}, HTTPStatus.ACCEPTED


api.add_resource(RoleView, "/v1/access/role")
api.add_resource(RoleAssignmentView, "/v1/access/assign")
