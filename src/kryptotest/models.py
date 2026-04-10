from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class VaultEntry:
    site: str
    username: str
    password: str
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "site": self.site,
            "username": self.username,
            "password": self.password,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VaultEntry":
        return cls(
            site=data["site"],
            username=data["username"],
            password=data["password"],
            notes=data.get("notes", ""),
            created_at=data.get("created_at", datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.utcnow().isoformat()),
        )
