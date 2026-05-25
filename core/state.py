from core.piece import Piece
from utils.constants import INITIAL_TILE_COUNTS
from core.game_modes import STANDARD



class GameState:

    def __init__(self):
        self.solvable = True
        self.confirm_dialog = None

        # =========================
        # board pieces
        # =========================

        self.placed_pieces = []

        # =========================
        # inventory
        # =========================

        self.remaining_tiles = INITIAL_TILE_COUNTS.copy()

        # =========================
        # selected tile size
        # =========================

        self.selected_size = None

        # =========================
        # dragging state
        # =========================

        self.dragging_piece = None

        # =========================
        # preview
        # =========================

        self.preview_x = None
        self.preview_y = None

        self.preview_valid = False

        # =========================
        # analysis
        # =========================

        self.dead_regions = []
        self.mobility_data = {}
        self.deadzone_count = 0
        self.previous_deadzone_count = 0
        self.score = 0
        self.advisor_message = ""
        self.advisor_message_time = 0
        self.advisor_message_duration = 2200
        self.alert_message = ""
        self.alert_message_time = 0
        self.alert_message_duration = 2400
        self.alert_kind = ""

        self.analysis_dirty = True

        # =========================
        # animations
        # =========================

        self.tile_animations = []

        # =================================================
        # GAME MODE
        # =================================================

        self.game_mode = STANDARD

        self.game_over = False
        self.game_over_sound_played = False
        self.game_won = False
        self.win_sound_played = False

        self.mode_transition_active = False
        self.mode_transition_phase = ""
        self.mode_transition_alpha = 0
        self.mode_transition_target = None
        self.mode_transition_next_mode = None

        
        

    # =====================================================
    # INVENTORY
    # =====================================================

    def can_take_tile(self, size):

        return self.remaining_tiles[size] > 0

    def take_tile(self, size):

        if self.can_take_tile(size):

            self.remaining_tiles[size] -= 1
            self.analysis_dirty = True

            return True

        return False

    def return_tile(self, size):

        self.remaining_tiles[size] += 1
        self.analysis_dirty = True

    # =====================================================
    # PIECES
    # =====================================================

    def add_piece(self, piece):

        self.placed_pieces.append(piece)
        self.analysis_dirty = True

    def remove_piece(self, piece):

        if piece in self.placed_pieces:
            self.placed_pieces.remove(piece)
            self.analysis_dirty = True

    # =====================================================
    # BOARD LOOKUP
    # =====================================================

    def get_piece_at(self, grid_x, grid_y):

        for piece in reversed(self.placed_pieces):

            if piece.contains(grid_x, grid_y):
                return piece

        return None

    # =====================================================
    # ANIMATIONS
    # =====================================================

    def add_tile_animation(self, animation_type, **data):

        self.tile_animations.append({
            "type": animation_type,
            **data
        })

    def clear_finished_tile_animations(self, current_time):

        active_animations = []

        for animation in self.tile_animations:

            start_time = animation.get("start_time", current_time)
            duration = animation.get("duration", 0)

            if current_time - start_time < duration:
                active_animations.append(animation)

        self.tile_animations = active_animations
    