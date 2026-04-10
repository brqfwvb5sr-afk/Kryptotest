import argparse
import getpass

from src.kryptotest.crypto_utils import generate_password
from src.kryptotest.passwords import (
    add_entry,
    delete_entry,
    get_entry,
    list_entries,
    search_entries,
    update_entry,
)
from src.kryptotest.storage import (
    create_empty_vault,
    export_decrypted_data,
    load_vault,
    save_vault,
    vault_exists,
)


def _prompt_master_password(confirm: bool = False) -> str:
    password = getpass.getpass("Master-Passwort: ")
    if confirm:
        second = getpass.getpass("Master-Passwort wiederholen: ")
        if password != second:
            raise ValueError("Die Passwörter stimmen nicht überein.")
    return password


def handle_setup() -> None:
    if vault_exists():
        print("Vault existiert bereits.")
        return
    master_password = _prompt_master_password(confirm=True)
    create_empty_vault(master_password)
    print("Vault wurde erstellt.")


def handle_unlock() -> None:
    master_password = _prompt_master_password()
    load_vault(master_password)
    print("Vault erfolgreich entsperrt.")


def handle_add() -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)
    site = input("Seite: ").strip()
    username = input("Benutzername: ").strip()
    use_generator = input("Passwort generieren? (j/n): ").strip().lower() == "j"
    if use_generator:
        password = generate_password()
        print(f"Generiertes Passwort: {password}")
    else:
        password = getpass.getpass("Passwort: ")
    notes = input("Notizen (optional): ").strip()
    add_entry(data, site=site, username=username, password=password, notes=notes)
    save_vault(data, master_password)
    print("Eintrag gespeichert.")


def handle_list() -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)
    entries = list_entries(data)
    if not entries:
        print("Keine Einträge vorhanden.")
        return

    for entry in entries:
        print("-" * 40)
        print(f"Seite: {entry['site']}")
        print(f"Benutzername: {entry['username']}")
        print(f"Erstellt: {entry['created_at']}")


def handle_get(site: str) -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)
    entry = get_entry(data, site)
    print(f"Seite: {entry['site']}")
    print(f"Benutzername: {entry['username']}")
    print(f"Passwort: {entry['password']}")
    print(f"Notizen: {entry.get('notes', '')}")
    print(f"Erstellt: {entry['created_at']}")
    print(f"Aktualisiert: {entry['updated_at']}")


def handle_search(query: str) -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)
    results = search_entries(data, query)
    if not results:
        print("Keine Treffer.")
        return
    for entry in results:
        print("-" * 40)
        print(f"Seite: {entry['site']}")
        print(f"Benutzername: {entry['username']}")
        print(f"Notizen: {entry.get('notes', '')}")


def handle_delete(site: str) -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)
    deleted = delete_entry(data, site)
    if not deleted:
        print("Eintrag wurde nicht gefunden.")
        return
    save_vault(data, master_password)
    print("Eintrag gelöscht.")


def handle_generate(length: int) -> None:
    password = generate_password(length=length)
    print(password)


def handle_export() -> None:
    master_password = _prompt_master_password()
    export_decrypted_data(master_password)
    print("Vault wurde als entschlüsselte Datei exportiert: vault_export.json")


def handle_update(site: str) -> None:
    master_password = _prompt_master_password()
    data = load_vault(master_password)

    print("Felder leer lassen, wenn nichts geändert werden soll.")
    username = input("Neuer Benutzername: ").strip() or None
    password = getpass.getpass("Neues Passwort: ").strip() or None
    notes = input("Neue Notizen: ").strip() or None

    updated = update_entry(data, site=site, username=username, password=password, notes=notes)
    if not updated:
        print("Eintrag wurde nicht gefunden.")
        return

    save_vault(data, master_password)
    print("Eintrag aktualisiert.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Kryptotest - lokaler Passwort-Tresor mit Verschlüsselung"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("setup")
    subparsers.add_parser("unlock")
    subparsers.add_parser("add")
    subparsers.add_parser("list")

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--site", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--query", required=True)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--site", required=True)

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--length", type=int, default=20)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--site", required=True)

    subparsers.add_parser("export")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "setup":
            handle_setup()
        elif args.command == "unlock":
            handle_unlock()
        elif args.command == "add":
            handle_add()
        elif args.command == "list":
            handle_list()
        elif args.command == "get":
            handle_get(args.site)
        elif args.command == "search":
            handle_search(args.query)
        elif args.command == "delete":
            handle_delete(args.site)
        elif args.command == "generate":
            handle_generate(args.length)
        elif args.command == "export":
            handle_export()
        elif args.command == "update":
            handle_update(args.site)
    except Exception as exc:
        print(f"Fehler: {exc}")
