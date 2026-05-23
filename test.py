from logic import *

board = create_board()

print("EMPTY BOARD:")
print_board(board)

print("\n")

# Place 3x3 tile
if can_place(board, 3, 0, 0):

    place_tile(board, 3, 0, 0)

print("AFTER PLACING 3x3:")
print_board(board)

print("\n")

# Try overlapping placement
result = can_place(board, 2, 1, 1)

print("CAN PLACE 2x2 AT (1,1)?")
print(result)

print("\n")

# Remove tile
remove_tile(board, 3, 0, 0)

print("AFTER REMOVAL:")
print_board(board)