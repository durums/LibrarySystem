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
        borrowTimestamps (dict): Zeitstempel der Ausleihen.
    """

    def __init__(self, userID, name, age, password, role='user'):
        self.userID = userID
        self.name = name
        self.age = age
        self.password = password
        self.role = role
        self.borrowedItems = []  # Funktioniert jetzt für alle Medientypen
        self.borrowTimestamps = {}

    def borrowItem(self, item):
        if item.borrow():
            self.borrowedItems.append(item)
            self.borrowTimestamps[item.itemID] = datetime.datetime.now().isoformat()
        else:
            print(f"'{item.title}' ist derzeit nicht verfügbar.")

    def returnItem(self, item):
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
        super().__init__(userID, name, age, password, role='author')
        self.biography = biography
        self.writtenBooks = []

    def add_book(self, book):
        self.writtenBooks.append(book)