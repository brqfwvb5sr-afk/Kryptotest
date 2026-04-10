from src.kryptotest.passwords import add_entry, delete_entry, get_entry, search_entries, update_entry


def test_add_and_get_entry():
    data = {"entries": []}
    add_entry(data, "github.com", "alexandre", "secret123")
    entry = get_entry(data, "github.com")

    assert entry["username"] == "alexandre"
    assert entry["password"] == "secret123"


def test_search_entries():
    data = {"entries": []}
    add_entry(data, "github.com", "alex", "pw1", "code hosting")
    add_entry(data, "gmail.com", "alex.mail", "pw2", "mail")
    results = search_entries(data, "git")

    assert len(results) == 1
    assert results[0]["site"] == "github.com"


def test_update_entry():
    data = {"entries": []}
    add_entry(data, "github.com", "alex", "pw1")
    updated = update_entry(data, "github.com", password="pw2")

    assert updated is True
    assert get_entry(data, "github.com")["password"] == "pw2"


def test_delete_entry():
    data = {"entries": []}
    add_entry(data, "github.com", "alex", "pw1")
    deleted = delete_entry(data, "github.com")

    assert deleted is True
    assert data["entries"] == []
