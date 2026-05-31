import pygame

from core.fitmap import FitMap
from core.deadzones import DeadzoneDetector
from core.placements import PlacementGenerator
from core.mobility import MobilityAnalyzer


class AnalysisEngine:

    def __init__(self, board):

        self.board = board

        # ============================================
        # topology systems
        # ============================================

        self.fitmap = FitMap(board)

        self.deadzone_detector = DeadzoneDetector(
            board,
            self.fitmap
        )

        self.placement_generator = PlacementGenerator(
            board,
            self.fitmap
        )

        self.mobility_analyzer = MobilityAnalyzer(
            self.placement_generator
        )

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

        dead_regions = self.deadzone_detector.find_dead_regions(
            state
        )

        return len(dead_regions)

    # =====================================================
    # DEAD CELL COUNT
    # =====================================================

    def dead_cell_count(self, state):

        dead_cells = self.deadzone_detector.find_dead_cells(
            state
        )

        return len(dead_cells)

    # =====================================================
    # TOTAL FUTURE MOVES
    # =====================================================

    def total_future_moves(self, state):

        return self.placement_generator.total_moves(
            state
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
    # SOLVABILITY SCORE
    # =====================================================

    def solvability_score(self, state):

        score = 1000

        dead_cells = self.dead_cell_count(state)

        dead_regions = self.dead_region_count(state)

        fragmentation = self.fragmentation_score(state)

        mobility = self.mobility_analyzer.mobility_score(
            state
        )

        # ============================================
        # penalties
        # ============================================

        score -= dead_cells * 2

        score -= dead_regions * 150

        score -= fragmentation

        # ============================================
        # reward mobility
        # ============================================

        score += mobility

        return max(score, 0)

        # ============================================
        # penalties
        # ============================================

        score -= dead_cells * 2

        score -= dead_regions * 150

        score -= fragmentation

        # ============================================
        # reward flexibility
        # ============================================

        score += future_moves // 25

        return max(score, 0)

    # =====================================================
    # UPDATE STATE
    # =====================================================

    def update(self, state):

        if not state.analysis_dirty:
            return

        # ============================================
        # topology
        # ============================================

        dead_regions = self.deadzone_detector.find_dead_regions(
            state
        )

        deadzone_count = len(dead_regions)
        previous_deadzone_count = getattr(
            state,
            "deadzone_count",
            0
        )

        limit = (
            state.current_level.deadzone_limit
            if getattr(state, "current_level", None)
            else state.game_mode.deadzone_limit
        )

        score = self.solvability_score(state)

        mobility_data = self.mobility_analyzer.analyze(
            state
        )


        # ============================================
        # END STATE CHECKS
        # ============================================

        if self.board.is_full(state):

            state.game_won = True
            state.game_over = False

        elif limit is not None and deadzone_count >= limit:

            state.game_over = True
            state.game_won = False

        # ============================================
        # update state
        # ============================================

        state.dead_regions = dead_regions

        state.score = score

        state.mobility_data = mobility_data

        state.analysis_dirty = False

        state.previous_deadzone_count = previous_deadzone_count
        state.deadzone_count = deadzone_count

        if deadzone_count > previous_deadzone_count:

            state.alert_message = (
                "New dead zone formed."
            )
            state.alert_message_time = pygame.time.get_ticks()
            state.alert_kind = "deadzone"


       

            