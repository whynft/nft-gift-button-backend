from fastapi import APIRouter

import schemas
from config.settings import settings
from utils.logger import get_app_logger

router = APIRouter()
logger = get_app_logger()


@router.get(
    '/darilka-contract',
    description=(
        'Get Darilka contract address & abi.'
    ),
    response_model=schemas.DarilkaContract,
)
async def darilka_contract():
    return {'address': settings.DARILKA_CONTRACT_ADDRESS, 'abi': settings.DARILKA_CONTRACT_ABI_JSON}
