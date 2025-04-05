import tkinter as tk
from GUI.start import TriviaClient
from GUI.browse import TriviaClientBrowse
from GUI.create import TriviaServerCreate
from GUI.serverwait import TriviaServerWait

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trivia Spiel")
        self.geometry("400x300")
        self.current_frame = None
        self.show_start()

    def switch_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            self.current_frame.destroy()

        self.current_frame = frame_class(self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def show_start(self):
        self.switch_frame(TriviaClient)

    def show_serverbrowse(self):
        self.switch_frame(TriviaClientBrowse)

    def show_servercreate(self):
        self.switch_frame(TriviaServerCreate)

    def show_serverwait(self, game_name, game_category):
        self.switch_frame(TriviaServerWait, game_name, game_category)


if __name__ == "__main__":
    app = App()
    app.mainloop()