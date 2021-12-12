from pydantic import BaseModel


class GiftToBookIn(BaseModel):
    nft_token: str
    nft_contract: str
    receiver_address: str


# class GiftToTransferIn(GiftToBookIn):
#     password: str
