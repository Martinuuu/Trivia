import tkinter as tk
from GUI.start import TriviaClient
from GUI.browse import TriviaClientBrowse

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trivia Spiel")
        self.geometry("400x300")
        self.aktueller_frame = None
        self.show_start()

    def switch_frame(self, seite_klasse):
        if self.aktueller_frame:
            self.aktueller_frame.destroy()
        self.aktueller_frame = seite_klasse(self)
        self.aktueller_frame.pack(fill="both", expand=True)

    def show_start(self):
        self.switch_frame(TriviaClient)

    def show_serverbrowse(self):
        self.switch_frame(TriviaClientBrowse)


if __name__ == "__main__":
    app = App()
    app.mainloop()