import tkinter as tk
import random
import html
from clientnetwork import send_answer
import threading

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
                # button.grid_remove()
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
        
        self.stop_event = threading.Event()
        if self.rolle == "client" and self.server_address:
            self.listener_thread = threading.Thread(target=self.listen_for_updates, daemon=True)
            self.listener_thread.start()

    def listen_for_updates(self):
        from clientnetwork import sock
        import json
        sock.settimeout(1)
        while not self.stop_event.is_set():
            try:
                data, addr = sock.recvfrom(65536)
                msg = data.decode()
                if msg.startswith("QUESTIONS;"):
                    fragen_json = msg[len("QUESTIONS;"):]
                    fragen = json.loads(fragen_json)
                    # Neue Frage anzeigen (immer im Hauptthread!)
                    self.after(0, lambda: self.show_new_question(fragen))
                elif msg.startswith("SCORE;"):
                    # Optional: Score-Update anzeigen
                    pass
            except Exception:
                continue


    def highlight_correct_answer(self, frage):
        # Finde die richtige Antwort
        if "all_answers" in frage:
            answers = [html.unescape(a) for a in frage["all_answers"]]
        else:
            answers = frage["incorrect_answers"] + [frage["correct_answer"]]
            answers = [html.unescape(a) for a in answers]
            random.shuffle(answers)
        correct = html.unescape(frage["correct_answer"])
        for btn, answer in zip(self.answer_buttons, answers):
            if answer == correct:
                btn.config(bg="green")
            else:
                btn.config(bg="SystemButtonFace")  # Standardfarbe

    def show_new_question(self, fragen):
        # Ersetze aktuelle Frage(n) durch die neue(n)
        self.fragen = fragen
        self.frage_index = 0
        self.show_question(self.frage_index)

    def update_scores(self, scores):
        if hasattr(self, "score_listbox"):
            self.score_listbox.delete(0, tk.END)
            for name, score in scores.items():
                self.score_listbox.insert(tk.END, f"{name} - Punkte: {score}")
    
    def update_scores_and_question(self, frage, scores):
        # Setze alle Buttons zurück (Standardfarbe)
        for btn in self.answer_buttons:
            btn.config(bg="SystemButtonFace")

        self.question_label.config(text=html.unescape(frage["question"]))
        # Antworten in Server-Reihenfolge übernehmen
        if "all_answers" in frage:
            answers = [html.unescape(a) for a in frage["all_answers"]]
        else:
            answers = frage["incorrect_answers"] + [frage["correct_answer"]]
            answers = [html.unescape(a) for a in answers]
            random.shuffle(answers)
        for btn, answer in zip(self.answer_buttons, answers):
            btn.config(text=answer)
            btn.config(command=lambda a=answer: self.on_answer(a))
        self.update_scores(scores)

    def update_timer(self, seconds):
        self.timer_label.config(text=f"Zeit: {seconds} Sekunden")

    def show_answers(self, delay):
        # self.after(delay, self.show_answer_buttons)
        try:
            self.after_id = self.after(delay, self.show_answer_buttons)
        except Exception as e:
            print("Error in show_answers:", e)
            self.after_id = None


    def show_answer_buttons(self):
        for button in self.answer_buttons:
            button.grid()  # Buttons wieder sichtbar machen

    def show_question(self, index):
        # Setze alle Buttons zurück (Standardfarbe)
        for btn in self.answer_buttons:
            btn.config(bg="SystemButtonFace")  # oder "lightgray" je nach OS

        frage = self.fragen[index]
        self.question_label.config(text=html.unescape(frage["question"]))
        self.difficulty_label = tk.Label(self, text=frage["difficulty"], font=("Arial", 12))

        # Antworten in Server-Reihenfolge übernehmen
        if "all_answers" in frage:
            answers = [html.unescape(a) for a in frage["all_answers"]]
        else:
            answers = frage["incorrect_answers"] + [frage["correct_answer"]]
            answers = [html.unescape(a) for a in answers]
            random.shuffle(answers)

        for btn, answer in zip(self.answer_buttons, answers):
            btn.config(text=answer, bg="SystemButtonFace")
            btn.config(command=lambda a=answer: self.on_answer(a))
            btn.grid_remove()

        self.show_answers(1000)
    
    def on_answer(self, answer):
        if self.rolle == "client" and self.server_address:
            send_answer(self.server_address, answer)
            print(f"Antwort gesendet: {answer}")

    def destroy(self):
        if hasattr(self, "stop_event"):
            self.stop_event.set()
        if hasattr(self, "listener_thread") and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        if hasattr(self, "after_id") and self.after_id is not None:
            try:
                if self.winfo_exists():
                    self.after_cancel(self.after_id)
            except Exception as e:
                print("Error cancelling after_id: ", e)
            self.after_id = None 
        super().destroy()