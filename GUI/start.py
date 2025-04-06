import tkinter as tk

class TriviaClient(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title("Trivia Spiel")
        self.parent.geometry("400x300")

        self.create_server = tk.Button(self, text="Einen Spielserver erstellen", command=parent.show_servercreate)
        self.create_server.pack(pady=10)

        self.browse_server = tk.Button(self, text="Einen Spielserver suchen", command=parent.show_serverbrowse)
        self.browse_server.pack(pady=10)