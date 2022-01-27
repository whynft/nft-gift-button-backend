"""Convenience module to centralize keys storing."""
from config.settings import settings

ADDRESS_NONCE_KEY = f"nonce:{settings.ETHEREUM_PUBLIC_ADDRESS}"


def get_gift_hash_key(sender: str, nft_contract: str, nft_token: str):
    """Gift key to receiver.
    Note:
    - we differ sending one gift as we store it on unique together: sender + contract&token.
    """
    return 'gh' + ":" + sender + ":" + nft_contract + ":" + nft_token  # gh - gift hash


def compose_gift_verification_code_key(sender: str, nft_contract: str, nft_token: str):
    return 'gvc' + ":" + sender + ":" + nft_contract + ":" + nft_token  # gft - gift verification code
