from http import HTTPStatus

from flask import Blueprint, request, url_for
from flask_restful import Api

from api.base import BaseView
from db.controllers.users import UserController
from db.redis import TokenStorage
from utils.exceptions import OAuthEmailError
from utils.oauth.providers import ProviderFactory
from utils.tokens import TokenMaker

oauth_blueprint = Blueprint("oauth", __name__)
api = Api(oauth_blueprint)


class SocialLogin(BaseView):
    def get(self, provider: str):
        service = ProviderFactory.get_service(provider)
        oauth_provider = service.get_proveider()
        if oauth_provider is None:
            return {"message": f"Wrong OAuth provider - {provider}."}, HTTPStatus.BAD_REQUEST
        return oauth_provider.authorize_redirect(url_for(".socialcallbackview", provider=provider, _external=True))


class SocialCallbackView(BaseView):
    def get(self, provider: str):
        service = ProviderFactory.get_service(provider)
        try:
            payload = service.get_user_payload()
        except OAuthEmailError:
            return {
                "message": f"Provider {provider} can`t return an email for your account. "
                f"Choose another account or link your email with your {provider} account."
            }, HTTPStatus.FORBIDDEN
        controller = UserController()
        user = controller.create_social_user(payload)
        agent = request.user_agent
        access_token, refresh_token = TokenMaker.create_tokens_pair(user)
        TokenStorage().add_token_pair(
            user_id=user.id,
            user_agent=agent.string,
            refresh_token=refresh_token,
            access_token=access_token,
        )
        controller.add_login_record(dict(user_id=user.id, platform=agent.platform, ip=request.remote_addr))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, HTTPStatus.OK


api.add_resource(SocialLogin, "/v1/oauth/login/<string:provider>")
api.add_resource(SocialCallbackView, "/v1/oauth/callback/<string:provider>")
