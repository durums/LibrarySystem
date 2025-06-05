import json, os
from utils.class_media_items import (Book, DVD, Magazine, MediaItem)
from utils.class_users import (User, Author)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class LibrarySystem:
    """
    Hauptklasse des Bibliothekssystems zur Verwaltung von Medien und Benutzern.
    
    Attributes:
        media_items (list): Liste aller Medien im System.
        users (list): Liste registrierter Benutzer.
        books (list): Zusätzliche Liste der Bücher (falls separat geführt).
    """

    def __init__(self):
        """
        Initialisiert das Bibliothekssystem mit leeren Listen für Medien, Benutzer und Bücher.
        """
        self.media_items = []  # Enthält alle Medientypen (Bücher, DVDs, Magazine)
        self.users = []
        self.books = []

    def addMediaItem(self, item):
        """
        Fügt ein Medium zur Mediensammlung hinzu.

        Parameter:
        - item: Ein Objekt vom Typ Book, DVD oder Magazine.
        """
        self.media_items.append(item)

    def addUser(self, user):
        """
        Fügt einen Benutzer zur Benutzerliste hinzu.

        Parameter:
        - user: Ein User- oder Author-Objekt.
        """
        self.users.append(user)

    def find_media_by_title_and_type(self, title, mediatype):
        """
        Sucht ein Medium anhand von Titel und Typ (book, dvd, magazine).

        Parameter:
        - title (str): Titel des gesuchten Mediums.
        - mediatype (str): Typ des Mediums (z. B. "book", "dvd", "magazine").

        Rückgabewert:
        - Das gefundene Medium-Objekt oder None.
        """
        return next(
            (item for item in self.media_items
            if item.title.lower() == title.lower()
            and type(item).__name__.lower() == mediatype.lower()),
            None
        )

    def changeRole(self, user, new_role):
        """
        Ändert die Rolle eines Benutzers (z. B. von 'user' zu 'admin').

        Parameter:
        - user: Das Benutzerobjekt.
        - new_role (str): Neue Rollenbezeichnung.
        """
        user.role = new_role

    def searchItems(self, title):
        """
        Sucht Medien mit einem bestimmten Titel oder Titelteil.

        Parameter:
        - title (str): Suchbegriff (ganz oder teilweise).

        Rückgabewert:
        - Liste passender Medienobjekte.
        """
        return [item for item in self.media_items if title.lower() in item.title.lower()]

    def username_exists(self, username):
        """
        Prüft, ob ein Benutzername im System bereits existiert.

        Parameter:
        - username (str): Benutzername zur Überprüfung.

        Rückgabewert:
        - True, wenn der Name existiert, sonst False.
        """
        return any(u.name.lower() == username.lower() for u in self.users)

    def save_media_to_json(self, filename="media.json"):
        """
        Speichert alle Medienobjekte als JSON-Datei.

        Parameter:
        - filename (str): Name der Zieldatei (Standard: "media.json").
        """
        path = os.path.join(BASE_DIR, filename)

        data = []
        for item in self.media_items:
            data.append({
                "itemID": item.itemID,
                "type": item.type,
                "title": item.title,
                "author": getattr(item, "author", ""),
                "isbn": getattr(item, "isbn", ""),
                "genre": getattr(item, "genre", ""),
                "issue": getattr(item, "issue", ""),
                "duration": getattr(item, "duration", ""),
                "available": item.available
            })

        with open(path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_media_from_json(self, filename="media.json"):
        """
        Lädt Medienobjekte aus einer JSON-Datei und fügt sie dem System hinzu.

        Parameter:
        - filename (str): Dateiname der JSON-Datei (Standard: "media.json").

        Hinweise:
        - Unterstützt die Typen "book", "dvd" und "magazine".
        - Setzt den Verfügbarkeitsstatus (available) korrekt.
        """
        path = os.path.join(BASE_DIR, filename)

        if not os.path.exists(path):
            print(f"❌ Datei nicht gefunden: {path}")
            return

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                data = json.load(file)

            for entry in data:
                item_type = entry["type"].lower()

                if item_type == "book":
                    item = Book(
                        itemID=entry["itemID"],
                        title=entry["title"],
                        author=entry["author"],
                        isbn=entry["isbn"],
                        genre=entry["genre"],
                        type=item_type
                    )
                elif item_type == "dvd":
                    item = DVD(
                        itemID=entry["itemID"],
                        title=entry["title"],
                        duration=entry["duration"],
                        genre=entry["genre"],  # falls du das eingeführt hast
                        type=item_type
                    )
                elif item_type == "magazine":
                    item = Magazine(
                        itemID=entry["itemID"],
                        title=entry["title"],
                        issue=entry["issue"],
                        type=item_type
                    )
                else:
                    print(f"⚠️ Unbekannter Typ: {item_type}")
                    continue

                item.available = entry.get("available", True)
                self.media_items.append(item)

        except Exception as e:
            print(f"❌ Fehler beim Laden aus JSON: {e}")

    def load_users_from_json(self, filename="users.json"):
        """
        Lädt Benutzer aus einer JSON-Datei und rekonstruiert deren ausgeliehene Bücher.

        Parameter:
        - filename (str): Name der JSON-Datei (Standard: "users.json").

        Hinweise:
        - Unterstützt normale Benutzer und Autoren.
        - Weist ausgeliehene Bücher anhand der ISBNs zu.
        - Stellt Zeitstempel zu Ausleihen (borrowTimestamps) wieder her.
        """
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            print(f"❌ Datei nicht gefunden: {path}")
            return

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                users = json.load(file)

            for entry in users:
                user_id = entry["userID"]
                name = entry["name"]
                age = entry["age"]
                password = entry["password"]
                role = entry["role"]

                if role == "author":
                    user = Author(user_id, name, age, password, biography="")
                else:
                    user = User(user_id, name, age, password, role)

                # Bücher zuweisen
                for isbn in entry.get("borrowedBooks", []):
                    for item in self.media_items:
                        if isinstance(item, Book) and item.isbn == isbn:
                            user.borrowedItems.append(item)
                            item.available = False

                # Zeitstempel wiederherstellen
                timestamps = entry.get("borrowedBookTimestamps", {})
                for isbn, ts in timestamps.items():
                    for item in user.borrowedItems:
                        if isinstance(item, Book) and item.isbn == isbn:
                            user.borrowTimestamps[item.itemID] = ts

                self.addUser(user)

        except Exception as e:
            print(f"❌ Fehler beim Laden der Benutzer aus JSON: {e}")

    def save_users_to_json(self, filename="users.json"):
        """
        Speichert alle Benutzer und deren ausgeliehene Bücher (ISBN & Zeitstempel) als JSON-Datei.

        Parameter:
        - filename (str): Dateiname der Ausgabedatei (Standard: "users.json").
        """
        path = os.path.join(BASE_DIR, filename)
        data = []

        for user in self.users:
            borrowed_books = [
                item.isbn for item in user.borrowedItems if hasattr(item, "isbn")
            ]

            borrowed_timestamps = {
                item.isbn: user.borrowTimestamps.get(item.itemID)
                for item in user.borrowedItems if hasattr(item, "isbn")
            }

            data.append({
                "userID": user.userID,
                "name": user.name,
                "age": user.age,
                "password": user.password,
                "role": user.role,
                "borrowedBooks": borrowed_books,
                "borrowedBookTimestamps": borrowed_timestamps
            })

        with open(path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)