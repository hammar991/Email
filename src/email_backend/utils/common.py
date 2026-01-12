from argon2 import PasswordHasher


def get_password_hash(password: str) -> str:
    return PasswordHasher().hash(password)


def verify_password_hash(password: str, hash_str: str) -> bool:
    return PasswordHasher().verify(hash_str, password)
