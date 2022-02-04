from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import schemas
from config.misc import redis
from utils.logger import get_app_logger
from clients.evm import crypto_book
from utils.redisdb import NftGiftRedisKeys
from utils.security import verify_verification_code

router = APIRouter()
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
    nft_gift_redis_keys = NftGiftRedisKeys(gift_in.sender_address, gift_in.nft_contract, gift_in.nft_token)
    gift_hash_key = nft_gift_redis_keys.key_to_receiver()

    receiver_address = await redis.get(gift_hash_key)
    if receiver_address:
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={"message": f"Already booked by: {gift_in.receiver_address}"},
        )

    verification_code_hash = await redis.get(nft_gift_redis_keys.key_to_verification_code())
    if not verification_code_hash:
        logger.info(f'Gift is not sent, backend knows nothing: {gift_in}')
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
        )

    if not verify_verification_code(gift_in.verification_code, verification_code_hash):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": f"Verification code is invalid for: {gift_in}"},
        )

    res = await crypto_book(
        receiver_address=gift_in.receiver_address, nft_token=gift_in.nft_token, nft_contract=gift_in.nft_contract,
    )
    logger.info(f'Booked through crypto, got {res}')

    logger.info(f'Remember booking of {gift_in} for {gift_in.receiver_address}')
    await redis.set(gift_hash_key, gift_in.receiver_address)

    return gift_in
