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

        # ensure fit map is up-to-date
        try:
            # if FitMap exposes a compute/get_map API, it's safe to call compute here
            self.fitmap.compute(state)
        except Exception:
            pass

        # query via FitMap API to avoid depending on internal map structure
        for y in range(self.board.size):
            for x in range(self.board.size):
                try:
                    largest = self.fitmap.largest_square_at(x, y)
                except Exception:
                    # fallback: try indexing raw map if available
                    fmap = self.fitmap.get_map()
                    try:
                        largest = fmap[y][x]
                    except Exception:
                        largest = 0

                if largest >= size:
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