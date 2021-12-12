import aioredis

from config.settings import settings

redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', db=0, decode_responses=True)
