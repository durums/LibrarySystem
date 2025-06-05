##################
# users_class.py #
##################

import datetime

class User:
    """
    Repräsentiert einen Benutzer des Bibliothekssystems.
    
    Attributes:
        userID (int): Eindeutige Benutzer-ID.
        name (str): Benutzername.
        age (int): Alter des Benutzers.
        password (str): Passwort des Benutzers.
        role (str): Benutzerrolle (z.B. 'user' oder 'author').
        borrowedItems (list): Liste ausgeliehener Medienobjekte.
        borrowTimestamps (dict): Zeitstempel der Ausleihen nach itemID.
    """

    def __init__(self, userID, name, age, password, role='user'):
        """
        Initialisiert ein neues User-Objekt mit den angegebenen Attributen.

        Args:
            userID (int): Eindeutige Benutzer-ID.
            name (str): Name des Benutzers.
            age (int): Alter des Benutzers.
            password (str): Passwort für das Benutzerkonto.
            role (str, optional): Rolle des Benutzers im System. Standard ist 'user'.
        """
        self.userID = userID
        self.name = name
        self.age = age
        self.password = password
        self.role = role
        self.borrowedItems = []  # Funktioniert jetzt für alle Medientypen
        self.borrowTimestamps = {}

    def borrowItem(self, item):
        """
        Versucht, ein Medium auszuleihen, und speichert bei Erfolg den Ausleihzeitpunkt.

        Args:
            item: Das auszuleihende Medienobjekt mit Methoden `borrow()` und Attributen `itemID`, `title`.
        """
        if item.borrow():
            self.borrowedItems.append(item)
            self.borrowTimestamps[item.itemID] = datetime.datetime.now().isoformat()
        else:
            print(f"'{item.title}' ist derzeit nicht verfügbar.")

    def returnItem(self, item):
        """
        Gibt ein ausgeliehenes Medium zurück und entfernt es aus den Ausleihlisten.

        Args:
            item: Das zurückzugebende Medienobjekt mit Methoden `return_item()` und Attribut `itemID`.
        """
        if item in self.borrowedItems:
            item.return_item()
            self.borrowedItems.remove(item)
            self.borrowTimestamps.pop(item.itemID, None)

   
class Author(User):
    """
    Erweiterung der User-Klasse für Autoren mit Biografie und veröffentlichten Büchern.
    
    Attributes:
        biography (str): Kurzbiografie des Autors.
        writtenBooks (list): Liste der vom Autor geschriebenen Bücher.
    """

    def __init__(self, userID, name, age, password, biography):
        """
        Initialisiert ein neues Author-Objekt mit den gegebenen Benutzerdaten und einer Biografie.

        Args:
            userID (int): Die eindeutige ID des Benutzers.
            name (str): Der Name des Autors.
            age (int): Das Alter des Autors.
            password (str): Das Passwort des Benutzerkontos.
            biography (str): Die Biografie des Autors.
        """
        super().__init__(userID, name, age, password, role='author')
        self.biography = biography
        self.writtenBooks = []

    def add_book(self, book):
        """
        Fügt ein Buch zur Liste der vom Autor geschriebenen Bücher hinzu.

        Args:
            book (Book): Ein Buchobjekt, das vom Autor verfasst wurde.
        """
        self.writtenBooks.append(book)
