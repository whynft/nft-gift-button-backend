import asyncio

from web3 import Web3

from events.startup import warming_nonce
from utils.logger import get_app_logger
from config.misc import redis, w3
from config.settings import settings
from utils.redisdb import ADDRESS_NONCE_KEY

logger = get_app_logger()
lock = asyncio.Lock()


def _is_transaction_nonce_low(web3_error) -> bool:
    if not len(web3_error.args):
        return False
    args = web3_error.args[0]
    if args.get('message') and args['message'] == 'nonce too low':
        return True
    return False


async def crypto_book(receiver_address: str, nft_contract: str, nft_token: str) -> str:
    """Returns transaction hex.
    Note that we want to allow retry on wrong nonce and implement such continues retry policy.
    The issue comes when private key is used in external from app manner - directly from metamask e.g.
    (ref to https://github.com/whynft/nft-gift-button-backend/issues/10).
    """
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(settings.DARILKA_CONTRACT_ADDRESS),
        abi=settings.DARILKA_CONTRACT_ABI_JSON,
    )

    nonce = int(await redis.incr(ADDRESS_NONCE_KEY)) - 1
    logger.info(f'Prepare next operation with {nonce = } for {settings.ETHEREUM_PUBLIC_ADDRESS = }.')

    txn_dict = (
        contract
        .functions
        .bookTransfer(
            Web3.toChecksumAddress(receiver_address),
            Web3.toChecksumAddress(nft_contract),
            int(nft_token)
        )
        .buildTransaction(
            {
                'gas': settings.DARILKA_BOOK_TRANSFER_GAS,
                'gasPrice': settings.DARILKA_BOOK_TRANSFER_GAS_PRICE,
                'nonce': nonce,
            }
        )  # todo: make clever
    )

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=settings.ETHEREUM_PRIVATE_KEY)

    try:
        transaction = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except ValueError as e:
        if _is_transaction_nonce_low(e):
            async with lock:
                await warming_nonce()
            return await crypto_book(receiver_address, nft_contract, nft_token)
        raise(e)

    logger.debug(f'Sent transaction to EMV, got transaction = {transaction.hex()}.')
    return transaction.hex()
