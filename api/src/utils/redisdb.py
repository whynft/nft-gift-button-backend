"""Convenience module to centralize keys storing."""
from config.settings import settings

ADDRESS_NONCE_KEY = f"nonce:{settings.ETHEREUM_PUBLIC_ADDRESS}"


def get_gift_hash_key(nft_contract: str, nft_token: str):
    return nft_contract + ":" + nft_token


def get_gift_verification_code_key(nft_contract: str, nft_token: str):
    return nft_contract + ":" + nft_token + ":" + 'vc'
