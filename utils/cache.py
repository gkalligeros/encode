import json
from typing import Optional, Union, List, Any
from zlib import adler32

from redis import Redis

from config import config


class RedisCache:
    def __init__(self):
        if Redis is object:
            self.client = None
            return
        self.client = Redis(
            host=config.REDIS_HOST,
            username=config.REDIS_USER,
            password=config.REDIS_PASSWORD,
            db=0,
            socket_timeout=5,
            decode_responses=True,
        )

    def get_json(self, key: str) -> Optional[Union[list, dict]]:
        if not self.client:
            return None
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError) as e:
                return None
        return None

    def store_json(
        self, key: str, value: Union[list, dict], expire: int = None
    ) -> None:
        if not self.client:
            return
        self.client.set(key, json.dumps(value), ex=expire)

    def generate_key(self, function_name: str, params: List[Any]):
        params_str = f"{[str(param) for param in params]}"
        return f"{function_name}:{adler32(params_str.encode())}"
