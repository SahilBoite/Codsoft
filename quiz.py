import tkinter as tk
from tkinter import messagebox
import random
import time

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("600x400")
        self.root.configure(bg="#F0F0F0")  # Set light gray background color

        self.score = 0
        self.current_question = 0
        self.timer_text = tk.StringVar()
        self.timer_text.set("30")  # Initial value for the timer

        # Sample quiz questions (you can replace with your own questions)
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4"
            },
            # Add more questions here
        ]

        self.question_label = tk.Label(root, text="", wraplength=550, font=("Helvetica", 16), fg="#333333", bg="#F0F0F0")
        self.question_label.pack(pady=30)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", font=("Helvetica", 12), bg="#E5E5E5", relief=tk.FLAT,
                            activebackground="#D3D3D3", command=lambda idx=i: self.check_answer(idx))
            self.option_buttons.append(btn)
            btn.pack(pady=5, padx=20, ipadx=5, ipady=3)

        self.timer_label = tk.Label(root, textvariable=self.timer_text, font=("Helvetica", 20), fg="#333333", bg="#F0F0F0")
        self.timer_label.place(x=20, y=20)  # Position the timer label in the top-left corner

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 16), fg="#333333", bg="#F0F0F0")
        self.score_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="#333333", bg="#F0F0F0")
        self.feedback_label.pack(pady=20)

        self.show_welcome_message()

    def show_welcome_message(self):
        welcome_text = "Welcome to the Quiz Game!\n\nInstructions:\n\n" \
                       "- You will be asked a series of multiple-choice questions.\n" \
                       "- Click on the option you think is correct.\n" \
                       "- You will score a point for each correct answer.\n\n" \
                       "Press the Start button to begin the quiz."
        self.question_label.config(text=welcome_text)

        start_button = tk.Button(self.root, text="Start", font=("Helvetica", 16), fg="#007AFF", bg="#E5E5E5",
                                 activebackground="#D3D3D3", command=self.start_game)
        start_button.pack(pady=10)

    def start_game(self):
        self.shuffle_questions()
        self.current_question = 0
        self.score = 0
        self.show_question()

    def shuffle_questions(self):
        random.shuffle(self.questions)

    def show_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["question"])
            self.show_multiple_choice_options(question_data["options"])
            self.start_timer()  # Start the timer when a new question is shown

    def show_multiple_choice_options(self, options):
        random.shuffle(options)
        for i in range(4):
            if i < len(options):
                self.option_buttons[i].config(text=options[i], state=tk.NORMAL, relief=tk.FLAT)
            else:
                self.option_buttons[i].config(text="", state=tk.DISABLED, relief=tk.FLAT)

    def start_timer(self):
        self.remaining_time = 30
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            self.timer_text.set(str(self.remaining_time))
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_text.set("Time's up!")
            self.check_answer(-1)  # Consider it as an incorrect answer when time's up

    def check_answer(self, selected_option_idx):
        self.stop_timer()
        question_data = self.questions[self.current_question]
        correct_answer = question_data["correct_answer"]
        selected_answer = self.option_buttons[selected_option_idx]["text"] if selected_option_idx >= 0 else None

        if selected_answer == correct_answer:
            self.score += 1

        self.show_feedback(correct_answer)
        self.current_question += 1

    def stop_timer(self):
        self.timer_text.set("")  # Clear the timer text when the timer stops

    def show_feedback(self, correct_answer):
        question_data = self.questions[self.current_question]
        self.show_multiple_choice_options([])  # Hide the answer buttons while showing feedback

        if correct_answer:
            feedback_text = f"Correct!\nThe answer is: {correct_answer}"
        else:
            feedback_text = f"Time's up!\nThe correct answer is: {question_data['correct_answer']}"

        self.feedback_label.config(text=feedback_text)
        self.score_label.config(text=f"Score: {self.score}")

        if self.current_question == len(self.questions):
            self.show_final_results()
        else:
            self.root.after(2000, self.show_question)  # Show the next question after 2 seconds

    def show_final_results(self):
        final_score_text = f"Congratulations!\nYou have completed the quiz.\nYour final score is: {self.score}"
        self.question_label.config(text=final_score_text)
        self.feedback_label.config(text="")
        self.score_label.config(text="")
        self.play_again_button = tk.Button(self.root, text="Play Again", font=("Helvetica", 16), fg="#007AFF", bg="#E5E5E5",
                                           activebackground="#D3D3D3", command=self.start_game)
        self.play_again_button.pack(pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    quiz_game = QuizGame(root)
    quiz_game.run()
