# Importiere tkinter für GUI
import tkinter as tk
# Importiere threading für paralleles Ausführen (z. B. Server-Listener im Hintergrund)
import threading
# Importiere Netzwerkfunktionen für Client-Seite
from clientnetwork import listenServer, retrievePlayers, sock
import time
import socket
import json



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
        self.searching = True
        self.wait_for_start = True
        threading.Thread(target=listenServer, args=(server_address, self.show_game, self.server_listbox), daemon=True).start()
        

    # Methode zum Hinzufügen eines Clients zur Listbox
    def add_client(self, client_address):
        # Namen aus dem Server holen, falls vorhanden
        name = None
        if hasattr(self, "game_server") and hasattr(self.game_server, "client_names"):
            name = self.game_server.client_names.get(client_address)
        if name:
            self.server_listbox.insert(tk.END, f"Spieler: {name}")
        else:
            self.server_listbox.insert(tk.END, f"Client: {client_address[0]}:{client_address[1]}")
    
    def show_game(self, fragen=None):
        self.after(0, lambda: self.parent.show_game(fragen, "client"))  # Zeigt das Spiel an, wenn die Fragen empfangen wurden

    # Funktion, die im Thread läuft: Spieler abrufen und auf neue Spieler warten



    # Wenn der Zurück-Button gedrückt wird
    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Versucht, das Event zu setzen (Problem: self.game_server existiert hier nicht!)
        self.waitThread.join()  # Wartet auf das Ende des Threads
        self.parent.show_servercreate()  # Geht zurück zum Spiel-Erstellungs-Bildschirm
