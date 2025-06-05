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
        """
        Initialisiert ein neues MediaItem mit einem Titel und generierter eindeutiger ID.

        Args:
            itemID (str): Platzhalter für die Übergabe, wird durch UUID überschrieben.
            title (str): Titel des Mediums.
        """
        self.itemID = str(uuid.uuid4())
        self.title = title
        self.available = True

    def borrow(self):
        """
        Versucht, das Medium auszuleihen.

        Returns:
            bool: True, wenn das Medium verfügbar war und ausgeliehen wurde, sonst False.
        """
        if self.available:
            self.available = False
            return True
        return False

    def return_item(self):
        """
        Gibt das Medium zurück und setzt den Verfügbarkeitsstatus auf True.
        """
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
        """
        Initialisiert ein neues Buch-Objekt mit Autor, ISBN und Genre.

        Args:
            itemID (int): Eindeutige ID des Mediums.
            title (str): Titel des Buches.
            author (str): Name des Autors.
            isbn (str): ISBN des Buches.
            genre (str): Genre des Buches (z. B. 'Krimi', 'Sachbuch').
            type (str, optional): Typ des Mediums. Standard ist 'book'.
        """
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
        """
        Initialisiert ein neues DVD-Objekt mit Spieldauer und optionalem Genre.

        Args:
            itemID (int): Eindeutige ID des Mediums.
            title (str): Titel der DVD.
            duration (int): Spieldauer der DVD in Minuten.
            genre (str, optional): Genre der DVD (z. B. 'Drama', 'Action'). Standard ist leerer String.
            type (str, optional): Typ des Mediums. Standard ist 'dvd'.
        """
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
        """
        Initialisiert ein neues Magazin-Objekt mit ID, Titel und Ausgabenbezeichnung.

        Args:
            itemID (int): Die eindeutige ID des Mediums.
            title (str): Der Titel des Magazins.
            issue (str): Die Ausgabenbezeichnung (z. B. 'Juli 2025').
            type (str, optional): Der Medientyp. Standard ist 'magazine'.
        """
        super().__init__(itemID, title)
        self.issue = issue
        self.type = type
