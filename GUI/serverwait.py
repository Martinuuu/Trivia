import tkinter as tk
import threading
from servernetwork import Server


class TriviaServerWait(tk.Frame):
    def __init__(self, parent, game_name, game_categorie):
        super().__init__(parent)    
        self.parent = parent
        parent.title(f"{game_name} - {game_categorie}")

        self.label = tk.Label(self, text="Verbundene Spieler:")
        self.label.pack()
        
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.X, expand=True, padx=20)

        self.game_server = Server(game_name, game_categorie)

        threading.Thread(target=self.wait, daemon=True).start()



    def wait(self):
        self.game_server.waitConnection()
        
        


        

       


    
