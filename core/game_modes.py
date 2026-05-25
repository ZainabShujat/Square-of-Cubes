class GameMode:

    def __init__(
        self,
        name,
        deadzone_limit,
        description,
        theme=None
    ):

        self.name = name

        self.deadzone_limit = deadzone_limit

        self.description = description

        self.theme = theme or {}


# =====================================================
# MODES
# =====================================================

ENDLESS = GameMode(
    name="ENDLESS",

    deadzone_limit=None,

    description=(
        "No deadzone limit. "
        "Play freely and experiment."
    ),

    theme={
        "screen_tint": (8, 18, 34),
        "overlay_alpha": 24,
        "sidebar_bg": (8, 18, 42),
        "panel_fill": (16, 30, 60),
        "panel_border": (100, 200, 255),
        "accent": (90, 220, 255),
        "accent_soft": (70, 160, 220),
        "banner_fill": (18, 36, 58),
        "banner_border": (110, 210, 255),
        "board_fill": (9, 17, 35),
        "inventory_fill": (8, 14, 30)
    }
)

STANDARD = GameMode(
    name="STANDARD",

    deadzone_limit=4,

    description=(
        "Too many deadzones "
        "ends the run."
    ),

    theme={
        "screen_tint": (6, 8, 24),
        "overlay_alpha": 22,
        "sidebar_bg": (10, 10, 40),
        "panel_fill": (20, 20, 54),
        "panel_border": (120, 135, 255),
        "accent": (170, 180, 255),
        "accent_soft": (110, 120, 210),
        "banner_fill": (24, 24, 58),
        "banner_border": (130, 140, 220),
        "board_fill": (10, 10, 30),
        "inventory_fill": (6, 6, 28)
    }
)

HARDCORE = GameMode(
    name="HARDCORE",

    deadzone_limit=1,

    description=(
        "Every deadzone matters."
    ),

    theme={
        "screen_tint": (24, 6, 10),
        "overlay_alpha": 14,
        "sidebar_bg": (28, 8, 14),
        "panel_fill": (44, 12, 20),
        "panel_border": (255, 100, 100),
        "accent": (255, 120, 120),
        "accent_soft": (190, 70, 70),
        "banner_fill": (58, 18, 24),
        "banner_border": (255, 120, 120),
        "board_fill": (18, 8, 12),
        "inventory_fill": (20, 8, 14)
    }
)


# =====================================================
# MODE REGISTRY
# =====================================================

GAME_MODES = {

    "ENDLESS": ENDLESS,

    "STANDARD": STANDARD,

    "HARDCORE": HARDCORE
}