import tkinter as tk
from tkinter import messagebox

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

        title = tk.Label(
            root,
            text="2048",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(20, 5))

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 16)
        )
        self.score_label.pack(pady=(0, 10))

        self.board_frame = tk.Frame(
            root,
            bg="#bbada0"
        )
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

        new_game_button = tk.Button(
            root,
            text="New Game",
            font=("Arial", 12, "bold"),
            command=self.new_game
        )
        new_game_button.pack(pady=10)

        instructions = tk.Label(
            root,
            text="Use the arrow keys to move",
            font=("Arial", 10)
        )
        instructions.pack(pady=(0, 20))

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
            text=f"Score: {self.game.score}"
        )

    def new_game(self):
        self.game = Game2048()
        self.update_display()


root = tk.Tk()
app = GameGUI(root)
root.mainloop()