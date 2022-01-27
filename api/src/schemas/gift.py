from pydantic import BaseModel


class Gift(BaseModel):
    sender_address: str
    nft_token: str
    nft_contract: str


class VerificationCodeOut(Gift):
    verification_code: str


class GiftToBookIn(Gift):
    verification_code: str
    receiver_address: str


