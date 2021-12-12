import bcrypt
import uuid


def create_verification_code() -> str:
    return uuid.uuid4().hex


def verify_verification_code(plain_code: str, hashed_code: str) -> bool:
    return bcrypt.checkpw(plain_code.encode('utf-8'), hashed_code.encode('utf-8'))


def get_verification_code_hash(verification_code: str) -> str:
    return bcrypt.hashpw(verification_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
