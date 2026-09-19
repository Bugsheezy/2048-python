import tkinter as tk
from tkinter import messagebox

from game import Game2048


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.resizable(False, False)

        self.game = Game2048()

        # Title
        title = tk.Label(
            root,
            text="2048",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(20, 5))

        # Score
        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 16)
        )
        self.score_label.pack(pady=(0, 10))

        # Game board
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=20, pady=10)

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
                    relief="solid",
                    borderwidth=2
                )

                cell.grid(
                    row=row,
                    column=column,
                    padx=3,
                    pady=3
                )

                cell_row.append(cell)

            self.cells.append(cell_row)

        # New Game button
        new_game_button = tk.Button(
            root,
            text="New Game",
            font=("Arial", 12),
            command=self.new_game
        )
        new_game_button.pack(pady=10)

        # Instructions
        instructions = tk.Label(
            root,
            text="Use the arrow keys to move",
            font=("Arial", 10)
        )
        instructions.pack(pady=(0, 20))

        # Keyboard controls
        self.root.bind("<Left>", lambda event: self.handle_move("left"))
        self.root.bind("<Right>", lambda event: self.handle_move("right"))
        self.root.bind("<Up>", lambda event: self.handle_move("up"))
        self.root.bind("<Down>", lambda event: self.handle_move("down"))

        self.update_display()

    def handle_move(self, direction):
        moved = self.game.move(direction)

        if moved:
            self.update_display()

            if self.game.game_over():
                messagebox.showinfo(
                    "Game Over",
                    f"Game Over!\n\nFinal Score: {self.game.score}"
                )

    def update_display(self):
        for row in range(4):
            for column in range(4):
                value = self.game.board[row][column]

                if value == 0:
                    self.cells[row][column].config(text="")
                else:
                    self.cells[row][column].config(text=str(value))

        self.score_label.config(
            text=f"Score: {self.game.score}"
        )

    def new_game(self):
        self.game = Game2048()
        self.update_display()


root = tk.Tk()
app = GameGUI(root)
root.mainloop()