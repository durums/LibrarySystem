#########################
# external_functions.py #
#########################

import time, sys, os, msvcrt, datetime, uuid, json
from utils.class_media_items import (Book, DVD, Magazine, MediaItem)
from utils.class_users import (User, Author)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cls():
    """
    Bildschirm löschen – funktioniert auf Windows- und Unix-Systemen.

    Führt den passenden Systembefehl aus, um das Terminal zu leeren:
    - 'cls' für Windows
    - 'clear' für Unix/Linux/macOS
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_screen(duration = 5):
    """
    Zeigt eine einfache Ladeanimation für die angegebene Dauer.

    Die Animation besteht aus rotierenden Symbolen (|, /, -, \\), die im Terminal angezeigt werden.

    Args:
        duration (int, optional): Dauer der Ladeanimation in Sekunden. Standard ist 5 Sekunden.
    """
    cls()
    end_time = time.time() + duration
    loading_animation = ["|", "/", "-", "\\"]

    while time.time() < end_time:
        for frame in loading_animation:
            sys.stdout.write(f"\rLädt... {frame}")
            sys.stdout.flush()
            time.sleep(0.2)

def hold_until_user_exits():
    """
    Pausiert das Programm, bis der Benutzer die Leertaste drückt.

    Wartet in einer Schleife auf Benutzereingaben über `msvcrt.getch()`
    und beendet sich erst, wenn die Leertaste erkannt wird.
    """
    print("\nDrücke <Leertaste> um zu verlassen.")
    while True:
        key = msvcrt.getch()  # Reads the input but does nothing if it's not the space bar

        if key == b' ':  # If space bar is pressed
            break

def menu_show_articles(library):
    """
    Zeigt alle verfügbaren Bücher, DVDs oder Magazine basierend auf Benutzerauswahl.

    Der Benutzer wählt eine Medienkategorie (Bücher, DVDs oder Magazine).
    Die Funktion listet alle Medienobjekte dieser Kategorie aus `library.media_items` auf,
    einschließlich ihres Verfügbarkeitsstatus.

    Args:
        library: Ein Objekt, das eine Liste `media_items` enthält,
                 bestehend aus Instanzen von Book, DVD oder Magazine.
    """
    cls()
    inner_choice = input("Auswählen:\n\n1. Alle Bücher\n2. Alle DVDs\n3. Alle Magazine\n\nBitte Auswahl eingeben (1-3):").strip().lower()
    if inner_choice == "1":
        cls()
        print("📖 Verfügbare Bücher:\n")
        for item in library.media_items:
            status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
            if isinstance(item, Book):
                print(f"- 📘 Buch: {item.title} von {item.author} [{item.genre}] – {status}")
                time.sleep(0.1)

    elif inner_choice == "2":
        cls()
        print("📀 Verfügbare DVDs:\n")
        for item in library.media_items:
            status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
            if isinstance(item, DVD):
                print(f"- 📀 DVD: {item.title}, Dauer: {item.duration} Min. – {status}")
                time.sleep(0.1)

    elif inner_choice == "3":
        cls()
        print("📰 Verfügbare Magazine:\n")
        for item in library.media_items:
            status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
            if isinstance(item, Magazine):
                print(f"- 📰 Magazine: {item.title} – {status}")
                time.sleep(0.1)          
    else:
        cls()
        print("❌ Falsche Eingabe")
    hold_until_user_exits()
def menu_search_articles(library):
    """
    Ermöglicht die Suche nach Medien anhand eines Titels oder Stichworts.

    Durchsucht alle Medien in `library` nach einem passenden Titel oder Teilstring.
    Zeigt gefundene Medien mit Typ, Titel, Zusatzinfos (z. B. Autor, Ausgabe) und Verfügbarkeitsstatus an.

    Args:
        library: Ein Objekt mit der Methode `searchItems`, das Medien durchsuchen kann.
    """
    cls()
    title = input("🔎 Titel oder Stichwort eingeben: ")
    found_items = library.searchItems(title)
    
    if found_items:
        print("📦 Gefundene Medien:")
        for item in found_items:
            status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
            item_type = item.type.capitalize()
            
            if item_type == "Book":
                print(f"- 📘 [Buch] {item.title} von {item.author} ({status})")
            elif item_type == "Dvd":
                print(f"- 📀 [DVD] {item.title}, Dauer: {item.duration} Min. ({status})")
            elif item_type == "Magazine":
                print(f"- 📰 [Magazin] {item.title}, Ausgabe: {item.issue} ({status})")
            else:
                print(f"- ❓ [Unbekannt] {item.title} ({status})")
        
        hold_until_user_exits()
    else:
        cls()
        print("⚠️ Kein Medium gefunden.")
        hold_until_user_exits()

def menu_add_article(library):
    """
    Fügt ein neues Medium (Buch, DVD oder Magazin) zur Bibliothek hinzu.

    Der Benutzer wählt den Medientyp und gibt die relevanten Informationen ein.
    Anschließend wird das neue Medienobjekt erstellt, automatisch mit einer UUID versehen
    und über `library.addMediaItem()` hinzugefügt.

    Args:
        library: Ein Objekt mit der Methode `addMediaItem`, das Medienobjekte speichern kann.
    """
    cls()
    print("📦 Medien hinzufügen:\n")
    print("1. Buch")
    print("2. DVD")
    print("3. Magazin")
    media_choice = input("\nWähle den Medientyp (1-3): ").strip()

    if media_choice not in {"1", "2", "3"}:
        print("❌ Ungültige Auswahl.")
        time.sleep(1.5)
        return

    cls()
    print("📝 Medieninformationen eingeben:\n")
    title = input("Titel: ").strip()
    if not title:
        print("❌ Titel darf nicht leer sein.")
        time.sleep(1.5)
        return

    # ID automatisch generieren
    next_id = str(uuid.uuid4())

    # === BUCH ===
    if media_choice == "1":
        author = input("Autor: ").strip()
        isbn = input("ISBN: ").strip()
        genre = input("Genre: ").strip()
        new_item = Book(next_id, title, author, isbn, genre)

    # === DVD ===
    elif media_choice == "2":
        duration = input("Dauer (in Minuten): ").strip()
        genre = input("Genre: ").strip()
        new_item = DVD(next_id, title, duration, genre)

    # === MAGAZIN ===
    elif media_choice == "3":
        issue = input("Ausgabe: ").strip()
        publisher = input("Verlag: ").strip()
        new_item = Magazine(next_id, title, issue, publisher)

    # Objekt hinzufügen
    library.addMediaItem(new_item)

    print(f"✅ {new_item.type.capitalize()} '{title}' wurde hinzugefügt.")
    hold_until_user_exits()


def menu_delete_article(library):
    """
    Öffnet ein Menü zur Auswahl eines Medientyps (Buch, DVD, Magazin) und ermöglicht das Löschen
    eines Mediums anhand seines Titels aus der Bibliothek.

    Parameter:
    - library: Das Bibliotheksobjekt, das eine Liste von Medieneinträgen (media_items) enthält.

    Der Nutzer wählt zunächst den Medientyp, sieht eine Liste der verfügbaren Titel und
    gibt dann den Titel des zu löschenden Mediums ein. Wenn der Titel gefunden wird,
    wird das Objekt aus den entsprechenden Listen entfernt.
    
    Unterstützte Medientypen:
    - Book
    - DVD
    - Magazine
    
    Hinweise:
    - Eingabe von Enter im Hauptmenü bricht den Vorgang ab.
    - Nach der Löschung wird eine Bestätigung ausgegeben.
    - Bei ungültiger Eingabe oder nicht gefundenem Titel erfolgt eine entsprechende Meldung.
    """
    
    cls()
    print("🗑️  Welchen Medientyp möchtest du löschen?\n")
    print("1. 📕 Buch")
    print("2. 📀 DVD")
    print("3. 📰 Magazin")

    media_choice = input("\nAuswahl (1–3 oder Enter zum Abbrechen): ").strip()
    if media_choice == "":
        print("🔙 Abbruch.")
        time.sleep(1.5)
        cls()
        return

    cls()

    if media_choice == "1":
        print("📕 Verfügbare Bücher:\n")
        found = False
        for item in library.media_items:
            if isinstance(item, Book):
                status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
                print(f"- 📘 {item.title} von {item.author} [{item.genre}] – {status}")
                found = True
                time.sleep(0.1)
        if not found:
            cls()
            print("⚠️ Keine Bücher im System.")
            hold_until_user_exits()
            return

        title = input("\n🗑️ Titel des zu löschenden Buchs: ").strip()
        book = next((i for i in library.media_items if isinstance(i, Book) and i.title.lower() == title.lower()), None)
        if book:
            library.media_items.remove(book)
            if book in library.books:
                library.books.remove(book)
                cls()
            print(f"✅ Buch '{book.title}' wurde gelöscht.")
        else:
            print("❌ Buch nicht gefunden.")

    elif media_choice == "2":
        print("📀 Verfügbare DVDs:\n")
        found = False
        for item in library.media_items:
            if isinstance(item, DVD):
                status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
                print(f"- 📀 {item.title}, Dauer: {item.duration} Min. – {status}")
                found = True
                time.sleep(0.1)
        if not found:
            print("⚠️ Keine DVDs im System.")
            hold_until_user_exits()
            return

        title = input("\n🗑️ Titel der zu löschenden DVD: ").strip()
        dvd = next((i for i in library.media_items if isinstance(i, DVD) and i.title.lower() == title.lower()), None)
        if dvd:
            library.media_items.remove(dvd)
            cls()
            print(f"✅ DVD '{dvd.title}' wurde gelöscht.")
        else:
            print("❌ DVD nicht gefunden.")

    elif media_choice == "3":
        print("📰 Verfügbare Magazine:\n")
        found = False
        for item in library.media_items:
            if isinstance(item, Magazine):
                status = "✅ Verfügbar" if item.available else "❌ Ausgeliehen"
                print(f"- 📰 {item.title}, Ausgabe: {item.issue} – {status}")
                found = True
                time.sleep(0.1)
        if not found:
            print("⚠️ Keine Magazine im System.")
            hold_until_user_exits()
            return

        title = input("\n🗑️ Titel des zu löschenden Magazins: ").strip()
        mag = next((i for i in library.media_items if isinstance(i, Magazine) and i.title.lower() == title.lower()), None)
        if mag:
            library.media_items.remove(mag)
            cls()
            print(f"✅ Magazin '{mag.title}' wurde gelöscht.")
        else:
            print("❌ Magazin nicht gefunden.")

    else:
        print("❌ Ungültige Auswahl. Abbruch.")
        time.sleep(1.5)

    hold_until_user_exits()
    cls()

    
def menu_remove_article_from_user(library):
    """
    Öffnet ein Menü, um einem Benutzer ein zuvor ausgeliehenes Medium zu entziehen
    und es in der Bibliothek wieder als verfügbar zu markieren.

    Parameter:
    - library: Das Bibliotheksobjekt, das eine Liste von Benutzern (library.users) enthält,
      von denen jeder ausgeliehene Medien in `borrowedItems` haben kann.

    Ablauf:
    - Zeigt eine Übersicht aller ausgeliehenen Medien je Benutzer.
    - Benutzername wird abgefragt.
    - Wenn Benutzer existiert und Medien ausgeliehen hat, wird der Titel des Mediums abgefragt.
    - Bei erfolgreichem Match wird das Medium zurückgebucht (via `returnItem`) und als verfügbar markiert.

    Hinweise:
    - Bei leerer Eingabe erfolgt ein Abbruch.
    - Fehlerhafte Namen oder Titel führen zu einer entsprechenden Meldung.
    - Die Funktion nimmt keine Änderungen an der Medienliste der Bibliothek vor, sondern nur an der Ausleihliste des Benutzers.
    """
    
    cls()
    print("📦 Medium von Benutzer entziehen:\n")

    # Prüfen, ob überhaupt etwas ausgeliehen ist
    any_loans = any(user.borrowedItems for user in library.users)
    if not any_loans:
        print("ℹ️  Es wurden keine Medien ausgeliehen.")
        hold_until_user_exits()
        return

    print("📖 === Übersicht: Ausgeliehene Medien ===")
    for user_in_list in library.users:
        if user_in_list.borrowedItems:
            items = ", ".join([f"{type(item).__name__}: {item.title}" for item in user_in_list.borrowedItems])
            print(f"- 👤 \033[1;38;5;214m{user_in_list.name}\033[0m – Ausgeliehen: \033[1;32m{items}\033[0m")

    print("\n⚠️  Abbrechen jederzeit mit leerer Eingabe (↩ Enter)\n")

    name = input("👤 Name des Benutzers: ").strip()
    if not name:
        cls()
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    # Benutzer finden
    target_user = next((u for u in library.users if u.name.lower() == name.lower()), None)
    if not target_user:
        print("❌ Benutzer nicht gefunden.")
        time.sleep(1.5)
        return

    if not target_user.borrowedItems:
        print(f"ℹ️ Benutzer '{target_user.name}' hat keine ausgeliehenen Medien.")
        time.sleep(1.5)
        return
    
    cls()
    print(f"\n📚 Ausgeliehene Medien von {target_user.name}:\n")
    for idx, item in enumerate(target_user.borrowedItems, 1):
        print(f"{idx}. {item.title} ({type(item).__name__})")

    title = input("\n🎯 Titel des Mediums zum Entziehen (↩ Enter für Abbruch): ").strip()
    if not title:
        cls()
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    # Gesuchtes Item finden
    item_to_remove = next((i for i in target_user.borrowedItems if i.title.lower() == title.lower()), None)

    if item_to_remove:
        cls()
        target_user.returnItem(item_to_remove)
        print(f"✅ Medium '{item_to_remove.title}' wurde von {target_user.name} entzogen.")
    else:
        print("❌ Medium nicht gefunden oder nicht ausgeliehen.")

    time.sleep(1.5)


def menu_user_list(library):
    """
    Zeigt eine Liste aller registrierten Benutzer mit ausgeliehenen Medien und Zeitstempeln.
    """

    cls()
    print("\n👥 Benutzerliste:")

    for user_in_list in library.users:
        items = []

        for item in user_in_list.borrowedItems:
            # Versuche, passenden Zeitstempel zu finden
            timestamp = user_in_list.borrowTimestamps.get(item.itemID, "⏳ Unbekannt")
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(timestamp)
                timestamp_str = dt.strftime("%d.%m.%Y – %H:%M Uhr")
            except Exception:
                timestamp_str = timestamp  # fallback

            item_type = type(item).__name__
            items.append(f"{item_type}: {item.title} (am {timestamp_str})")

        item_list = ", ".join(items) if items else "\033[37mKeine Medien ausgeliehen\033[0m"

        print(f"- \033[1;38;5;214m{user_in_list.name}\033[0m "
            f"(Alter: {user_in_list.age} | Rolle: {user_in_list.role}) – "
            f"Ausgeliehen: \033[1;32m{item_list}\033[0m")

    hold_until_user_exits()

def menu_change_role(library, user):
    """
    Ändert die Rolle eines anderen Benutzers (user, verwaltung, admin).
    """

    cls()
    print("👥 Benutzerrolle ändern:\n")

    print("📜 \033[37mAktive Benutzer:\033[0m")
    for u in library.users:
        if u.role == "user":    
            print(f"- \033[37m{u.name}\033[0m aktuelle Rolle: \033[1;32m{u.role}\033[0m")
            time.sleep(0.1)
        elif u.role == "verwaltung":
            print(f"- \033[37m{u.name}\033[0m aktuelle Rolle: \033[1;38;5;214m{u.role}\033[0m")
            time.sleep(0.1)
        elif u.role == "admin":
            print(f"- \033[37m{u.name}\033[0m aktuelle Rolle: \033[1;31m{u.role}\033[0m")
            time.sleep(0.1)

    print("\n↩️  (Leerlassen + ↩ Enter zum Abbrechen)")

    name = input("\nName des Benutzers: ").strip()
    if name == "":
        cls()
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    user_in_user_list = next((u for u in library.users if u.name.lower() == name.lower()), None)

    if user_in_user_list:
        if user == user_in_user_list:
            cls()
            print("❌ Du kannst deine eigene Rolle nicht ändern.")
            time.sleep(1.5)
            return

        print("\nVerfügbare Rollen: user, admin, verwaltung")
        new_role = input(f"Neue Rolle für {user_in_user_list.name}: ").strip().lower()

        if new_role not in ['user', 'admin', 'verwaltung']:
            print("❌ Ungültige Rolle. Keine Änderung vorgenommen.")
            time.sleep(1.5)
        else:
            cls()
            library.changeRole(user_in_user_list, new_role)
            print(f"✅ Rolle von {user_in_user_list.name} wurde zu '{new_role}' geändert.")
            time.sleep(1.5)

    else:
        print("❌ Benutzer nicht gefunden.")
        time.sleep(1.5)

def menu_add_user(library):
    """
    Fügt einen neuen Benutzer mit Name, Alter, Passwort und Rolle zur Bibliothek hinzu.
    """

    cls()
    print("👥 Benutzer hinzufügen\n↩️  Leerlassen + ↩ Enter zum Abbrechen\n")

    name = input("📝 Name: ").strip()
    if not name:
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    found_user = next((u for u in library.users if u.name.lower() == name.lower()), None)
    if found_user:
        print("❌ Benutzername ist bereits vergeben.")
        time.sleep(1.5)
        return

    while True:
        try:
            age_input = input("🎂 Alter: ").strip()
            if not age_input:
                print("❌ Abgebrochen.")
                time.sleep(1.5)
                break
            age = int(age_input)
            if 1 <= age <= 119:
                break
            else:
                print("❌ Ungültiges Alter (1–119).")
        except ValueError:
            print("❌ Bitte gib eine gültige Zahl ein.")
        time.sleep(1.5)

    password = input("🔑 Passwort: ").strip()
    if not password:
        print("❌ Passwort darf nicht leer sein.")
        time.sleep(1.5)
        return

    print("\nVerfügbare Rollen: user, admin, verwaltung")
    role = input("🛡️  Rolle: ").strip().lower()
    if role not in ['user', 'admin', 'verwaltung']:
        print("⚠️ Ungültige Rolle. Setze Standardrolle: 'user'.")
        role = 'user'
        time.sleep(1)

    user_id = max((u.userID for u in library.users), default=0) + 1
    new_user = User(user_id, name, age, password, role)
    library.addUser(new_user)

    cls()
    print(f"✅ Benutzer '{name}' wurde mit Rolle '{role}' erfolgreich hinzugefügt.")
    time.sleep(1.5)

def menu_delete_user(library, user):
    """
    Durchsucht die Benutzerdatenbank nach einem Namensteil und listet passende Benutzer auf.
    """

    cls()
    print("👥 Benutzer löschen:\n")
    
    print("📋 Aktuelle Benutzer:")
    for idx, u in enumerate(library.users, 1):
        print(f"{idx}. {u.name} (Rolle: {u.role})")

    print("\n⚠️  Eigene Löschung ist nicht erlaubt.")
    print("↩️  Abbrechen mit Enter\n")

    name = input("🗑️  Name des Benutzers, der gelöscht werden soll: ").strip()
    if name == "":
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    user_to_delete = next((u for u in library.users if u.name.lower() == name.lower()), None)

    if not user_to_delete:
        print("❌ Benutzer nicht gefunden.")
        time.sleep(1.5)
        return

    if user_to_delete == user:
        print("❌ Du kannst dich nicht selbst löschen.")
        time.sleep(1.5)
        return
    cls()
    confirm = input(f"⚠️  Bist du sicher, dass du '{user_to_delete.name}' löschen willst? (j/n): ").strip().lower()
    if confirm != "j":
        print("❌ Löschung abgebrochen.")
        time.sleep(1.5)
        return

    library.users.remove(user_to_delete)
    cls()
    print(f"✅ Benutzer '{user_to_delete.name}' wurde gelöscht.")
    time.sleep(1.5)

def menu_search_user(library):
    """
    Öffnet ein Suchmenü zur Benutzersuche basierend auf Namensfragmenten.
    
    Args:
        library (LibrarySystem): Das aktuelle Bibliothekssystem mit Benutzerliste.
    """

    cls()
    print("👥 Benutzer suchen\n↩️  Leerlassen zum Abbrechen\n")

    query = input("🔍 Suchbegriff (Teil des Namens): ").strip().lower()
    if not query:
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    matching_users = [u for u in library.users if query in u.name.lower()]

    if matching_users:
        cls()
        print(f"✅ Gefundene Benutzer ({len(matching_users)} Treffer):\n")
        for match in matching_users:
            print(f"- {match.name} (Rolle: {match.role})")
        hold_until_user_exits()
    else:
        cls()
        print("❌ Kein Benutzer gefunden.")
        time.sleep(1.5)

def menu_borrow_article(library, user):
    """
    Öffnet ein Menü zur Auswahl eines Medientyps und ermöglicht dem Benutzer das Ausleihen eines Mediums.
    
    Args:
        library (LibrarySystem): Das aktuelle Bibliothekssystem mit Medienbestand.
        user (User): Der aktuell angemeldete Benutzer, der das Medium ausleihen möchte.
    """

    cls()
    print("🎁 Welchen Medientyp möchtest du ausleihen?\n")
    print("1. 📘 Buch")
    print("2. 📀 DVD")
    print("3. 📰 Magazin")
    print("↩️  Leerlassen zum Abbrechen\n")

    media_choice = input("Bitte gib die Zahl ein (1-3): ").strip()

    if media_choice == "":
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    media_type_map = {
        "1": Book,
        "2": DVD,
        "3": Magazine
    }

    selected_class = media_type_map.get(media_choice)

    if not selected_class:
        print("❌ Ungültige Auswahl.")
        time.sleep(1.5)
        return

    cls()
    print(f"🔍 Verfügbare {selected_class.__name__}s:\n")

    available_items = [item for item in library.media_items if isinstance(item, selected_class) and item.available]

    if not available_items:
        print("⚠️ Keine Medien dieses Typs verfügbar.")
        hold_until_user_exits()
        return

    for item in available_items:
        if isinstance(item, Book):
            print(f"- 📘 {item.title} von {item.author} [{item.genre}]")
        elif isinstance(item, DVD):
            print(f"- 📀 {item.title}, Dauer: {item.duration} Min.")
        elif isinstance(item, Magazine):
            print(f"- 📰 {item.title}, Ausgabe: {item.issue}")

    title = input("\n🎯 Titel des Mediums (↩ Enter zum Abbrechen): ").strip()
    if not title:
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    item = next((i for i in available_items if i.title.lower() == title.lower()), None)

    if not item:
        print("❌ Medium nicht gefunden oder bereits ausgeliehen.")
        time.sleep(1.5)
        return

    # Spezielle Regel für Bücher
    if isinstance(item, Book) and len(user.borrowedItems) >= 3:
        print("❌ Du kannst maximal 3 Bücher ausleihen.")
        time.sleep(1.5)
        return

    # Ausleihe durchführen
    user.borrowItem(item)
    cls()
    print(f"✅ '{item.title}' wurde ausgeliehen.")
    time.sleep(1)

def menu_show_own_items(user):
    """
    Zeigt alle vom Benutzer ausgeliehenen Medien mit Ausleihzeitpunkt an.
    
    Args:
        user (User): Der aktuell angemeldete Benutzer.
    """

    cls()
    print("📚 \033[1;37mDeine ausgeliehenen Medien:\033[0m\n")

    if not user.borrowedItems:
        print("⚠️ Du hast keine Medien ausgeliehen.")
        hold_until_user_exits()
        return

    for idx, item in enumerate(user.borrowedItems, 1):
        timestamp = user.borrowTimestamps.get(item.itemID, "⏳ Unbekannt")
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp)
            timestamp_str = dt.strftime("%d.%m.%Y – %H:%M Uhr")
        except Exception:
            timestamp_str = timestamp

        if isinstance(item, Book):
            print(f"{idx}. 📘 Buch: \033[33m{item.title}\033[0m von {item.author} (ISBN: {item.isbn}) – ausgeliehen am {timestamp_str}")
        elif isinstance(item, DVD):
            print(f"{idx}. 📀 DVD: \033[36m{item.title}\033[0m, Dauer: {item.duration} Min. – ausgeliehen am {timestamp_str}")
        elif isinstance(item, Magazine):
            print(f"{idx}. 📰 Magazin: \033[35m{item.title}\033[0m, Ausgabe: {item.issue} – ausgeliehen am {timestamp_str}")
        else:
            print(f"{idx}. ❓ Unbekanntes Medium: {item.title} – ausgeliehen am {timestamp_str}")

    hold_until_user_exits()

def menu_return_book(user):
    """
    Ermöglicht dem Benutzer die Rückgabe eines zuvor ausgeliehenen Buchs.
    
    Args:
        user (User): Der aktuell angemeldete Benutzer.
    """

    cls()
    print("📕 \033[1;37mDeine ausgeliehenen Bücher:\033[0m\n")

    # Filtere nur ausgeliehene Bücher
    borrowed_books = [item for item in user.borrowedItems if isinstance(item, Book)]

    if not borrowed_books:
        print("⚠️ Du hast keine Bücher ausgeliehen.")
        hold_until_user_exits()
        return

    for idx, book in enumerate(borrowed_books, 1):
        timestamp = user.borrowTimestamps.get(book.itemID, "⏳ Unbekannt")
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(timestamp)
            timestamp_str = dt.strftime("%d.%m.%Y – %H:%M Uhr")
        except Exception:
            timestamp_str = timestamp
        print(f"{idx}. \033[33m{book.title}\033[0m von {book.author} – ausgeliehen am {timestamp_str}")

    print("\n↩️  Verlassen mit Enter")

    title = input("\n📘 Titel des Buches, das du zurückgeben möchtest: ").strip()
    if not title:
        print("❌ Abgebrochen.")
        time.sleep(1.5)
        return

    book = next((b for b in borrowed_books if b.title.lower() == title.lower()), None)

    if book:
        user.returnItem(book)
        cls()
        print(f"✅ Buch '{book.title}' wurde zurückgegeben.")
        time.sleep(1.5)
    else:
        print("❌ Buch nicht gefunden.")
        time.sleep(1.5)

def log_out():
    """
    Führt den Logout-Vorgang durch und zeigt eine Bestätigung an.
    """

    cls()
    loading_screen(0.4)
    cls()
    print("👋 Log-out erfolgreich.")
    time.sleep(1.2)

def login(library):
    """
    Führt die Benutzeranmeldung durch oder ermöglicht eine Neuregistrierung.
    
    Args:
        library (LibrarySystem): Das Bibliothekssystem zur Benutzerüberprüfung.
    
    Returns:
        User: Der angemeldete oder neu registrierte Benutzer.
    """

    while True:
        cls()
        print("🔐 === Anmeldung zum LibrarySystem ===")

        # Sicherstellen, dass der Name nicht leer ist
        name = input("👤 Bitte gib deinen Namen ein: ").strip()
        if not name:
            cls()
            print("⚠️ Name darf nicht leer sein.")
            time.sleep(1.5)
            continue

        # Benutzernameprüfung
        if library.username_exists(name):
            user = next((u for u in library.users if u.name.lower() == name.lower()), None)
            if user:
                password = input("🔑 Bitte gib dein Passwort ein: ").strip()
                if not password:
                    print("⚠️ Passwort darf nicht leer sein.")
                    time.sleep(1.5)
                    continue

                if user.password == password:
                    cls()
                    print(f"✅ Willkommen zurück, {user.name}!")
                    time.sleep(2)
                    loading_screen(1)
                    return user  # Rückgabe des Benutzers
                else:
                    print("⚠️ Falsches Passwort. Bitte versuche es erneut.")
                    time.sleep(1.5)
            else:
                print(f"⚠️ Benutzer '{name}' nicht gefunden.")
        else:
            print(f"⚠️ Benutzername '{name}' ist nicht registriert.")
            create = input("Möchtest du dich registrieren? (j/n): ").strip().lower()
            if create == 'j':
                age = input("Alter: ").strip()
                if not age.isdigit():
                    print("⚠️ Ungültiges Alter. Bitte erneut versuchen.")
                    time.sleep(1.5)
                    continue

                password = input("Passwort: ").strip()
                if not password:
                    print("⚠️ Passwort darf nicht leer sein.")
                    time.sleep(1.5)
                    continue

                try:
                    user_id = max([u.userID for u in library.users]) + 1 if library.users else 1
                    new_user = User(user_id, name, int(age), password)
                    library.addUser(new_user)
                    print(f"✅ Willkommen im System, {name}!")
                    return new_user
                except ValueError:
                    print("⚠️ Fehler bei der Registrierung. Bitte erneut versuchen.")
                    time.sleep(1.5)
            else:
                print("🔁 Versuche es erneut.")
                time.sleep(1.5)

def snake_type_shii():
    """
    Easter Egg - input: _EE_ um es auszulösen.
    """
    print(r"""
             ____
           /      \_____ 
          /    ^    \    \__
         /           \      \_      
        /      / \     \       \_
       /      /   \     \        \
      /      /     \     \        |
     /      /       \_____\_______|
    /      /                 \      \
   /      /                   \      \
  /      /                     \      \
 /      /                       \      \
/      /                         \      \
\     /                           \      \
 \   /                             \      \
  \_/                               \     |
         ___                     ____|____|____
        /   \                   /   ^     ^    \
       |     |                 |    o     o     | ~~~ 'IM A sSsSsSNAKEEE!'
        \___/                   \   \_______/   /
                                 \_____________/    
          
    """)
    hold_until_user_exits()