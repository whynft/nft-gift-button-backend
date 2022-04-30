from web3 import Web3

from config.misc import w3, redis
from config.settings import settings
from utils.redisdb import ADDRESS_NONCE_KEY


async def warming_nonce():
    nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(settings.ETHEREUM_PUBLIC_ADDRESS))
    await redis.set(ADDRESS_NONCE_KEY, nonce)
