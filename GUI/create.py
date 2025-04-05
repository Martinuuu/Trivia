import tkinter as tk
import threading
from trivia_api import get_categories

class TriviaServerCreate(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)    
        self.parent = parent

        # Widgets an `self` binden
        name_label = tk.Label(self, text="Servername:")
        name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.options = tk.StringVar(self)
        self.options.set("Lade Kategorien...")
        self.options_menu = tk.OptionMenu(self, self.options, "Lade Kategorien...")
        self.options_menu.pack()

        tk.Button(self, text="Fertig", command=self.submit).pack()

        # Kategorien im Hintergrund laden
        threading.Thread(target=self.load_categories, daemon=True).start()

    def submit(self):
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






