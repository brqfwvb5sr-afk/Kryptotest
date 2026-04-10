# Sicherheitsnotizen

## Was dieses Projekt gut macht

- Es verwendet keine selbst erfundene Verschlüsselung.
- Es nutzt einen Salt.
- Es leitet den Schlüssel mit PBKDF2 ab.
- Die eigentlichen Daten werden verschlüsselt gespeichert.
- Lokale Vault-Dateien werden per `.gitignore` nicht versehentlich hochgeladen.

## Was noch verbessert werden könnte

- Passwort-Hash-Vergleich mit `hmac.compare_digest`
- getrennte Konfigurationsdatei
- besserer Umgang mit Speicherbereinigung sensibler Daten
- Clipboard-Schutz
- automatisches Sperren nach Zeit
- Backup- und Recovery-Mechanismus
- mehr Tests für Fehlerfälle

## Wichtiger Hinweis

Dieses Projekt ist ein Lernprojekt. Es ist eine gute Basis, aber noch kein voll ausgereifter Ersatz für professionelle Passwort-Manager.
