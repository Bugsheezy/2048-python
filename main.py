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

add_tile()
print_board()