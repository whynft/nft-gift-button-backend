from fastapi import APIRouter

from api.endpoints import receive_gift, general, send_gift


api_router = APIRouter()
api_router.include_router(receive_gift.router, prefix='/receive-gift', tags=['receive-gift'])
api_router.include_router(general.router, prefix='/general', tags=['general'])
api_router.include_router(send_gift.router, prefix='/send-gift', tags=['send-gift'])
