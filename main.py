import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

from game import Game2048


TILE_COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

TEXT_COLORS = {
    2: "#776e65",
    4: "#776e65"
}


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.resizable(False, False)

        self.game = Game2048()
        self.win_announced = False
        self.high_scores = self.load_high_scores()

        # Title
        title = tk.Label(
            root,
            text="2048",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(20, 5))

        # Creator
        creator = tk.Label(
            root,
            text="by John Ocampo",
            font=("Arial", 9)
        )
        creator.pack(pady=(0, 5))

        # Score and Best Score
        score_frame = tk.Frame(root)
        score_frame.pack(pady=(5, 10))

        self.score_label = tk.Label(
            score_frame,
            text="SCORE\n0",
            font=("Arial", 14, "bold"),
            width=10
        )
        self.score_label.pack(
            side="left",
            padx=5
        )

        self.best_label = tk.Label(
            score_frame,
            text="BEST\n0",
            font=("Arial", 14, "bold"),
            width=10
        )
        self.best_label.pack(
            side="left",
            padx=5
        )

        # Game Board
        self.board_frame = tk.Frame(
            root,
            bg="#bbada0"
        )
        self.board_frame.pack(
            padx=20,
            pady=10
        )

        self.cells = []

        for row in range(4):
            cell_row = []

            for column in range(4):
                cell = tk.Label(
                    self.board_frame,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 20, "bold"),
                    relief="flat",
                    borderwidth=0
                )

                cell.grid(
                    row=row,
                    column=column,
                    padx=5,
                    pady=5
                )

                cell_row.append(cell)

            self.cells.append(cell_row)

        # New Game Button
        new_game_button = tk.Button(
            root,
            text="New Game",
            font=("Arial", 12, "bold"),
            command=self.new_game
        )
        new_game_button.pack(pady=10)

        # Leaderboard
        leaderboard_title = tk.Label(
            root,
            text="TOP 3 SCORES",
            font=("Arial", 12, "bold")
        )
        leaderboard_title.pack(
            pady=(5, 2)
        )

        self.leaderboard_label = tk.Label(
            root,
            text="1. ---\n2. ---\n3. ---",
            font=("Arial", 10),
            justify="left"
        )
        self.leaderboard_label.pack(
            pady=(0, 10)
        )

        # Instructions
        instructions = tk.Label(
            root,
            text="Use the arrow keys or WASD to move",
            font=("Arial", 10)
        )
        instructions.pack(
            pady=(0, 20)
        )

        # Arrow Key Controls
        self.root.bind(
            "<Left>",
            lambda event: self.handle_move("left")
        )

        self.root.bind(
            "<Right>",
            lambda event: self.handle_move("right")
        )

        self.root.bind(
            "<Up>",
            lambda event: self.handle_move("up")
        )

        self.root.bind(
            "<Down>",
            lambda event: self.handle_move("down")
        )

        # WASD Controls
        self.root.bind(
            "a",
            lambda event: self.handle_move("left")
        )

        self.root.bind(
            "d",
            lambda event: self.handle_move("right")
        )

        self.root.bind(
            "w",
            lambda event: self.handle_move("up")
        )

        self.root.bind(
            "s",
            lambda event: self.handle_move("down")
        )

        self.update_display()
        self.update_leaderboard()

    def save_high_scores(self):
        with open("high_scores.json", "w") as file:
            json.dump(
                self.high_scores,
                file,
                indent=4
            )

    def check_high_score(self):
        score = self.game.score

        qualifies = (
            len(self.high_scores) < 3
            or score > self.high_scores[-1]["score"]
        )

        if not qualifies:
            return

        name = simpledialog.askstring(
            "Top Score!",
            f"Your score of {score} made the Top 3!\n\n"
            "Enter your name:",
            parent=self.root
        )

        if not name:
            name = "Anonymous"

        name = name.strip()

        if not name:
            name = "Anonymous"

        self.high_scores.append({
            "name": name,
            "score": score
        })

        self.high_scores.sort(
            key=lambda entry: entry["score"],
            reverse=True
        )

        self.high_scores = self.high_scores[:3]

        self.save_high_scores()
        self.update_leaderboard()

    def load_high_scores(self):
        if os.path.exists("high_scores.json"):
            try:
                with open("high_scores.json", "r") as file:
                    return json.load(file)

            except (json.JSONDecodeError, OSError):
                return []

        return []

    def update_leaderboard(self):
        lines = []

        for i in range(3):
            if i < len(self.high_scores):
                name = self.high_scores[i]["name"]
                score = self.high_scores[i]["score"]

                lines.append(
                    f"{i + 1}. {name} - {score}"
                )

            else:
                lines.append(
                    f"{i + 1}. ---"
                )

        self.leaderboard_label.config(
            text="\n".join(lines)
        )

    def handle_move(self, direction):
        moved = self.game.move(direction)

        if moved:
            self.update_display()

            if self.game.has_won() and not self.win_announced:
                self.win_announced = True

                play_again = messagebox.askyesno(
                    "You Win!",
                    f"You reached 2048!\n\n"
                    f"Score: {self.game.score}\n\n"
                    "Start a new game?"
                )

                if play_again:
                    self.new_game(confirm=False)

                return

        if self.game.game_over():
            self.check_high_score()

            play_again = messagebox.askyesno(
                "Game Over",
                f"No more moves available.\n\n"
                f"Final Score: {self.game.score}\n\n"
                "Start a new game?"
            )

            if play_again:
                self.new_game(confirm=False)

    def update_display(self):
        for row in range(4):
            for column in range(4):
                value = self.game.board[row][column]

                background = TILE_COLORS.get(
                    value,
                    "#3c3a32"
                )

                if value in TEXT_COLORS:
                    text_color = TEXT_COLORS[value]
                else:
                    text_color = "#f9f6f2"

                if value == 0:
                    text = ""
                else:
                    text = str(value)

                self.cells[row][column].config(
                    text=text,
                    bg=background,
                    fg=text_color
                )

        self.score_label.config(
            text=f"SCORE\n{self.game.score}"
        )

        if self.high_scores:
            best_score = self.high_scores[0]["score"]
        else:
            best_score = 0

        best_score = max(
            best_score,
            self.game.score
        )

        self.best_label.config(
            text=f"BEST\n{best_score}"
        )

    def new_game(self, confirm=True):
        if confirm and self.game.score > 0:
            restart = messagebox.askyesno(
                "New Game",
                "Are you sure you want to start a new game?\n\n"
                "Your current game will be lost."
            )

            if not restart:
                return

        self.game = Game2048()
        self.win_announced = False

        self.update_display()


root = tk.Tk()
app = GameGUI(root)
root.mainloop()