# Projektübersicht

## Idee

Kryptotest ist ein lokaler Passwort-Tresor in Python. Die Einträge werden nicht im Klartext gespeichert, sondern verschlüsselt in einer Datei abgelegt.

## Lernziele

Mit diesem Projekt lernst du:

- was ein Salt ist
- wie aus einem Passwort ein Schlüssel abgeleitet wird
- was symmetrische Verschlüsselung ist
- wie man Daten strukturiert speichert
- wie man ein CLI-Programm baut
- wie man ein Projekt für GitHub sauber aufteilt

## Technische Bausteine

### 1. Master-Passwort
Das Master-Passwort wird verwendet, um den Verschlüsselungsschlüssel abzuleiten.

### 2. PBKDF2-HMAC-SHA256
Das Master-Passwort wird nicht direkt als Schlüssel genutzt. Stattdessen wird mit PBKDF2 und einem Salt ein stärkerer Schlüssel abgeleitet.

### 3. Fernet
Fernet übernimmt die eigentliche Verschlüsselung und stellt sicher, dass die Daten nicht unbemerkt verändert wurden.

### 4. JSON-Datei
Die verschlüsselte Datei enthält:

- Version
- Salt
- Hash des Master-Passworts
- verschlüsselte Nutzdaten

## Mögliche Erweiterungen

- grafische Oberfläche
- Kategorien
- Passwortbewertung
- TOTP für Zwei-Faktor-Codes
- verschlüsselter Import/Export
- Backup-System
