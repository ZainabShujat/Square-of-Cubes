class DeadzoneDetector:

    def __init__(self, board, fitmap):

        self.board = board
        self.fitmap = fitmap

    # =====================================================
    # DEAD CELLS
    # =====================================================

    def find_dead_cells(self, state):

        self.fitmap.compute(state)

        fitmap = self.fitmap.get_map()

        dead_cells = set()

        # ---------------------------------------------
        # remaining tile sizes
        # ---------------------------------------------

        remaining_sizes = []

        for size, count in state.remaining_tiles.items():

            if count > 0:

                remaining_sizes.append(size)

        # no tiles left
        if not remaining_sizes:

            return dead_cells

        smallest_size = min(remaining_sizes)

        # ---------------------------------------------
        # detect dead cells
        # ---------------------------------------------

        for y in range(self.board.size):

            for x in range(self.board.size):

                value = fitmap[y][x]

                # occupied cells
                if value == 0:
                    continue

                # cannot even fit smallest tile
                if value < smallest_size:

                    dead_cells.add((x, y))

        return dead_cells

    # =====================================================
    # DEAD REGIONS
    # =====================================================

    def find_dead_regions(self, state):

        dead_cells = self.find_dead_cells(state)

        regions = self.board.get_regions(state)

        dead_regions = []

        for region in regions:

            is_dead = True

            for cell in region:

                if cell not in dead_cells:

                    is_dead = False
                    break

            if is_dead:

                dead_regions.append(region)

        return dead_regions
    