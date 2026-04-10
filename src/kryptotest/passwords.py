from datetime import datetime

from src.kryptotest.models import VaultEntry


def add_entry(data: dict, site: str, username: str, password: str, notes: str = "") -> None:
    entries = data.setdefault("entries", [])
    for entry in entries:
        if entry["site"].lower() == site.lower():
            raise ValueError("Für diese Seite existiert bereits ein Eintrag.")
    new_entry = VaultEntry(site=site, username=username, password=password, notes=notes)
    entries.append(new_entry.to_dict())


def list_entries(data: dict) -> list[dict]:
    return sorted(data.get("entries", []), key=lambda entry: entry["site"].lower())


def get_entry(data: dict, site: str) -> dict:
    for entry in data.get("entries", []):
        if entry["site"].lower() == site.lower():
            return entry
    raise KeyError("Eintrag nicht gefunden.")


def delete_entry(data: dict, site: str) -> bool:
    entries = data.get("entries", [])
    for index, entry in enumerate(entries):
        if entry["site"].lower() == site.lower():
            del entries[index]
            return True
    return False


def search_entries(data: dict, query: str) -> list[dict]:
    query = query.lower()
    results = []
    for entry in data.get("entries", []):
        if (
            query in entry["site"].lower()
            or query in entry["username"].lower()
            or query in entry.get("notes", "").lower()
        ):
            results.append(entry)
    return sorted(results, key=lambda entry: entry["site"].lower())


def update_entry(
    data: dict,
    site: str,
    username: str | None = None,
    password: str | None = None,
    notes: str | None = None,
) -> bool:
    for entry in data.get("entries", []):
        if entry["site"].lower() == site.lower():
            if username is not None:
                entry["username"] = username
            if password is not None:
                entry["password"] = password
            if notes is not None:
                entry["notes"] = notes
            entry["updated_at"] = datetime.utcnow().isoformat()
            return True
    return False
