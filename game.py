import random


class Game2048:
    def __init__(self):
        self.score = 0
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty_cells = []

        for row in range(4):
            for column in range(4):
                if self.board[row][column] == 0:
                    empty_cells.append((row, column))

        if empty_cells:
            row, column = random.choice(empty_cells)

            # 90% chance of 2, 10% chance of 4
            self.board[row][column] = 4 if random.random() < 0.1 else 2

    def merge_row_left(self, row):
        numbers = [number for number in row if number != 0]

        merged = []
        i = 0

        while i < len(numbers):
            if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
                new_value = numbers[i] * 2
                merged.append(new_value)

                # Add the merged tile to the score
                self.score += new_value

                i += 2
            else:
                merged.append(numbers[i])
                i += 1

        while len(merged) < 4:
            merged.append(0)

        return merged

    def move_left(self):
        for i in range(4):
            self.board[i] = self.merge_row_left(self.board[i])

    def move_right(self):
        for i in range(4):
            reversed_row = self.board[i][::-1]
            merged_row = self.merge_row_left(reversed_row)
            self.board[i] = merged_row[::-1]

    def move_up(self):
        for column in range(4):
            values = [self.board[row][column] for row in range(4)]
            merged = self.merge_row_left(values)

            for row in range(4):
                self.board[row][column] = merged[row]

    def move_down(self):
        for column in range(4):
            values = [self.board[row][column] for row in range(4)]
            values.reverse()

            merged = self.merge_row_left(values)
            merged.reverse()

            for row in range(4):
                self.board[row][column] = merged[row]

    def move(self, direction):
        old_board = [row[:] for row in self.board]

        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        else:
            return False

        # Only create a new tile if something actually moved
        if self.board != old_board:
            self.add_tile()
            return True

        return False

    def game_over(self):
        # An empty square means another move is possible
        for row in self.board:
            if 0 in row:
                return False

        # Check horizontal neighbours
        for row in range(4):
            for column in range(3):
                if self.board[row][column] == self.board[row][column + 1]:
                    return False

        # Check vertical neighbours
        for row in range(3):
            for column in range(4):
                if self.board[row][column] == self.board[row + 1][column]:
                    return False

        return True

    def has_won(self):
        for row in self.board:
            if 2048 in row:
                return True

        return False