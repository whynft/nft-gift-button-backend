import aioredis
from web3 import Web3

from config.settings import settings

redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', db=0, decode_responses=True)
w3 = Web3(Web3.HTTPProvider(settings.INFURA_HTTPS_ENDPOINT, request_kwargs={'timeout': 60}))
