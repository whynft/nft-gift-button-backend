from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import schemas
from clients.crypto_sdk import CryptoSdk
from config.settings import settings
from config.misc import redis  # todo: to crud system?
from config.logger import get_app_logger
from utils.evm import crypto_book
from utils.security import verify_verification_code

router = APIRouter()
crypto_sdk = CryptoSdk(settings.CRYPTO_SDK_ENDPOINT)
logger = get_app_logger()


@router.post(
    '/book',
    description=(
            'Book a gift to a receiver particular address. '
            'It requires receiver to show right verification code and after that '
            'backend will book the receiver with help of Darilka contract.'
    ),
    response_model=schemas.GiftToBookIn,
    responses={
        status.HTTP_423_LOCKED: {"model": schemas.Message, "description": "Booked by another address."},
        status.HTTP_409_CONFLICT: {
            "model": schemas.Message, "description": "Gift is not sent, backend knows nothing about."
        },
        status.HTTP_403_FORBIDDEN: {
            "model": schemas.Message, "description": "Verification code is invalid."
        },
    }
)
async def book(gift_in: schemas.GiftToBookIn):
    gift_hash = gift_in.nft_contract + ":" + gift_in.nft_token  # todo
    gift_verification_code_key = gift_in.nft_contract + ":" + gift_in.nft_token + ':' + 'passphrase'  # todo

    receiver_address = await redis.get(gift_hash)
    if receiver_address and receiver_address != gift_in.receiver_address:
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={"message": f"Already booked by another address: {gift_in.receiver_address}"},
        )

    verification_code_hash = await redis.get(gift_verification_code_key)
    if not verification_code_hash:
        logger.info(f'Gift is not sent, backend knows nothing: {gift_in}')
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        )

    if not verify_verification_code(gift_in.verification_code, verification_code_hash):  # todo: pop verification_code
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": f"Verification code is invalid for: {gift_in}"},
        )

    res = crypto_book(
        receiver_address=gift_in.receiver_address, nft_token=gift_in.nft_token, nft_contract=gift_in.nft_contract,
    )
    # todo: deprecate Js and Js microservice
    # res = await crypto_sdk.book(
    #     gift_in,
    #     centralized_backend_key=settings.ETHEREUM_PRIVATE_KEY,
    #     transfer_contract=settings.DARILKA_CONTRACT,
    # )
    logger.info(f'Booked through crypto, got {res}')

    logger.info(f'Remember booking {gift_hash} for {gift_in.receiver_address}')
    await redis.set(gift_hash, gift_in.receiver_address)

    return gift_in
