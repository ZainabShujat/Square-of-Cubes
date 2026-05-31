# =========================
# WINDOW
# =========================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650

MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 450

FPS = 60

TITLE = "Sum of Cubes"

# =========================
# LAYOUT
# =========================

OUTER_PADDING = 32
INNER_PADDING = 20

# =========================
# BOARD
# =========================

BOARD_SIZE = 45
GRID_SIZE = 45

CELL_SIZE = 16

BOARD_X = 40
BOARD_Y = 40

# =========================
# SIDEBAR
# =========================

SIDEBAR_WIDTH = 220

# =========================
# INVENTORY
# =========================

INVENTORY_HEIGHT = 140

# =========================
# COLORS
# =========================

BACKGROUND_COLOR = (5, 5, 28)

SIDEBAR_COLOR = (8, 8, 40)

INVENTORY_BG = (4, 4, 30)

TEXT_COLOR = (240, 240, 240)

PREVIEW_VALID = (120, 255, 120)

PREVIEW_INVALID = (255, 90, 90)

DEAD_ZONE_COLOR = (28, 28, 42)

GRID_LINE_COLOR = (70, 70, 130)

SELECTED_TILE_BG = (45, 45, 85)

NORMAL_TILE_BG = (24, 24, 52)

GRID_COLOR = GRID_LINE_COLOR

# =========================
# TILE COLORS
# =========================

TILE_COLORS = {
    1: (255, 94, 122),
    2: (255, 170, 64),
    3: (245, 255, 84),
    4: (88, 255, 132),
    5: (76, 231, 255),
    6: (92, 145, 255),
    7: (177, 109, 255),
    8: (255, 79, 214),
    9: (255, 208, 240),
}

# =========================
# TILE COUNTS
# =========================

INITIAL_TILE_COUNTS = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
}

PIECE_COLORS = [

    (255, 94, 122),    # ruby rose
    (255, 170, 64),    # fire opal
    (245, 255, 84),    # neon citrine
    (88, 255, 132),    # emerald glow
    (76, 231, 255),    # cyan crystal
    (92, 145, 255),    # sapphire blue
    (177, 109, 255),   # amethyst
    (255, 79, 214),    # magenta jewel
    (255, 208, 240),   # pearl blush

]


def get_tile_color(size):

    if size in TILE_COLORS:
        return TILE_COLORS[size]

    return PIECE_COLORS[(size - 1) % len(PIECE_COLORS)]

# =========================
# MENU
# =========================

BUTTON_WIDTH = 260
BUTTON_HEIGHT = 64

BUTTON_RADIUS = 16

BUTTON_BG = (32, 32, 68)
BUTTON_HOVER = (48, 48, 92)

BUTTON_TEXT = (240, 240, 255)

TOPBAR_HEIGHT = 72

SMALL_BUTTON_WIDTH = 120
SMALL_BUTTON_HEIGHT = 42