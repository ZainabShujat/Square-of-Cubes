import pygame
import sys

from settings import *
from colors import *

from board import Board
from logic import *
from inventory import tile_inventory

import ui

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)
current_width = WIDTH
current_height = HEIGHT

pygame.display.set_caption(
    "Square of Cubes"
)

clock = pygame.time.Clock()

board = Board()

dragging = False
dragged_size = None


def get_drag_anchor(mouse_x, mouse_y, size):
    return (
        (mouse_x - OFFSET_X - (size * CELL_SIZE // 2)) // CELL_SIZE,
        (mouse_y - OFFSET_Y - (size * CELL_SIZE // 2)) // CELL_SIZE,
    )

running = True

while running:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        # QUIT
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------------------------
        # START DRAGGING
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                for size, rect in ui.inventory_boxes.items():

                    if rect.collidepoint(mouse_x, mouse_y):

                        if tile_inventory[size] > 0:

                            dragging = True
                            dragged_size = size

        # -------------------------
        # DROP TILE
        # -------------------------

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if dragging:

                    grid_x, grid_y = get_drag_anchor(
                        mouse_x,
                        mouse_y,
                        dragged_size
                    )

                    if (
                        0 <= grid_x < GRID_SIZE and
                        0 <= grid_y < GRID_SIZE
                    ):

                        if can_place(
                            board.grid,
                            dragged_size,
                            grid_y,
                            grid_x
                        ):

                            place_tile(
                                board.grid,
                                dragged_size,
                                grid_y,
                                grid_x
                            )

                            tile_inventory[dragged_size] -= 1

                    dragging = False
                    dragged_size = None

    # -------------------------
    # DRAW
    # -------------------------

    screen.fill(BACKGROUND)

    board.draw(screen)

    # -------------------------
    # PREVIEW
    # -------------------------

    if dragging:

        grid_x, grid_y = get_drag_anchor(mouse_x, mouse_y, dragged_size)

        valid = can_place(
            board.grid,
            dragged_size,
            grid_y,
            grid_x
        )

        board.draw_preview(
            screen,
            dragged_size,
            grid_y,
            grid_x,
            valid
        )

        board.draw_dragging_tile(
            screen,
            dragged_size,
            mouse_x,
            mouse_y
        )

    # -------------------------
    # UI
    # -------------------------

    font = pygame.font.SysFont(
        "arial",
        28
    )

    ui.draw_inventory(
        screen,
        font,
        tile_inventory,
        dragged_size
    )

    pygame.display.flip()

    clock.tick(FPS)