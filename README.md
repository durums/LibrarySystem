# 1. 📚 Library Management System
Ein textbasiertes Bibliotheksverwaltungssystem zur Verwaltung von Medien (Bücher, DVDs, Magazine) und Benutzern mit verschiedenen Rollenrechten. Ideal für Lern- und Schulprojekte im Bereich Python OOP, Dateiverwaltung und Konsolenanwendungen.

# 1.2 🚀 Funktionen

# 1.2.1 🔐 Benutzerverwaltung
- Anmeldung mit Passwort
- Rollen: `user`, `verwaltung`, `admin`
- Benutzer hinzufügen, löschen, Rolle ändern
- Benutzerliste und Suchfunktion

# 1.2.2 📦 Medienverwaltung
- Medien hinzufügen: Buch, DVD, Magazin
- Medien löschen
- Medien durchsuchen und anzeigen
- JSON Datenspeicherung
- Automatisierte UUID-Generierung

# 1.2.3 📖 Ausleihsystem
- Medien ausleihen (Rollenabhängig)
- Medien zurückgeben
- Medien von Nutzern entziehen (nur Admin)
- Eigene ausgeliehene Artikel einsehen
- Zeitstempel für jede Ausleihe

# 1.3 👥 Rollenübersicht

| Rolle       | Berechtigungen                                                                  |
|-------------|---------------------------------------------------------------------------------|
| `user`      | Artikel ausleihen, zurückgeben, eigene Artikel einsehen                         |
| `verwaltung`| Alles wie `user`, zusätzlich: Medien hinzufügen/löschen, Benutzer verwalten     |
| `admin`     | Volle Rechte inkl. Rollenänderung, Artikelentzug, detaillierte Benutzerübersicht|

# 1.4 🛠️ Technische Details

- **Sprache:** Python 3.x
- **Dateien:**
  - `LibrarySystem.py`: Hauptlogik und Menüführung
  - `external_functions.py`: Hilfsfunktionen, Klassen und Backend-Logik
- **Datenformate:**
  - JSON (`media.json`, `users.json`) – primäre Speicherung

# 1.5 🧪 Beispielnutzung

```bash
python LibrarySystem.py