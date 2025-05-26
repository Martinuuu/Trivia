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

        self.after_id = None  # ID für die wiederkehrende Abfrage

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
        self.stop_event = threading.Event()
        self.listener_thread = threading.Thread(
            target=self.listen_wrapper, daemon=True
        )
        self.listener_thread.start()

    def listen_wrapper(self):
        def gui_callback_in_main_thread(fragen):
            # Callback wird IMMER im Tkinter-Hauptthread ausgeführt
            self.after(0, lambda: self.show_game(fragen))
        listenServer(self.server_address, gui_callback_in_main_thread, self.server_listbox, self.stop_event)

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
        # Stoppe Listener und Timer, bevor das Frame gewechselt wird!
        self.stop_event.set()
        if hasattr(self, "listener_thread") and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        if hasattr(self, "after_id") and self.after_id is not None:
            try:
                if self.winfo_exists():
                    self.after_cancel(self.after_id)
            except Exception as e:
                print("Error cancelling after_id in show_game: ", e)
            self.after_id = None
        self.parent.show_game(fragen, "client")

    # Funktion, die im Thread läuft: Spieler abrufen und auf neue Spieler warten



    # Wenn der Zurück-Button gedrückt wird
    def back(self):
        self.parent.show_serverbrowse()  # Geht zurück zum Spiel-Erstellungs-Bildschirm

    def destroy(self):
        self.stop_event.set()
        if hasattr(self, "listener_thread") and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        if hasattr(self, "after_id") and self.after_id is not None:
            try:
                if self.winfo_exists() and self.tk.call("after", "info", self.after_id):
                    self.after_cancel(self.after_id)
            except Exception as e:
                print("Error cancelling after_id: ", e)
            self.after_id = None
        super().destroy()
