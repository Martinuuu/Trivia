import tkinter as tk
from tkinter import messagebox
from clientnetwork import checkServer

class TriviaClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Spiel")
        self.root.geometry("400x300")

        self.create_server = tk.Button(root, text="Server Erstellen")
        self.create_server = tk.Button(root, text="Server Erstellen")

        self.label = tk.Label(root, text="Gefundene Server:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.server_listbox = tk.Listbox(root, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.BOTH, expand=True, padx=20)

        self.refresh_button = tk.Button(root, text="Nach Servern suchen", command=self.suche_server)
        self.refresh_button.pack(pady=10)

    def suche_server(self):
        self.server_listbox.delete(0, tk.END)
        try:
            server_liste = checkServer()
            if server_liste is not None:
                for eintrag in server_liste:
                    self.server_listbox.insert(tk.END, eintrag)
            else:
                messagebox.showinfo("Kein Server gefunden", "Es wurde kein Spielserver gefunden.")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaClient(root)
    root.mainloop()
