import json
import random
import tkinter as tk
from tkinter import messagebox


# Function to load questions from the questions.json file
def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

# Function to load highscores from the highscores.json file
def load_high_scores(filename):
    try:
        with open(filename, 'r') as file:
            high_scores = json.load(file)
    except FileNotFoundError:
        high_scores = {"highscores": []}
    return high_scores

# Function to save high scores to a JSON file
def save_high_scores(filename, high_scores):
    with open(filename, 'w') as file:
        json.dump(high_scores, file, indent=4)

# Main class for my quiz game
class QuizGame:
    def __init__(self, main_window):
        self.root = main_window
        self.root.title("Owen's Quiz Game")
        self.root.geometry("600x400")

        # Load questions and initialize variables
        self.questions = load_questions('questions.json')
        self.score = 0
        self.scores = [0, 0]
        self.current_player = random.randint(0, 1)
        self.available_questions = {
            category.lower(): [200, 400, 600, 800, 1000]
            for category in self.questions
        }

        # Initialize player and UI variables
        self.single_player = None
        self.mode_label = None
        self.single_player_button = None
        self.multiplayer_button = None
        self.quit_button = None
        self.player_name = None
        self.score_label = None
        self.player_label = None
        self.category_label = None
        self.category_var = tk.StringVar(self.root)
        self.category_menu = None
        self.value_label = None
        self.value_var = tk.StringVar(self.root)
        self.value_menu = None
        self.select_button = None
        self.question_label = None
        self.answer_var = None
        self.submit_button = None
        self.timer_label = None
        self.feedback_label = None
        self.category = None
        self.value = None
        self.time_left = 20
        self.timer_id = None
        self.player_name_label = None
        self.player_name_entry = None
        self.start_button = None

        # Create the initial UI widgets
        self.create_widgets()

    # Function to create the UI widgets
    def create_widgets(self):
        title_label = tk.Label(
            self.root, text="Welcome to Owen's Quiz Game!", font=("Helvetica", 16)
        )
        title_label.pack(pady=10)

        self.mode_label = tk.Label(self.root, text="Choose a mode:")
        self.mode_label.pack(pady=10)

        self.single_player_button = tk.Button(
            self.root, text="Single Player", command=self.single_player_mode
        )
        self.single_player_button.pack(pady=5)

        self.multiplayer_button = tk.Button(
            self.root, text="Multiplayer", command=self.multiplayer_mode
        )
        self.multiplayer_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.BOTTOM, pady=10)

    # Function to start single player mode
    def single_player_mode(self):
        self.clear_widgets()
        self.player_name_label = tk.Label(self.root, text="Enter your name:")
        self.player_name_label.pack(pady=5)

        self.player_name_entry = tk.Entry(self.root)
        self.player_name_entry.pack(pady=5)

        self.start_button = tk.Button(
            self.root, text="Start Game", command=self.start_single_player_game
        )
        self.start_button.pack(pady=5)

    # Function to start single player mode
    def start_single_player_game(self):
        if self.player_name_entry:
            self.player_name = self.player_name_entry.get()
        else:
            self.player_name = ""

        if self.player_name:
            self.score = 0
            self.start_game(single_player=True)
        else:
            messagebox.showerror("Error", "Please enter your name.")

    # Function to setup multiplayer
    def multiplayer_mode(self):
        self.scores = [0, 0]
        self.current_player = random.randint(0, 1)
        self.start_game(single_player=False)

    # Function to start the game
    def start_game(self, single_player):
        self.clear_widgets()
        self.single_player = single_player
        self.show_question_selection()

    # Function to clear the UI widgets
    def clear_widgets(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    # Function to change the value menu based on the category that was chosen 
    def update_value_menu(self, selected_category):
        if self.value_menu:
            self.value_menu['menu'].delete(0, 'end')
            if selected_category in self.available_questions:
                for val in self.available_questions[selected_category]:
                    self.value_menu['menu'].add_command(
                        label=val, command=lambda v=val: self.value_var.set(str(v))
                    )
            self.value_menu.config(state=tk.NORMAL)

    # Function to show the question choosing UI
    def show_question_selection(self):
        self.clear_widgets()
        if self.single_player:
            current_score_text = f"Current Score: {self.score}"
        else:
            current_score_text = (
                f"Player 1: {self.scores[0]} | Player 2: {self.scores[1]}"
            )
            self.player_label = tk.Label(
                self.root, text=f"Player {self.current_player + 1}'s turn"
            )
            self.player_label.pack(pady=5)

        self.score_label = tk.Label(self.root, text=current_score_text)
        self.score_label.pack(pady=10)

        self.category_label = tk.Label(self.root, text="Choose a category:")
        self.category_label.pack(pady=5)

        self.category_var.set("Select a category")

        self.category_menu = tk.OptionMenu(
            self.root, self.category_var, *self.available_questions.keys(),
            command=self.update_value_menu
        )
        self.category_menu.pack(pady=5)

        self.value_label = tk.Label(self.root, text="Choose a value:")
        self.value_label.pack(pady=5)

        self.value_var.set("Select a value")

        self.value_menu = tk.OptionMenu(self.root, self.value_var, "")
        self.value_menu.pack(pady=5)
        self.value_menu.config(state=tk.DISABLED)

        self.select_button = tk.Button(
            self.root, text="Select", command=self.select_question
        )
        self.select_button.pack(pady=5)

    # Function to choose a question
    def select_question(self):
        category = self.category_var.get()
        value = self.value_var.get()

        if (
            category in self.available_questions
            and self.available_questions[category]
            and value.isdigit()
            and int(value) in self.available_questions[category]
        ):
            self.ask_question(category, int(value))
        else:
            self.feedback_label = tk.Label(
                self.root, text="Invalid category or value selection", fg="red"
            )
            self.feedback_label.pack(pady=5)

    # Function to display the question
    def ask_question(self, category, value):
        self.clear_widgets()
        self.category = category
        self.value = value
        question_data = random.choice(self.questions[category][str(value)])

        self.question_label = tk.Label(self.root, text=question_data['question'])
        self.question_label.pack(pady=10)

        self.answer_var = tk.IntVar()

        for i, choice in enumerate(question_data['choices']):
            rb = tk.Radiobutton(
                self.root, text=choice, variable=self.answer_var, value=i + 1
            )
            rb.pack(pady=5)

        self.submit_button = tk.Button(
            self.root, text="Submit", command=lambda: self.check_answer(question_data)
        )
        self.submit_button.pack(pady=10)

        self.timer_label = tk.Label(
            self.root, text=f"Time left: {self.time_left} seconds"
        )
        self.timer_label.pack(pady=10)
        self.update_timer()

    # Function to update the timer
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            if self.timer_label:
                self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.feedback_label = tk.Label(
                self.root, text="Time's up! Moving to the next question.", fg="red"
            )
            self.feedback_label.pack(pady=5)
            self.check_answer(None, timed_out=True)

    # Function to  check if the answer is right
    def check_answer(self, question_data, timed_out=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.submit_button:
            self.submit_button.config(state=tk.DISABLED)
        if not timed_out:
            selected_answer = self.answer_var.get() if self.answer_var else 0
            correct_answer = question_data['choices'].index(
                question_data['answer']
            ) + 1

            if selected_answer == correct_answer:
                self.feedback_label = tk.Label(
                    self.root, text="Correct!", fg="green"
                )
                self.feedback_label.pack(pady=5)
                if self.single_player:
                    self.score += self.value if self.value else 0
                else:
                    self.scores[self.current_player] += (
                        self.value if self.value else 0
                    )
            else:
                self.feedback_label = tk.Label(
                    self.root,
                    text=f"Incorrect. The correct answer was {question_data['answer']}",
                    fg="red"
                )
                self.feedback_label.pack(pady=5)
                if self.single_player:
                    self.score -= self.value if self.value else 0
                else:
                    self.scores[self.current_player] -= (
                        self.value if self.value else 0
                    )
        else:
            if self.single_player:
                self.score -= self.value if self.value else 0
            else:
                self.scores[self.current_player] -= self.value if self.value else 0

        if self.value and self.value in self.available_questions.get(
            self.category, []
        ):
            self.available_questions[self.category].remove(self.value)
            if not self.available_questions[self.category]:
                del self.available_questions[self.category]
        self.time_left = 20
        self.root.after(2000, self.next_turn)

    # Function to go to the next turn
    def next_turn(self):
        if any(values for values in self.available_questions.values()):
            if not self.single_player:
                self.current_player = 1 - self.current_player
            self.show_question_selection()
        else:
            self.end_game()

    # Function to end the game and show the final scores if single player
    def end_game(self):
        self.clear_widgets()

        if self.single_player:
            high_scores = load_high_scores('highscores.json')
            high_scores["highscores"].append(
                {"name": self.player_name, "score": self.score}
            )
            high_scores["highscores"] = sorted(
                high_scores["highscores"], key=lambda x: x["score"], reverse=True
            )[:3]
            save_high_scores('highscores.json', high_scores)

            final_score = f"Your final score is {self.score}"
            top_scores = "\n".join(
                [
                    f"{entry['name']}: {entry['score']}"
                    for entry in high_scores["highscores"]
                ]
            )

            self.feedback_label = tk.Label(
                self.root,
                text=f"{final_score}\nTop 3 High Scores:\n{top_scores}",
                fg="blue"
            )
            self.feedback_label.pack(pady=10)
        else:
            final_score = (
                f"Player 1 final score: {self.scores[0]}\n"
                f"Player 2 final score: {self.scores[1]}"
            )
            if self.scores[0] > self.scores[1]:
                result = "Player 1 wins!"
            elif self.scores[1] > self.scores[0]:
                result = "Player 2 wins!"
            else:
                result = "It's a tie!"

            self.feedback_label = tk.Label(
                self.root, text=f"{final_score}\n{result}", fg="blue"
            )
            self.feedback_label.pack(pady=10)

        self.create_widgets()


# Main function to start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
