from flask_jwt_extended import create_access_token, create_refresh_token

from db.models import User


class TokenMaker:
    @classmethod
    def create_tokens_pair(cls, user: User) -> tuple[str, str]:
        action_ids = set([action.id for user_role in user.roles for action in user_role.role.actions])
        access_token = create_access_token({"user_id": user.id, "action_ids": list(action_ids)})
        refresh_token = create_refresh_token({"user_id": user.id})
        return access_token, refresh_token
