import tkinter as tk
import threading
from servernetwork import Server


class TriviaServerWait(tk.Frame):
    def __init__(self, parent, game_name, game_categorie):
        super().__init__(parent)    
        self.parent = parent
        parent.title(f"{game_name} - {game_categorie}")

        # Zurück-Button
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Fixe Position oben links

        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()
        
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        self.game_server = Server(game_name, game_categorie)

        self.stop_event = threading.Event()
        self.waitThread = threading.Thread(target=self.game_server.waitConnection, daemon=True)
        self.waitThread.start()

    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Stop-Event setzen, um die Schleife zu beenden
        self.waitThread.join()  # Warten, bis der Thread beendet ist
        self.parent.show_servercreate()  # Zurück zum Create-Fenster










