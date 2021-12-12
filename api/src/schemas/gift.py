from pydantic import BaseModel


class Gift(BaseModel):
    nft_token: str
    nft_contract: str


class GiftToBookIn(Gift):
    receiver_address: str


class VerificationCodeOut(Gift):
    verification_code: str


