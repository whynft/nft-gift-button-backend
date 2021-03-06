from logging.config import dictConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api import api_router
from utils.logger import get_app_logger
from config.settings import settings, LOGGING

dictConfig(LOGGING)
logger = get_app_logger()


app = FastAPI(
    title='NFT Gift API',
    openapi_url=f'{settings.API_V1}/openapi.json',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    from events.startup import warming_nonce

    logger.info("Prepare and initiate nonce according to the chain...")
    await warming_nonce()


app.include_router(api_router, prefix=settings.API_V1)
