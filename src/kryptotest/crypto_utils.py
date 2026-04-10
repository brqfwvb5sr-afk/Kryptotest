import base64
import hashlib
import secrets

from cryptography.fernet import Fernet


PBKDF2_ITERATIONS = 390_000
SALT_SIZE = 16


def generate_salt() -> bytes:
    return secrets.token_bytes(SALT_SIZE)


def derive_key(master_password: str, salt: bytes) -> bytes:
    if not master_password:
        raise ValueError("Master-Passwort darf nicht leer sein.")
    key = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32,
    )
    return base64.urlsafe_b64encode(key)


def build_fernet(master_password: str, salt: bytes) -> Fernet:
    key = derive_key(master_password, salt)
    return Fernet(key)


def encrypt_bytes(data: bytes, master_password: str, salt: bytes) -> bytes:
    fernet = build_fernet(master_password, salt)
    return fernet.encrypt(data)


def decrypt_bytes(token: bytes, master_password: str, salt: bytes) -> bytes:
    fernet = build_fernet(master_password, salt)
    return fernet.decrypt(token)


def hash_master_password(master_password: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=32,
    )
    return digest.hex()


def verify_master_password(master_password: str, salt: bytes, stored_hash: str) -> bool:
    return hash_master_password(master_password, salt) == stored_hash


def generate_password(
    length: int = 20,
    use_letters: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    if length < 8:
        raise ValueError("Die Passwortlänge muss mindestens 8 sein.")

    alphabet = ""
    if use_letters:
        alphabet += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_digits:
        alphabet += "0123456789"
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.?/"

    if not alphabet:
        raise ValueError("Mindestens ein Zeichensatz muss aktiviert sein.")

    return "".join(secrets.choice(alphabet) for _ in range(length))
