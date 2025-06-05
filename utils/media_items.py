##################
# media_items.py #
##################

import uuid

class MediaItem:
    """
    Basisklasse für alle Medientypen in der Bibliothek.
    
    Attributes:
        itemID (str): Eindeutige ID des Mediums.
        title (str): Titel des Mediums.
        available (bool): Verfügbarkeitsstatus des Mediums.
    """

    def __init__(self, itemID, title):
        self.itemID = str(uuid.uuid4())
        self.title = title
        self.available = True

    def borrow(self):
        if self.available:
            self.available = False
            return True
        return False

    def return_item(self):
        self.available = True

class Book(MediaItem):
    """
    Repräsentiert ein Buch und erweitert MediaItem um buchtypische Eigenschaften.
    
    Attributes:
        author (str): Name des Autors.
        isbn (str): ISBN des Buches.
        genre (str): Genre des Buches.
        type (str): Typ des Mediums (Standard: 'book').
    """

    def __init__(self, itemID, title, author, isbn, genre, type='book'):
        super().__init__(itemID, title)
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.type = type

class DVD(MediaItem):
    """
    Repräsentiert eine DVD als Medium mit Dauer und optionalem Genre.
    
    Attributes:
        duration (int): Spieldauer in Minuten.
        genre (str): Genre der DVD.
        type (str): Typ des Mediums (Standard: 'dvd').
    """

    def __init__(self, itemID, title, duration, genre="", type="dvd"):
        super().__init__(itemID, title)
        self.duration = duration
        self.genre = genre
        self.type = type
        
class Magazine(MediaItem):
    """
    Repräsentiert ein Magazin mit Ausgabenummer.
    
    Attributes:
        issue (str): Ausgabenbezeichnung.
        type (str): Typ des Mediums (Standard: 'magazine').
    """

    def __init__(self, itemID, title, issue, type='magazine'):
        super().__init__(itemID, title)
        self.issue = issue
        self.type = type