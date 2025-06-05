##################################
# LibrarySystem.py MAIN FUNCTION #
##################################

import time
from utils.external_functions import (
    cls,
    menu_borrow_article,
    menu_search_user,
    menu_delete_user,
    menu_add_user,
    menu_change_role,
    menu_user_list,
    menu_remove_article_from_user,
    menu_delete_article,
    loading_screen,
    hold_until_user_exits,
    snake_type_shii,
    login,
    log_out,
    menu_search_articles,
    menu_show_articles,
    menu_show_own_items,
    menu_add_article,
    menu_return_book,
)

from utils.class_media_items import (
    MediaItem,
    Book,
    Magazine,
    DVD    
)

from utils.class_users import (
    User,
    Author
)

from utils.class_librarySystem import (
    LibrarySystem
)

def main_menu(library, user):
    """
    Zeigt das Hauptmenü basierend auf der Benutzerrolle (admin, verwaltung, user)
    und verarbeitet Benutzereingaben, um entsprechende Funktionen auszuführen.

    Parameter:
        library (LibrarySystem): Das Bibliothekssystem-Objekt, das Artikel- und Benutzerdaten verwaltet.
        user (User): Das aktuell angemeldete Benutzerobjekt mit zugehöriger Rolle.

    Rückgabe:
        str oder None: Gibt "switch" zurück, wenn der Benutzer sich ausloggt,
                       None bei Beenden des Programms.
    """
    while True:
        cls()
        if user.role == 'admin':
            # Admin-Menü mit erweiterten Verwaltungsfunktionen
            print(f"📚 === \033[32mLibrarySystem \033[1;31m<ADMIN CONSOLE>\033[0m ===\n")
            print("1. Alle Artikel anzeigen")
            print("2. Artikel suchen")
            print("3. Artikel hinzufügen")
            print("4. Artikel löschen")
            print("5. Artikel von Benutzer entziehen")
            print("6. Alle Benutzer | Ausgeliehene Bücher")
            print("7. Benutzerrolle ändern")
            print("8. Benutzer hinzufügen")
            print("9. Benutzer löschen")
            print("10. Benutzer suchen")
            print("11. Log-out")
            print("12. Beenden\n")
            choice = input("Bitte Auswahl eingeben (1-12): ")

            # Auswahlverarbeitung
            if choice == "1":
                menu_show_articles(library)
            elif choice == "2":
                menu_search_articles(library)
            elif choice == "3":
                menu_add_article(library)
            elif choice == "4":
                menu_delete_article(library)
            elif choice == "5":
                menu_remove_article_from_user(library)
            elif choice == "6":
                menu_user_list(library)
            elif choice == "7":
                menu_change_role(library, user)
            elif choice == "8":
                menu_add_user(library)
            elif choice == "9":
                menu_delete_user(library, user)
            elif choice == "10":
                menu_search_user(library)
            elif choice == "11":
                log_out()
                return "switch"
            elif choice == "12":
                return
            elif choice == "_EE_":
                cls()
                snake_type_shii()
            else:
                cls()
                print("⚠️ Ungültige Eingabe. Bitte erneut versuchen.")
                time.sleep(1)

        elif user.role == 'verwaltung':
            # Menü für Verwaltungsnutzer
            print(f"📚 === \033[32mWillkommen im LibrarySystem \033[1;38;5;214m{user.name}\033[0m! ===\n")
            print("1. Alle Artikel anzeigen")
            print("2. Artikel suchen")
            print("3. Artikel ausleihen")
            print("4. Artikel zurückgeben")
            print("5. Artikel hinzufügen")
            print("6. Artikel löschen")
            print("7. Meine Artikel")
            print("8. Alle Benutzer anzeigen")
            print("9. Benutzer hinzufügen")
            print("10. Benutzer löschen")
            print("11. Log-out")
            print("12. Beenden\n")
            choice = input("Bitte Auswahl eingeben (1-12): ")

            if choice == "1":
                menu_show_articles(library)
            elif choice == "2":
                menu_search_articles(library)
            elif choice == "3":
                menu_borrow_article(library, user)
            elif choice == "4":
                menu_return_book(user)
            elif choice == "5":
                menu_add_article(library)
            elif choice == "6":
                menu_delete_article(library)
            elif choice == "7":
                menu_show_own_items(user)
            elif choice == "8":
                menu_user_list(library)
            elif choice == "9":
                menu_add_user(library)
            elif choice == "10":
                menu_delete_user(library, user)
            elif choice == "11":
                log_out()
                return "switch"
            elif choice == "12":
                return
            elif choice == "_EE_":
                cls()
                snake_type_shii()
            else:
                cls()
                print("⚠️ Ungültige Eingabe. Bitte erneut versuchen.")
                time.sleep(1)

        elif user.role == 'user':
            # Menü für normale Benutzer
            print(f"📚 === \033[32mWillkommen im LibrarySystem \033[1;38;5;214m{user.name}\033[0m! ===\n")
            print("1. Alle Artikel anzeigen")
            print("2. Artikel suchen")
            print("3. Meine Artikel")
            print("4. Artikel ausleihen")
            print("5. Artikel zurückgeben")
            print("6. Log-out")
            print("7. Beenden\n")
            choice = input("Bitte Auswahl eingeben (1-7): ")

            if choice == "1":
                menu_show_articles(library)
            elif choice == "2":
                menu_search_articles(library)
            elif choice == "3":
                menu_show_own_items(user)
            elif choice == "4":
                menu_borrow_article(library, user)
            elif choice == "5":
                menu_return_book(user)
            elif choice == "6":
                log_out()
                return "switch"
            elif choice == "7":
                cls()
                print("👋 Programm beendet.")
                time.sleep(1)
                break
            elif choice == "_EE_":
                cls()
                snake_type_shii()
            else:
                cls()
                print("⚠️ Ungültige Eingabe. Bitte erneut versuchen.")
                time.sleep(1)
        else:
            print("⚠️ Ungültige Eingabe. Bitte erneut versuchen.")
            time.sleep(1)

if __name__ == "__main__":
    """
    Einstiegspunkt des Programms:
    - Lädt Medien- und Benutzerdaten aus JSON-Dateien.
    - Führt die Benutzer-Authentifizierung durch.
    - Leitet zum Hauptmenü entsprechend der Rolle des Benutzers weiter.
    - Speichert alle Änderungen beim Beenden.
    """
    library = LibrarySystem()
    library.load_media_from_json()
    library.load_users_from_json()

    try:
        while True:
            user = login(library)
            result = main_menu(library, user)
            if result != "switch":
                break
            else:
                continue
    except KeyboardInterrupt:
        cls()
    finally:
        # Daten werden beim Beenden gespeichert
        cls()
        print("🔴 Das Programm wird jetzt beendet...")
        time.sleep(1)
        loading_screen(1)
        library.save_media_to_json()
        library.save_users_to_json()
        time.sleep(0.2)
        cls()
        print("✅ Daten erfolgreich gespeichert.")
        time.sleep(1.4)
        cls()