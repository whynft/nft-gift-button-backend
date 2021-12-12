from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import schemas
from clients.crypto_sdk import CryptoSdk
from config.settings import settings
from config.misc import redis  # todo: to crud system?
from config.logger import get_app_logger

router = APIRouter()
crypto_sdk = CryptoSdk(settings.CRYPTO_SDK_ENDPOINT)
logger = get_app_logger()


@router.post(
    '/book',
    description=(
            'Book a gift to a receiver particular address with help of book method of Darilka contract.'
    ),
    response_model=schemas.GiftToBookIn,
    responses={
        status.HTTP_423_LOCKED: {"model": schemas.Message, "description": "Booked by another address."},
    }
)
async def book(gift_in: schemas.GiftToBookIn):
    gift_hash = gift_in.nft_contract + ":" + gift_in.nft_token
    receiver_address = await redis.get(gift_hash)
    if receiver_address and receiver_address != gift_in.receiver_address:
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={"message": f"Already booked by another address: {gift_in.receiver_address}"},
        )

    res = await crypto_sdk.book(
        gift_in,
        centralized_backend_key=settings.ETHEREUM_PRIVATE_KEY,
        transfer_contract=settings.DARILKA_CONTRACT,
    )
    logger.info(f'Booked through sdk, got {res}')

    logger.info(f'Remember booking {gift_hash} for {gift_in.receiver_address}')
    await redis.set(gift_hash, gift_in.receiver_address)

    return gift_in


# @router.post(
#     '/transfer',
#     description=(
#         'Initiate transfer through backend contract, i.e. Darilka contract.'
#     ),
#     response_model=schemas.,
#     responses = {
#         status.HTTP_403_FORBIDDEN: {
#             "model": schemas.Message, "description": "When gift was not booked, i.e. we have not info in our system"},
#     }
# )
# async def transfer(gift_in: schemas.GiftToTransferIn):
#     gift_hash = gift_in.nft_contract + ":" + gift_in.nft_token
#     receiver_address = await redis.get(gift_hash)
#     if not receiver_address:
#         return JSONResponse(
#             status_code=status.HTTP_403_FORBIDDEN,
#             content={"message": f"May be gift was not booked."},
#         )
#
#
#     return gift_in
