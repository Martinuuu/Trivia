import tkinter as tk
import threading
from clientnetwork import listenServer, retrievePlayers


class TriviaClientWait(tk.Frame):
    def __init__(self, parent, server_address):
        super().__init__(parent)    
        self.parent = parent
        self.parent.geometry("550x300")
        #parent.title(f"{game_name} - {game_category}")
        
        self.server_address = server_address
        

        # Zurück-Button
        back = tk.Button(self, text="←", command=self.back, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Fixe Position oben links

        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()
        
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        # self.startButton = tk.Button(self, text="Spiel Starten", command=self.start_game)
        # self.startButton.pack(pady=10)

        self.stop_event = threading.Event()
        self.waitThread = threading.Thread(target=self.server_listen, daemon=True)
        self.waitThread.start()

    def add_client(self, client_address):
        self.server_listbox.insert(tk.END, f"Client: {client_address}")


    def server_listen(self):
        print("testmest")
        clients = retrievePlayers(self.server_address)
        print("Clients: "+ str(clients))
        for client in clients:
            self.add_client(client)
        listenServer(self.server_address, self.add_client)


    def back(self):
        print("Stopping Wait")
        self.game_server.stop_event.set()  # Stop-Event setzen, um die Schleife zu beenden
        self.waitThread.join()  # Warten, bis der Thread beendet ist
        self.parent.show_servercreate()  # Zurück zum Create-Fenster