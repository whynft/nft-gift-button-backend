from fastapi import APIRouter

from api.endpoints import receive_gift, general


api_router = APIRouter()
api_router.include_router(receive_gift.router, prefix='/receive-gift', tags=['receive-gift'])
api_router.include_router(general.router, prefix='/general', tags=['general'])
