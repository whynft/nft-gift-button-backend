from pydantic import BaseModel


class Gift(BaseModel):
    nft_token: str
    nft_contract: str


class VerificationCodeOut(Gift):
    verification_code: str


class GiftToBookIn(VerificationCodeOut):
    receiver_address: str


