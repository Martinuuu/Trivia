import tkinter as tk
import random
import html

class TriviaGame(tk.Frame):
    def __init__(self, parent, fragen=None):
        super().__init__(parent)
        self.parent = parent
        self.fragen = fragen or []
        self.frage_index = 0

        # Question label at the top
        self.question_label = tk.Label(self, text="Question goes here", font=("Arial", 20), wraplength=400)
        self.question_label.pack(pady=(20, 1))

        difficulty_label = tk.Label(self, text="difficulty", font=("Arial", 12))
        difficulty_label.pack(pady=(0, 10))

        # Frame for the 2x2 grid of answer buttons
        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack()

        # Create 4 buttons for answers in a 2x2 grid
        self.answer_buttons = []
        for i in range(2):
            for j in range(2):
                button = tk.Button(self.answer_frame, text=f"Answer {i*2 + j + 1}", font=("Arial", 16), width=20, height=2)
                button.grid(row=i, column=j, padx=10, pady=10)
                button.grid_remove()  # Buttons zunächst unsichtbar machen
                self.answer_buttons.append(button)

        if self.fragen:
            self.show_question(self.frage_index)

    def show_answers(self, delay):
        self.after(delay, self.show_answer_buttons)

    def show_answer_buttons(self):
        for button in self.answer_buttons:
            button.grid()  # Buttons wieder sichtbar machen

    def show_question(self, index):
        frage = self.fragen[index]
        # Frage-Text ggf. HTML-dekodieren
        self.question_label.config(text=html.unescape(frage["question"]))
    
        # Antworten zusammenstellen und mischen
        answers = frage["incorrect_answers"] + [frage["correct_answer"]]
        answers = [html.unescape(a) for a in answers]
        random.shuffle(answers)
    
        # Buttons mit Antworten belegen
        for btn, answer in zip(self.answer_buttons, answers):
            btn.config(text=answer)
            btn.grid_remove()  # Optional: Buttons erst nach kurzer Zeit anzeigen
    
        # Nach kurzer Zeit die Buttons einblenden
        self.show_answers(1000)  # z.B. nach 1 Sekunde
    

