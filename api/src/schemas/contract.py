from pydantic import BaseModel


class DarilkaContract(BaseModel):
    address: str
    abi: list
