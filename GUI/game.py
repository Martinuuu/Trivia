import tkinter as tk
import random
import html
from clientnetwork import send_answer

class TriviaGame(tk.Frame):
    def __init__(self, parent, fragen=None, rolle=None, server_address=None):
        super().__init__(parent)
        self.parent = parent
        self.fragen = fragen or []
        self.frage_index = 0
        self.rolle = rolle  # Rolle des Spielers (client/server)
        self.server_address = server_address
        self.after_id = None  # Für den Timer
        print("TriviaGame Rolle:", self.rolle)

        # Question label at the top
        self.question_label = tk.Label(self, text="Question goes here", font=("Arial", 20), wraplength=400)
        self.question_label.pack(pady=(20, 1))

        difficulty_label = tk.Label(self, text="difficulty", font=("Arial", 12))
        difficulty_label.pack(pady=(0, 10))

        # Frame for the 2x2 grid of answer buttons
        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack()

        self.timer_label = tk.Label(self, text="", font=("Arial", 16))
        self.timer_label.pack(pady=(0, 10))

        # Create 4 buttons for answers in a 2x2 grid
        self.answer_buttons = []
        for i in range(2):
            for j in range(2):
                button = tk.Button(self.answer_frame, text=f"Answer {i*2 + j + 1}", font=("Arial", 16), width=20, height=2)
                button.grid(row=i, column=j, padx=10, pady=10)
                button.grid_remove()
                button.config(command=lambda b=button: self.on_answer(b["text"]))
                self.answer_buttons.append(button)

        if self.fragen:
            self.show_question(self.frage_index)

        if self.rolle == "server":
            self.score_label = tk.Label(self, text="Punktestand:", font=("Arial", 14))
            self.score_label.pack()
            self.score_listbox = tk.Listbox(self, font=("Arial", 12))
            self.score_listbox.pack(fill=tk.X, expand=True, padx=20)
            # Initial befüllen, falls Scores übergeben werden
            self.update_scores({})

    def update_scores(self, scores):
        if hasattr(self, "score_listbox"):
            self.score_listbox.delete(0, tk.END)
            for name, score in scores.items():
                self.score_listbox.insert(tk.END, f"{name} - Punkte: {score}")
    
    def update_scores_and_question(self, frage, scores):
        self.question_label.config(text=html.unescape(frage["question"]))
        # Antworten aktualisieren:
        answers = frage["incorrect_answers"] + [frage["correct_answer"]]
        answers = [html.unescape(a) for a in answers]
        random.shuffle(answers)
        for btn, answer in zip(self.answer_buttons, answers):
            btn.config(text=answer)
        self.update_scores(scores)

    def update_timer(self, seconds):
        self.timer_label.config(text=f"Zeit: {seconds} Sekunden")

    def show_answers(self, delay):
        # self.after(delay, self.show_answer_buttons)
        self.after_id = self.after(delay, self.show_answer_buttons)
    def show_answer_buttons(self):
        for button in self.answer_buttons:
            button.grid()  # Buttons wieder sichtbar machen

    def show_question(self, index):
        frage = self.fragen[index]
        # Frage-Text ggf. HTML-dekodieren


        self.question_label.config(text=html.unescape(frage["question"]))
        self.difficulty_label = tk.Label(self, text=frage["difficulty"], font=("Arial", 12))
    
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
    
    def on_answer(self, answer):
        if self.rolle == "client" and self.server_address:
            send_answer(self.server_address, answer)
            print(f"Antwort gesendet: {answer}")

    def destroy(self):
        # Timer abbrechen, falls noch aktiv
        if self.after_id is not None:
            try:
                if self.winfo_exists():
                    self.after_cancel(self.after_id)
            except Exception as e:
                print("Fehler beim Abbrechen des Timers:", e)
            self.after_id = None
        super().destroy()