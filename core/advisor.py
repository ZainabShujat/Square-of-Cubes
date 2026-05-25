class Advisor:

    def __init__(self):

        self.last_message = ""

    # =====================================================
    # MAIN EVALUATION
    # =====================================================

    def evaluate(self, state):

        mobility = state.mobility_data

        total_moves = mobility.get(
            "total_moves",
            0
        )

        largest_tile = mobility.get(
            "largest_available_tile",
            0
        )

        dead_regions = len(
            state.dead_regions
        )

        previous_moves = getattr(
            state,
            "previous_mobility",
            total_moves
        )

        move_delta = (
            total_moves - previous_moves
        )

        # =================================================
        # CRITICAL STATES
        # =================================================

        if dead_regions >= 4:

            return (
                "You're painting yourself into a corner."
            )

        if total_moves < 15:

            return (
                "You're running out of options."
            )

        # =================================================
        # LARGE TILE WARNING
        # =================================================

        if largest_tile <= 2:

            return (
                "Big pieces may become difficult soon."
            )

        # =================================================
        # STRONG NEGATIVE MOVE
        # =================================================

        if move_delta < -250:

            return (
                "That closed off a lot of space."
            )

        if move_delta < -120:

            return (
                "Careful. The board's getting tighter."
            )

        # =================================================
        # GOOD MOVES
        # =================================================

        if move_delta > 250:

            return (
                "Nice recovery."
            )

        if move_delta > 120:

            return (
                "That keeps things open."
            )

        # =================================================
        # FRAGMENTATION
        # =================================================

        if dead_regions > 0:

            return (
                "Tiny gaps are starting to form."
            )

        # =================================================
        # HEALTHY STATES
        # =================================================

        if total_moves > 1500:

            return (
                "Plenty of room to work with."
            )

        if total_moves > 900:

            return (
                "Board looks healthy."
            )

        # =================================================
        # DEFAULT
        # =================================================

        return (
            "Looking stable."
        )