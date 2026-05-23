BOARD_SIZE = 45


# Create empty board
def create_board():

    return [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]


# Check if tile can be placed
def can_place(board, size, row, col):

    # Out of bounds
    if row + size > BOARD_SIZE:
        return False

    if col + size > BOARD_SIZE:
        return False

    # Check occupied cells
    for r in range(row, row + size):

        for c in range(col, col + size):

            if board[r][c] != 0:
                return False

    return True


# Place tile
def place_tile(board, size, row, col):

    for r in range(row, row + size):

        for c in range(col, col + size):

            board[r][c] = size


# Remove tile
def remove_tile(board, size, row, col):

    for r in range(row, row + size):

        for c in range(col, col + size):

            board[r][c] = 0


# Print board nicely
def print_board(board):

    for row in board:

        print(row)