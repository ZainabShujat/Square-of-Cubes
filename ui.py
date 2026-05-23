import pygame

from colors import *

inventory_boxes = {}

# =========================
# DRAW INVENTORY
# =========================

def draw_inventory(
    screen,
    font,
    tile_inventory,
    current_size
):

    global inventory_boxes

    inventory_boxes = {}

    # -------------------------
    # SIDEBAR BACKGROUND
    # -------------------------

    sidebar_width = 260
    sidebar_x = screen.get_width() - sidebar_width

    pygame.draw.rect(
    screen,
    (8, 8, 20),
    (
        sidebar_x,
        0,
        sidebar_width,
        screen.get_height()
    )
)

    # -------------------------
    # TITLE
    # -------------------------

    title_font = pygame.font.SysFont(
        "arial",
        26,
        bold=True
    )

    title = title_font.render(
        "Tile Inventory",
        True,
        WHITE
    )

    screen.blit(
        title,
        (sidebar_x + 20, 30)
    )

    # -------------------------
    # START POSITIONS
    # -------------------------

    start_x = sidebar_x + 25
    start_y = 90

    mini_cell = 6
    spacing = 14

    y = start_y

    # -------------------------
    # DRAW TILES
    # -------------------------

    for size in range(1, 10):

        color = TILE_COLORS[size]

        preview_size = size * 6
        cell = 6

        # clickable area
        rect = pygame.Rect(
            start_x,
            y,
            preview_size,
            preview_size
        )

        inventory_boxes[size] = rect

        # -------------------------
        # SELECTED GLOW
        # -------------------------

        if current_size is not None:

            if size == current_size:

                glow_rect = pygame.Rect(
                    start_x - 2,
                    y - 2,
                    preview_size + 4,
                    preview_size + 4
                )

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    glow_rect,
                    border_radius=8
                )

        # -------------------------
        # DRAW MINI TILE STACK
        # -------------------------

        for row in range(size):

            for col in range(size):

                tile_x = start_x + col * mini_cell
                tile_y = y + row * mini_cell

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        tile_x,
                        tile_y,
                        mini_cell - 1,
                        mini_cell - 1
                    ),
                    border_radius=3
                )

                # jewel shine
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        tile_x + 2,
                        tile_y + 2
                    ),
                    1
                )

        # -------------------------
        # COUNT TEXT
        # -------------------------

        count_text = font.render(
            f"x {tile_inventory[size]}",
            True,
            WHITE
        )

        text_y = y + (
            preview_size - count_text.get_height()
        ) // 2

        screen.blit(
            count_text,
            (
                start_x + preview_size + 18,
                text_y
            )
        )

        # next row
        y += preview_size + spacing