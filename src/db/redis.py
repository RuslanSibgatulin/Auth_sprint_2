from redis import StrictRedis

from config import settings


class TokenStorage:
    REFRESH_TOKEN_PREFIX: str = "refresh"
    ACCESS_TOKEN_PREFIX: str = "access"

    def __init__(self):
        self.redis = StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, charset="utf-8", decode_responses=True
        )

    def create_active_refresh_token_key(self, user_id: str, user_agent: str) -> str:
        key = f"{self.REFRESH_TOKEN_PREFIX}:{user_id}:{user_agent}"
        return key

    def create_active_access_token_key(self, user_id: str, user_agent: str) -> str:
        key = f"{self.ACCESS_TOKEN_PREFIX}:{user_id}:{user_agent}"
        return key

    def add_token_pair(self, user_id: str, user_agent: str, refresh_token: str, access_token: str) -> None:
        key_refresh = self.create_active_refresh_token_key(user_id=user_id, user_agent=user_agent)
        key_access = self.create_active_access_token_key(user_id=user_id, user_agent=user_agent)
        pipeline = self.redis.pipeline()
        pipeline.setex(name=key_refresh, time=settings.JWT_REFRESH_TOKEN_EXPIRES, value=refresh_token)
        pipeline.setex(name=key_access, time=settings.JWT_ACCESS_TOKEN_EXPIRES, value=access_token)
        pipeline.execute()

    def add_access_token(self, user_id: str, user_agent: str, access_token: str) -> None:
        key = self.create_active_access_token_key(user_id=user_id, user_agent=user_agent)
        self.redis.setex(name=key, time=settings.REFRESH_TOKEN_TTL, value=access_token)

    def __delete_tokens_by_template(self, template: str) -> None:
        keys_ = self.redis.keys(template)
        pipeline = self.redis.pipeline()
        for key in keys_:
            pipeline.delete(key)
        pipeline.execute()

    def delete_user_token_pair(self, user_id: str, user_agent: str) -> None:
        key_template = f"*:{user_id}:{user_agent}"
        self.__delete_tokens_by_template(key_template)

    def delete_all_user_tokens(self, user_id: str) -> None:
        key_template = f"*:{user_id}:*"
        self.__delete_tokens_by_template(key_template)

    def is_valid_token(self, user_id: str, user_agent: str, token: str, refresh: bool = False) -> bool:
        if refresh:
            key = self.create_active_refresh_token_key(user_id, user_agent)
        else:
            key = self.create_active_access_token_key(user_id, user_agent)
        token_in_redis = self.redis.get(key)
        if token_in_redis == token:
            return True
        return False
