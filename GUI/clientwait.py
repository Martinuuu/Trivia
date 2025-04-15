# Importiere tkinter für GUI
import tkinter as tk
# Importiere threading für paralleles Ausführen (z. B. Server-Listener im Hintergrund)
import threading
# Importiere Netzwerkfunktionen für Client-Seite
from clientnetwork import listenServer, retrievePlayers


# Klasse für den "Warten auf Spielstart"-Bildschirm des Clients
class TriviaClientWait(tk.Frame):
    def __init__(self, parent, server_address):
        super().__init__(parent)
        self.parent = parent

        # Setze Fenstergröße
        self.parent.geometry("550x300")

        # Speichere die Serveradresse (z. B. IP + Port)
        self.server_address = server_address

        # Zurück-Button oben links
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Positioniere den Button oben links

        # Überschrift für die Spieleranzeige
        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()

        # Listbox zur Anzeige der verbundenen Clients
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        # Start-Button ist hier auskommentiert, da der Client nicht das Spiel startet
        # self.startButton = tk.Button(self, text="Spiel Starten", command=self.start_game)
        # self.startButton.pack(pady=10)

        # Event, um das Beenden des Threads zu ermöglichen
        self.stop_event = threading.Event()

        # Starte einen Thread, der mit dem Server kommuniziert
        self.waitThread = threading.Thread(target=self.server_listen, daemon=True)
        self.waitThread.start()

    # Methode zum Hinzufügen eines Clients zur Listbox
    def add_client(self, client_address):
        self.server_listbox.insert(tk.END, f"Client: {client_address}")

    # Funktion, die im Thread läuft: Spieler abrufen und auf neue Spieler warten
    def server_listen(self):
        print("testmest")  # Debug-Ausgabe
        clients = retrievePlayers(self.server_address)  # Hole aktuell verbundene Spieler vom Server
        print("Clients: " + str(clients))  # Debug-Ausgabe
        for client in clients:
            self.add_client(client)  # Zeige alle vorhandenen Spieler an
        # Lausche auf neue Spieler, die sich verbinden, und füge sie mit add_client hinzu
        listenServer(self.server_address, self.add_client)

    # Wenn der Zurück-Button gedrückt wird
    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Versucht, das Event zu setzen (Problem: self.game_server existiert hier nicht!)
        self.waitThread.join()  # Wartet auf das Ende des Threads
        self.parent.show_servercreate()  # Geht zurück zum Spiel-Erstellungs-Bildschirm
