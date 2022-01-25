from web3 import Web3

from utils.logger import get_app_logger
from config.misc import redis
from config.settings import settings

logger = get_app_logger()

NONCE_KEY = f"nonce_{settings.ETHEREUM_PUBLIC_ADDRESS}"  # todo: to crud

w3 = Web3(Web3.HTTPProvider(settings.INFURA_HTTPS_ENDPOINT, request_kwargs={'timeout': 60}))


async def warming_nonce():
    nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(settings.ETHEREUM_PUBLIC_ADDRESS))
    await redis.set(NONCE_KEY, nonce)


async def crypto_book(receiver_address: str, nft_contract: str, nft_token: str):
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(settings.DARILKA_CONTRACT_ADDRESS),
        abi=settings.DARILKA_CONTRACT_ABI_JSON,
    )

    nonce = int(await redis.incr(NONCE_KEY)) - 1
    logger.info(f'Prepare next operation with {nonce = } for {settings.ETHEREUM_PUBLIC_ADDRESS = }.')

    txn_dict = (
        contract
        .functions
        .bookTransfer(
            Web3.toChecksumAddress(receiver_address),
            Web3.toChecksumAddress(nft_contract),
            int(nft_token)
        )
        .buildTransaction({'gas': 150000, 'gasPrice': 30000000000, 'nonce': nonce, })  # todo: make clever
    )

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=settings.ETHEREUM_PRIVATE_KEY)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.debug(f'Sent transaction to EMV, got {result = }.')

    return result
