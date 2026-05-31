class FitMap:

    def __init__(self, board):

        self.board = board

        self.map = []

    # =====================================================
    # COMPUTE FIT MAP
    # =====================================================

    def compute(self, state):

        size = self.board.size

        occupied = self.board.get_occupied_cells(state)

        # initialize fit map
        self.map = [
            [0 for _ in range(size)]
            for _ in range(size)
        ]

        # -------------------------------------------------
        # bottom-up dynamic programming
        # -------------------------------------------------

        for y in reversed(range(size)):

            for x in reversed(range(size)):

                # occupied cells cannot fit anything
                if (x, y) in occupied:
                    self.map[y][x] = 0
                    continue

                # edge cells
                if x == size - 1 or y == size - 1:
                    self.map[y][x] = 1
                    continue

                self.map[y][x] = 1 + min(
                    self.map[y][x + 1],
                    self.map[y + 1][x],
                    self.map[y + 1][x + 1]
                )

    # =====================================================
    # QUERY
    # =====================================================

    def largest_square_at(self, x, y):

        if not self.map:
            return 0

        return self.map[y][x]

    # =====================================================
    # EXPORT
    # =====================================================

    def get_map(self):

        return self.map