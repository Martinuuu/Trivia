import tkinter as tk
import threading
from servernetwork import Server


class TriviaServerWait(tk.Frame):
    def __init__(self, parent, game_name, game_category):
        super().__init__(parent)    
        self.parent = parent
        self.parent.geometry("550x300")
        parent.title(f"{game_name} - {game_category}")
        self.game_server = Server(game_name, game_category, client_callback=self.callback_handler)

        # Zurück-Button
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Fixe Position oben links

        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()
        
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        self.startButton = tk.Button(self, text="Spiel Starten", command=self.start_game)
        self.startButton.pack(pady=10)

        self.stop_event = threading.Event()
        self.waitThread = threading.Thread(target=self.game_server.waitConnection, daemon=True)
        self.waitThread.start()

    def callback_handler(self, command, *args):
        if command == "CONNECT_GAME":
            self.add_client(args[0])
        elif command == "LEAVE_GAME":
            self.remove_client(args[0])

    def add_client(self, client_address):
        self.server_listbox.insert(tk.END, f"Client: {client_address[0]}:{client_address[1]}")

    def remove_client(self, client_address):
        target = f"Client: {client_address[0]}:{client_address[1]}"
        index = self.server_listbox.get(0, tk.END).index(target)
        self.server_listbox.delete(index)

    def start_game(self):
        self.game_server.startGame()
        self.parent.show_game(self.game_server)

    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Stop-Event setzen, um die Schleife zu beenden
        self.waitThread.join()  # Warten, bis der Thread beendet ist
        self.parent.show_servercreate()  # Zurück zum Create-Fenster










