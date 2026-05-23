from utils.constants import TILE_COLORS


class Piece:

    def __init__(self, size, grid_x=None, grid_y=None):

        self.size = size

        self.grid_x = grid_x
        self.grid_y = grid_y

        self.dragging = False

        self.offset_x = 0
        self.offset_y = 0

        self.color = TILE_COLORS[size]

    @property
    def area(self):

        return self.size * self.size

    def contains(self, x, y):

        if self.grid_x is None or self.grid_y is None:
            return False

        return (
            self.grid_x <= x < self.grid_x + self.size
            and
            self.grid_y <= y < self.grid_y + self.size
        )