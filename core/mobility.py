class MobilityAnalyzer:

    def __init__(self, placement_generator):

        self.placement_generator = placement_generator

    # =====================================================
    # ALL MOBILITY DATA
    # =====================================================

    def analyze(self, state):

        placements = self.placement_generator.generate_all(
            state
        )

        mobility = {

            "total_moves": 0,

            "moves_by_size": {},

            "largest_available_tile": 0,

            "smallest_available_tile": 0
        }

        available_sizes = []

        # ============================================
        # analyze placement counts
        # ============================================

        for size, moves in placements.items():

            move_count = len(moves)

            mobility["moves_by_size"][size] = move_count

            mobility["total_moves"] += move_count

            if move_count > 0:

                available_sizes.append(size)

        # ============================================
        # largest/smallest surviving tile
        # ============================================

        if available_sizes:

            mobility["largest_available_tile"] = max(
                available_sizes
            )

            mobility["smallest_available_tile"] = min(
                available_sizes
            )

        return mobility

    # =====================================================
    # MOBILITY SCORE
    # =====================================================

    def mobility_score(self, state):

        data = self.analyze(state)

        score = 0

        # ============================================
        # reward future flexibility
        # ============================================

        score += data["total_moves"] // 10

        # ============================================
        # reward large tile survivability
        # ============================================

        score += (
            data["largest_available_tile"] * 50
        )

        return score
        