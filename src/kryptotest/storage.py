import base64
import json
from pathlib import Path
from typing import Any

from src.kryptotest.crypto_utils import (
    decrypt_bytes,
    encrypt_bytes,
    generate_salt,
    hash_master_password,
    verify_master_password,
)

VAULT_FILE = Path("vault.json")


def vault_exists() -> bool:
    return VAULT_FILE.exists()


def create_empty_vault(master_password: str) -> None:
    if vault_exists():
        raise FileExistsError("Vault existiert bereits.")

    salt = generate_salt()
    encrypted_payload = encrypt_bytes(b'{"entries": []}', master_password, salt)

    payload = {
        "version": 1,
        "salt": base64.b64encode(salt).decode("utf-8"),
        "master_hash": hash_master_password(master_password, salt),
        "encrypted_data": base64.b64encode(encrypted_payload).decode("utf-8"),
    }
    VAULT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_vault(master_password: str) -> dict[str, Any]:
    if not vault_exists():
        raise FileNotFoundError("Vault wurde nicht gefunden. Führe zuerst setup aus.")

    raw = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    salt = base64.b64decode(raw["salt"])

    if not verify_master_password(master_password, salt, raw["master_hash"]):
        raise PermissionError("Master-Passwort ist falsch.")

    encrypted_data = base64.b64decode(raw["encrypted_data"])
    decrypted = decrypt_bytes(encrypted_data, master_password, salt)
    return json.loads(decrypted.decode("utf-8"))


def save_vault(data: dict[str, Any], master_password: str) -> None:
    if not vault_exists():
        raise FileNotFoundError("Vault wurde nicht gefunden.")

    raw = json.loads(VAULT_FILE.read_text(encoding="utf-8"))
    salt = base64.b64decode(raw["salt"])

    if not verify_master_password(master_password, salt, raw["master_hash"]):
        raise PermissionError("Master-Passwort ist falsch.")

    encrypted_data = encrypt_bytes(
        json.dumps(data, indent=2).encode("utf-8"),
        master_password,
        salt,
    )

    raw["encrypted_data"] = base64.b64encode(encrypted_data).decode("utf-8")
    VAULT_FILE.write_text(json.dumps(raw, indent=2), encoding="utf-8")


def export_decrypted_data(master_password: str, target_path: str = "vault_export.json") -> None:
    data = load_vault(master_password)
    Path(target_path).write_text(json.dumps(data, indent=2), encoding="utf-8")
