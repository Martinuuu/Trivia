# Importiere tkinter für die GUI
import tkinter as tk
# Importiere threading für paralleles Ausführen (z. B. Clients verbinden, ohne GUI zu blockieren)
import threading
# Importiere den Server aus dem servernetwork-Modul
from servernetwork import Server

# Klasse für den "Warten auf Spieler"-Bildschirm des Servers
class TriviaServerWait(tk.Frame):
    def __init__(self, parent, game_name, game_category):
        super().__init__(parent)    
        self.parent = parent

        # Setze die Fenstergröße
        self.parent.geometry("550x300")
        # Setze den Fenstertitel auf "Spielname - Kategorie"
        parent.title(f"{game_name} - {game_category}")

        # Erzeuge den Spielserver mit Callback-Funktion für Client-Aktionen
        self.game_server = Server(game_name, game_category, client_callback=self.callback_handler)

        # Zurück-Button oben links
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Positioniere den Button oben links

        # Beschriftung für die Liste der verbundenen Spieler
        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()
        
        # Listbox zum Anzeigen der verbundenen Clients
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        # Button zum Starten des Spiels
        self.startButton = tk.Button(self, text="Spiel Starten", command=self.start_game)
        self.startButton.pack(pady=10)

        # Event-Objekt zum sauberen Beenden des Threads
        self.stop_event = threading.Event()
        # Starte den Server-Thread zum Warten auf Clients (als Daemon-Thread, damit er beim Schließen endet)
        self.waitThread = threading.Thread(target=self.game_server.waitConnection, daemon=True)
        self.waitThread.start()

    # Callback-Funktion für den Server (wird aufgerufen, wenn Clients beitreten oder verlassen)
    def callback_handler(self, command, *args):
        if command == "CONNECT_GAME":
            self.add_client(args[0])  # Neuer Client verbunden
        elif command == "LEAVE_GAME":
            self.remove_client(args[0])  # Client hat verlassen
        elif command == "UPDATE_GUI":
            frage, scores = args
            self.update_game_state(frage, scores)

    # Fügt einen Client zur Listbox hinzu
    def add_client(self, client_address):
        self.server_listbox.insert(tk.END, f"Client: {client_address[0]}:{client_address[1]}")

    # Entfernt einen Client aus der Listbox
    def remove_client(self, client_address):
        target = f"Client: {client_address[0]}:{client_address[1]}"
        index = self.server_listbox.get(0, tk.END).index(target)  # Finde den Index des Clients
        self.server_listbox.delete(index)  # Entferne den Eintrag aus der Liste

    # Startet das Spiel, wenn der Button geklickt wird
    def start_game(self):
        self.game_server.startGame()  # Informiere alle Clients, dass das Spiel startet
        self.parent.show_game(self.game_server.fragen, "server")  # Wechsle zur Spielansicht und übergebe den Server

    # Zurück-Button wurde gedrückt
    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Setzt das Stop-Event, damit der Server-Thread aufhört
        self.waitThread.join()  # Wartet auf sauberes Beenden des Threads
        self.parent.show_servercreate()  # Geht zurück zum Erstellen-Bildschirm

    def update_game_state(self, frage, scores):
        if not hasattr(self, "label") or not self.winfo_exists():
            return  # Frame oder Label existiert nicht mehr, also kein Update!
        try:
            self.label.config(text=f"Frage: {frage['question']}")
            self.server_listbox.delete(0, tk.END)
            for addr, score in scores.items():
                self.server_listbox.insert(tk.END, f"{addr[0]}:{addr[1]} - Punkte: {score}")
        except tk.TclError:
            # Widget wurde zerstört
            pass