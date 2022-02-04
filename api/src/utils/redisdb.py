"""Convenience module to centralize keys storing."""
from config.settings import settings

ADDRESS_NONCE_KEY = f"nonce:{settings.ETHEREUM_PUBLIC_ADDRESS}"


class NftGiftRedisKeys:
    """Convenience class to store keys per gift.
    - we differ sending one gift as we store it on unique together: sender + contract&token.
    """

    def __init__(self, sender: str, nft_contract: str, nft_token: str):
        self.sender = sender
        self.contract = nft_contract
        self.token = nft_token
        self._hash = f'{self.sender}:{self.contract}:{self.token}'

    def key_to_receiver(self):
        """We interpret a value existence as booked status for a gift."""
        return f'gh:{self._hash}'  # gh - gift hash

    def key_to_verification_code(self):
        return f'gvc:{self._hash}'  # gvt - gift verification code
