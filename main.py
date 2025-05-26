# Importiere das tkinter-Modul für die GUI-Erstellung
import tkinter as tk

# Importiere die verschiedenen GUI-Komponenten aus den Untermodulen
from GUI.start import TriviaClient
from GUI.browse import TriviaClientBrowse
from GUI.create import TriviaServerCreate
from GUI.serverwait import TriviaServerWait
from GUI.clientwait import TriviaClientWait
from GUI.game import TriviaGame

import random

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
    def show_serverwait(self, game_name, game_category_name, game_category_id):
        self.switch_frame(TriviaServerWait, game_name, game_category_name, game_category_id)

    # Zeigt den "Warten auf Spielstart"-Bildschirm für den Client an
    def show_clientwait(self, server_address):
        self.switch_frame(TriviaClientWait, server_address)
    
    # Startet das eigentliche Spiel
    def show_game(self, fragen=None, rolle=None):
        server_address = None
        old_frame = self.current_frame
        if rolle == "client":
            if hasattr(self.current_frame, "server_address"):
                server_address = self.current_frame.server_address
    
        if fragen:
            for frage in fragen:
                if "all_answers" not in frage:
                    answers = frage["incorrect_answers"] + [frage["correct_answer"]]
                    random.shuffle(answers)
                    frage["all_answers"] = answers



        self.switch_frame(TriviaGame, fragen, rolle, server_address)
    
        if rolle == "server":
            if hasattr(old_frame, "game_server"):
                def gui_update_callback(command, *args):
                    if command == "UPDATE_GUI":
                        frage, scores = args
                        # 1. Zeige die richtige Antwort grün an
                        self.current_frame.highlight_correct_answer(frage)
                        # 2. Warte z.B. 1 Sekunde, dann zeige die nächste Frage
                        self.current_frame.after(1000, lambda: self.current_frame.update_scores_and_question(frage, scores))
                old_frame.game_server.client_callback = gui_update_callback
                self.current_frame.game_server = old_frame.game_server

# Startpunkt der Anwendung
if __name__ == "__main__":
    app = App()  # Erzeugt eine Instanz der App
    app.mainloop()  # Startet die GUI-Schleife (Warten auf Events)
