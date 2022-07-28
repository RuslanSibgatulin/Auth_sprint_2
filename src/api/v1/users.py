from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Api
from sqlalchemy.exc import IntegrityError

from api.base import BaseView
from db.controllers.users import UserController
from db.redis import TokenStorage
from models.users import CreateUser
from utils import CreationError, PasswordHasher, TokenMaker

user_blueprint = Blueprint("user", __name__)
api = Api(user_blueprint)


class UserCreationView(BaseView):
    FIELDS = ["login", "email", "password", "second_password"]

    def post(self):
        request_args = self.PARSER.parse_args()
        try:
            user = CreateUser.parse_obj(request_args)
        except CreationError:
            return {"message": "Error! Check your passwords."}, HTTPStatus.BAD_REQUEST
        try:
            UserController().create(user.get_payload())
        except IntegrityError as e:
            message = e.args[0]
            if "login" in message:
                return {
                    "message": f"Error! User with login - {getattr(user, 'login')} already exists."
                }, HTTPStatus.BAD_REQUEST
            elif "email" in message:
                return {
                    "message": f"Error! User with email - {getattr(user, 'email')} already exists."
                }, HTTPStatus.BAD_REQUEST
            else:
                return {"message": "Error! Something wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {"message": "User created."}, HTTPStatus.CREATED


class UserLoginView(BaseView):
    FIELDS = ["login", "password"]

    def post(self):
        request_args = self.PARSER.parse_args()
        login = request_args.get("login")
        controller = UserController()
        user = controller.get_by_login(login)
        if not user:
            return {"message": f"User with login {login} does't exists."}, HTTPStatus.NOT_FOUND
        correct_password = PasswordHasher.check_password(request_args.get("password"), user.password_hash)
        if not correct_password:
            return {"message": "Wrong password"}, HTTPStatus.UNAUTHORIZED
        agent = request.user_agent
        access_token, refresh_token = TokenMaker.create_tokens_pair(user)
        TokenStorage().add_token_pair(
            user_id=user.id, user_agent=agent.string, refresh_token=refresh_token, access_token=access_token
        )
        controller.add_login_record(dict(user_id=user.id, platform=agent.platform, ip=request.remote_addr))
        return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK


class UserRefreshView(BaseView):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        refresh_token = self.get_token(request)
        user = UserController().get_by_id(user_id)
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        agent = request.user_agent.string
        token_storage = TokenStorage()
        if token_storage.is_valid_token(user_id, agent, refresh_token, True):
            access_token, refresh_token = TokenMaker.create_tokens_pair(user)
            token_storage.add_token_pair(
                user_id=user_id, user_agent=agent, refresh_token=refresh_token, access_token=access_token
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK
        else:
            return {"message": "Refresh token has expired. Login again."}, HTTPStatus.BAD_REQUEST


class UserHistoryView(BaseView):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        access_token = self.get_token(request)
        token_storage = TokenStorage()
        agent = request.user_agent.string
        if token_storage.is_valid_token(user_id, agent, access_token):
            page = request.args.get("page") or 1
            limit = request.args.get("limit") or 10
            skip = (int(page) - 1) * int(limit)
            controller = UserController()
            logins = controller.get_user_history(user_id, skip=skip, limit=int(limit))
            return {"page": page, "size": limit, "logins": logins}, HTTPStatus.OK
        else:
            return {"message": "Refresh your access token."}, HTTPStatus.BAD_REQUEST


class UserLogoutView(BaseView):
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        agent = request.user_agent.string
        access_token = self.get_token(request)
        token_storage = TokenStorage()
        if not token_storage.is_valid_token(user_id, agent, access_token):
            return {"message": "Refresh your access token."}, HTTPStatus.BAD_REQUEST
        token_storage.delete_user_token_pair(user_id, agent)
        return {"message": "You logged out."}, HTTPStatus.OK


class UserLogoutAllView(BaseView):
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        access_token = self.get_token(request)
        agent = request.user_agent.string
        token_storage = TokenStorage()
        if not token_storage.is_valid_token(user_id, agent, access_token):
            return {"message": "Refresh your access token."}, HTTPStatus.BAD_REQUEST
        token_storage.delete_all_user_tokens(user_id)
        return {"message": "You logged out."}, HTTPStatus.OK


class UserChangeView(BaseView):
    FIELDS = ["login", "password", "old_password"]

    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        user_id = identity.get("user_id")
        token_storage = TokenStorage()
        access_token = self.get_token(request)
        agent = request.user_agent.string
        if not token_storage.is_valid_token(user_id, agent, access_token):
            return {"message": "Refresh your access token."}, HTTPStatus.BAD_REQUEST
        request_args = self.PARSER.parse_args()
        user_controller = UserController()
        user = user_controller.get_by_id(user_id)
        correct_password = PasswordHasher.check_password(request_args.get("old_password"), user.password_hash)
        if not correct_password:
            return {"message": "Wrong old password."}, HTTPStatus.BAD_REQUEST
        del request_args["old_password"]
        updates = dict()
        for field in self.FIELDS:
            value = request_args.get(field)
            if field == "password" and value is not None:
                updates["password_hash"] = PasswordHasher.hash_password(value)
            elif field == "login" and value is not None:
                updates[field] = value
        try:
            UserController().update(user, updates)
        except IntegrityError:
            return {"message": f"User with login {updates['login']} already exists."}, HTTPStatus.BAD_REQUEST
        return {"message": "Your profile updated."}, HTTPStatus.OK


api.add_resource(UserCreationView, "/v1/sign-up")
api.add_resource(UserLoginView, "/v1/login")
api.add_resource(UserRefreshView, "/v1/refresh")
api.add_resource(UserHistoryView, "/v1/history")
api.add_resource(UserLogoutView, "/v1/logout")
api.add_resource(UserLogoutAllView, "/v1/logout-all")
api.add_resource(UserChangeView, "/v1/profile")
