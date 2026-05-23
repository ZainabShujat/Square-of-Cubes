from utils.constants import BOARD_SIZE


class AnalysisEngine:

    def __init__(self, board):

        self.board = board

    # =====================================================
    # REGION COUNT
    # =====================================================

    def region_count(self, state):

        return len(
            self.board.get_regions(state)
        )

    # =====================================================
    # LARGEST REGION
    # =====================================================

    def largest_region_size(self, state):

        regions = self.board.get_regions(state)

        if not regions:
            return 0

        return max(
            len(region)
            for region in regions
        )

    # =====================================================
    # DEAD REGION COUNT
    # =====================================================

    def dead_region_count(self, state):

        return len(
            self.board.get_dead_regions(state)
        )

    # =====================================================
    # FRAGMENTATION SCORE
    # =====================================================

    def fragmentation_score(self, state):

        regions = self.board.get_regions(state)

        if not regions:
            return 0

        score = 0

        for region in regions:

            region_size = len(region)

            # punish tiny fragmented spaces
            if region_size <= 4:
                score += 120

            elif region_size <= 9:
                score += 80

            elif region_size <= 16:
                score += 40

            else:
                score += 5

        return score

    # =====================================================
    # SOLVABILITY HEURISTIC
    # =====================================================

    def solvability_score(self, state):

        score = 1000

        regions = self.board.get_regions(state)

        remaining_areas = []

        for size, count in state.remaining_tiles.items():

            remaining_areas.extend(
                [size * size] * count
            )

        dead_regions = 0
        fragmentation = 0

        for region in regions:

            region_size = len(region)

            # -------------------------
            # dead regions
            # -------------------------

            possible = False

            for area in remaining_areas:

                if region_size % area == 0:

                    possible = True
                    break

            if not possible:

                dead_regions += 1

            # -------------------------
            # fragmentation
            # -------------------------

            if region_size <= 4:
                fragmentation += 120

            elif region_size <= 9:
                fragmentation += 80

            elif region_size <= 16:
                fragmentation += 40

            else:
                fragmentation += 5

        score -= dead_regions * 250

        score -= fragmentation

        # -------------------------
        # too many regions
        # -------------------------

        score -= max(0, len(regions) - 1) * 50

        return max(score, 0)

    # =====================================================
    # UPDATE STATE
    # =====================================================

    def update(self, state):
        if not state.analysis_dirty:
            return

        regions = self.board.get_regions(state)

        remaining_areas = []

        for size, count in state.remaining_tiles.items():

            remaining_areas.extend(
                [size * size] * count
            )

        dead_regions = []
        fragmentation = 0

        for region in regions:

            region_size = len(region)

            possible = False

            for area in remaining_areas:

                if region_size % area == 0:

                    possible = True
                    break

            if not possible:

                dead_regions.append(region)

            if region_size <= 4:
                fragmentation += 120

            elif region_size <= 9:
                fragmentation += 80

            elif region_size <= 16:
                fragmentation += 40

            else:
                fragmentation += 5

        score = 1000
        score -= len(dead_regions) * 250
        score -= fragmentation
        score -= max(0, len(regions) - 1) * 50

        state.dead_regions = dead_regions
        state.score = max(score, 0)
        state.analysis_dirty = False