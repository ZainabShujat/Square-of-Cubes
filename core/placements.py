class PlacementGenerator:

    def __init__(self, board, fitmap):

        self.board = board
        self.fitmap = fitmap

    # =====================================================
    # ALL LEGAL PLACEMENTS
    # =====================================================

    def generate_all(self, state):

        self.fitmap.compute(state)

        placements = {}

        for size, count in state.remaining_tiles.items():

            if count <= 0:
                continue

            placements[size] = self.generate_for_size(
                state,
                size
            )

        return placements

    # =====================================================
    # PLACEMENTS FOR SINGLE SIZE
    # =====================================================

    def generate_for_size(self, state, size):

        results = []

        fitmap = self.fitmap.get_map()

        for y in range(self.board.size):

            for x in range(self.board.size):

                # fitmap tells us largest valid square here
                if fitmap[y][x] >= size:

                    results.append((x, y))

        return results

    # =====================================================
    # TOTAL MOVE COUNT
    # =====================================================

    def total_moves(self, state):

        placements = self.generate_all(state)

        total = 0

        for moves in placements.values():

            total += len(moves)

        return total