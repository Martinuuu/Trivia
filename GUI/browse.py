import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from clientnetwork import checkServer, connectToGame

class TriviaClientBrowse(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Zurück-Button
        back = tk.Button(self, text="←", command=parent.show_start, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Fixe Position oben links

        # Label
        label = tk.Label(self, text="Gefundene Server:", font=("Arial", 12))
        label.pack(pady=10)

        # Listbox
        self.server_listbox = tk.Listbox(self, font=("Arial", 10))
        self.server_listbox.pack(fill=tk.BOTH, expand=True, padx=20)

        # Refresh-Button
        refresh_button = tk.Button(self, text="Nach Servern suchen", command=self.search_server)
        refresh_button.pack(pady=10)

        join_button = tk.Button(self, text="Server Beitreten", command=self.join_server)
        join_button.pack(pady=10)
        self.search_server()

    def search_server(self):
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

    def join_server(self):
        try:
            # Name abfragen
            name = simpledialog.askstring("Name eingeben", "Bitte gib deinen Spielernamen ein:")
            if not name or name.strip() == "":
                tk.messagebox.showerror("Fehler", "Du musst einen Namen eingeben!")
                return

            server_adress = self.server_listbox.get(self.server_listbox.curselection()[0]).split(":")[-1].strip()
            print("Versuche zu verbinden mit:", server_adress)
            result = connectToGame(server_adress, name)  # Name mitgeben!
            print("connectToGame Ergebnis:", result)
            if result:
                self.parent.show_clientwait(server_adress)
            else:
                tk.messagebox.showerror("Fehler", "Verbindung zum Server fehlgeschlagen!")
        except Exception as e:
            tk.messagebox.showerror("Fehler", f"Fehler beim Beitreten: {e}")

