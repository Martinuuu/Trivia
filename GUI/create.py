import tkinter as tk
import threading
from trivia_api import get_categories

class TriviaServerCreate(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)    
        self.parent = parent

        # Zurück-Button
        back = tk.Button(self, text="←", command=parent.show_start, width=2, height=1, font=("Arial", 10))
        back.place(x=10, y=10)  # Fixe Position oben links
        
        name_label = tk.Label(self, text="Servername:")
        name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.options = tk.StringVar(self)
        self.options.set("Lade Kategorien...")
        self.options_menu = tk.OptionMenu(self, self.options, "Lade Kategorien...")
        self.options_menu.pack()
        self.options_menu.config(state=tk.DISABLED)

        self.submit_button = tk.Button(self, text="Fertig", command=self.submit)
        self.submit_button.pack()

        # Kategorien im Hintergrund laden
        threading.Thread(target=self.load_categories, daemon=True).start()

    def submit(self):
        if(self.name_entry.get() == ""):
            tk.messagebox.showerror("Fehler", "Bitte einen Namen eingeben.")
            return
        if(self.options.get() == "Kategorie auswählen"):
            tk.messagebox.showerror("Fehler", "Bitte eine Kategorie auswählen.")
            return
        if(self.options.get() == "Lade Kategorien..."):
            tk.messagebox.showerror("Fehler", "Bitte warten bis die Kategorien geladen sind.")
            return
        if(self.options.get() == "Keine Kategorie gefunden"):
            tk.messagebox.showerror("Fehler", "Bitte eine Kategorie auswählen.")
            return
        game_name = self.name_entry.get()
        game_category = self.options.get()
        self.parent.show_serverwait(game_name, game_category)

    def load_categories(self):
        categories = get_categories()
        
        menu = self.options_menu["menu"]
        menu.delete(0, "end") 
        
        self.options.set("Kategorie auswählen")
        for categorie in categories:
            menu.add_command(label=categorie[1], command=lambda value=categorie[1]: self.options.set(value))
        self.options_menu.config(state=tk.NORMAL)






