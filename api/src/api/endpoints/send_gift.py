from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

import schemas
from config.misc import redis  # todo: to crud system?
from config.logger import get_app_logger
from utils.security import create_verification_code, get_verification_code_hash

router = APIRouter()
logger = get_app_logger()


@router.post(
    '/verification-code',
    description=(
        'Get verification code that receiver will need to proof himself to backend, i.e. book a gift.'
    ),
    response_model=schemas.VerificationCodeOut,
    responses={
        status.HTTP_410_GONE: {
            "model": schemas.Message,
            "description": "Gift has been already reported to backend and verification code was sent as response.",
        },
    }
)
async def verification_code(gift_in: schemas.Gift):
    gift_verification_code_key = gift_in.nft_contract + ":" + gift_in.nft_token + ':' + 'passphrase'  # todo
    gift_verification_code = await redis.get(gift_verification_code_key)

    if gift_verification_code:
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content={"message": f"Gift has been already reported to backend and verification code was sent as response."},
        )

    logger.info(f"Create pass phrase for {gift_in} and store in Redis its hash...")
    gift_verification_code = create_verification_code()
    await redis.set(gift_verification_code_key, get_verification_code_hash(gift_verification_code))

    return {'verification_code': gift_verification_code, **gift_in.dict()}
