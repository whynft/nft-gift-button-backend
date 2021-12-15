import json

from web3 import Web3

from config.logger import get_app_logger
from config.misc import redis
from config.settings import settings

logger = get_app_logger()

# todo: to env?
darilka_contract = '[ { "inputs": [ { "internalType": "uint256", "name": "_comission", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "constructor" }, { "inputs": [ { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "address", "name": "nftContract", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "bookTransfer", "outputs": [], "stateMutability": "payable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "changeOwner", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "address", "name": "nftContract", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" }, { "internalType": "string", "name": "confirmation", "type": "string" } ], "name": "performTransferNFT", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "nftContract", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" }, { "internalType": "bytes32", "name": "keccak256ConfirmationHash", "type": "bytes32" } ], "name": "setConfirmation", "outputs": [], "stateMutability": "payable", "type": "function" } ]'
darilka_contract_abi = json.loads(darilka_contract)
NONCE_KEY = f"nonce_{settings.ETHEREUM_PUBLIC_ADDRESS}"  # todo: to crud

w3 = Web3(Web3.HTTPProvider(settings.INFURA_HTTPS_ENDPOINT, request_kwargs={'timeout': 60}))


async def warming_nonce():
    nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(settings.ETHEREUM_PUBLIC_ADDRESS))
    await redis.set(NONCE_KEY, nonce)


async def crypto_book(receiver_address: str, nft_contract: str, nft_token: str):
    contract = w3.eth.contract(
        address=Web3.toChecksumAddress(settings.DARILKA_CONTRACT),
        abi=darilka_contract_abi,
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
