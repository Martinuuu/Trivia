import tkinter as tk

class TriviaGame(tk.Frame):
    def __init__(self, parent, server=None):
        super().__init__(parent)
        self.parent = parent
        self.server = server

        # Question label at the top
        self.question_label = tk.Label(self, text="Question goes here", font=("Arial", 20), wraplength=400)
        self.question_label.pack(pady=20)

        # Frame for the 2x2 grid of answer buttons
        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack()

        # Create 4 buttons for answers in a 2x2 grid
        self.answer_buttons = []
        for i in range(2):
            for j in range(2):
                button = tk.Button(self.answer_frame, text=f"Answer {i*2 + j + 1}", font=("Arial", 16), width=20, height=2)
                button.grid(row=i, column=j, padx=10, pady=10)
                if self.server:
                    button.config(state="disabled")
                self.answer_buttons.append(button)


