# Importiere das tkinter-Modul für die GUI-Erstellung
import tkinter as tk

# Importiere die verschiedenen GUI-Komponenten aus den Untermodulen
from GUI.start import TriviaClient
from GUI.browse import TriviaClientBrowse
from GUI.create import TriviaServerCreate
from GUI.serverwait import TriviaServerWait
from GUI.clientwait import TriviaClientWait
from GUI.game import TriviaGame

# Hauptklasse der Anwendung, die von tk.Tk erbt (dem Hauptfenster)
class App(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialisiert das tk.Tk-Fenster
        self.title("Trivia Spiel")  # Setzt den Fenstertitel
        self.geometry("400x300")  # Setzt die Fenstergröße
        self.current_frame = None  # Aktuell angezeigter Frame (Startwert: None)
        self.show_start()  # Zeigt beim Start den Startbildschirm an

    # Funktion zum Wechseln zwischen Frames
    def switch_frame(self, frame_class, *args):
        # Entfernt den aktuellen Frame, falls vorhanden
        if self.current_frame is not None:
            self.current_frame.pack_forget()  # Entfernt den Frame aus dem Layout
            self.current_frame.destroy()  # Zerstört den Frame (freigeben von Ressourcen)

        # Erzeugt einen neuen Frame basierend auf der übergebenen Klasse und Argumenten
        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)  # Fügt den neuen Frame ein und dehnt ihn aus

    # Zeigt den Startbildschirm an
    def show_start(self):
        self.switch_frame(TriviaClient)

    # Zeigt den Server-Browsing-Bildschirm (zum Beitreten eines Spiels) an
    def show_serverbrowse(self):
        self.switch_frame(TriviaClientBrowse)

    # Zeigt den Bildschirm zum Erstellen eines Spiels als Server an
    def show_servercreate(self):
        self.switch_frame(TriviaServerCreate)

    # Zeigt den "Warten auf Spieler"-Bildschirm des Servers an
    def show_serverwait(self, game_name, game_category):
        self.switch_frame(TriviaServerWait, game_name, game_category)

    # Zeigt den "Warten auf Spielstart"-Bildschirm für den Client an
    def show_clientwait(self, server_address):
        self.switch_frame(TriviaClientWait, server_address)
    
    # Startet das eigentliche Spiel
    def show_game(self, server=None):
        self.switch_frame(TriviaGame, server)

# Startpunkt der Anwendung
if __name__ == "__main__":
    app = App()  # Erzeugt eine Instanz der App
    app.mainloop()  # Startet die GUI-Schleife (Warten auf Events)
