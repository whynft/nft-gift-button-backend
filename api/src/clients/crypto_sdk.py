import aiohttp

from utils.logger import get_app_logger
from schemas import GiftToBookIn

logger = get_app_logger()


async def _post_request(url, data) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data) as response:
            try:
                return await response.json()
            except ValueError as e:
                logger.exception(f'Error {e} for {url = }: {response.text = }')
                raise e


class CryptoSdk:
    def __init__(self, endpoint: str = 'http://crypto_sdk:8080/'):
        self.endpoint = endpoint

    async def book(self, gift: GiftToBookIn, centralized_backend_key: str, transfer_contract: str):
        return await _post_request(
            self.endpoint + 'book',
            data={
                "transfer_contract": transfer_contract,
                "receiver": gift.receiver_address,
                "nft_contract": gift.nft_contract,
                "token": gift.nft_token,
                "private_ext": centralized_backend_key
            }
        )

