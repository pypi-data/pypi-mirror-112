from functools import partial

import orjson
from aiocache import Cache, cached
from aiocache.serializers import BaseSerializer

from .settings import settings


class JsonSerializer(BaseSerializer):
    def dumps(self, value):
        return orjson.dumps(value)

    def loads(self, value):
        if value is None:
            return None
        return orjson.loads(value)


json_cached = partial(
    cached,
    cache=Cache.REDIS,
    serializer=JsonSerializer(),
    endpoint=settings.redis_host,
    port=settings.redis_port,
)
