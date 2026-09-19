import random
print("2048 Project")

board = [

[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0]
]

def print_board():
    for row in board:
        print(row)

def add_tile():
    empty_cells = []

    for row in range(4):
        for column in range(4):
            if board[row][column] ==0:
                empty_cells.append((row, column))

    if empty_cells:
        row, column =  random.choice(empty_cells)
        board[row][column] = 2

def merge_row_left(row):
    # Remove empty spaces
    numbers = [number for number in row if number != 0]

    # Merge matching tiles
    merged = []
    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            merged.append(numbers[i] * 2)
            i += 2
        else:
            merged.append(numbers[i])
            i += 1

    # Restore empty spaces
    while len(merged) < 4:
        merged.append(0)

    return merged


def move_left():
    for i in range(4):
        board[i] = merge_row_left(board[i])


def move_right():
    for i in range(4):
        reversed_row = board[i][::-1]
        merged_row = merge_row_left(reversed_row)
        board[i] = merged_row[::-1]


def move_up():
    for column in range(4):
        values = [board[row][column] for row in range(4)]
        merged = merge_row_left(values)

        for row in range(4):
            board[row][column] = merged[row]


def move_down():
    for column in range(4):
        values = [board[row][column] for row in range(4)]
        values.reverse()

        merged = merge_row_left(values)
        merged.reverse()

        for row in range(4):
            board[row][column] = merged[row]

def game_over():
    # If there is an empty space, the game can continue
    for row in board:
        if 0 in row:
            return False

    # Check for horizontal merges
    for row in range(4):
        for column in range(3):
            if board[row][column] == board[row][column + 1]:
                return False

    # Check for vertical merges
    for row in range(3):
        for column in range(4):
            if board[row][column] == board[row + 1][column]:
                return False

    return True

# Start a new game
board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

add_tile()
add_tile()

while not game_over():
    print()
    print_board()

    move = input("\nMove (W/A/S/D or Q to quit): ").lower()

    if move == "a":
        move_left()
    elif move == "d":
        move_right()
    elif move == "w":
        move_up()
    elif move == "s":
        move_down()
    elif move == "q":
        print("Game ended.")
        break
    else:
        print("Invalid move.")
        continue

    add_tile()

if game_over():
    print()
    print_board()
    print("\nGame Over!")