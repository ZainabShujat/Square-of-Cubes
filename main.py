import sys
import ctypes
import pygame

from utils.constants import *

from core.board import Board
from core.state import GameState
from core.analysis import AnalysisEngine

from rendering.board_renderer import BoardRenderer
from rendering.inventory_renderer import InventoryRenderer
from rendering.ui_renderer import UIRenderer

try:
    from pygame._sdl2.video import Window
except ImportError:
    Window = None


# =====================================================
# INIT
# =====================================================

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


# =====================================================
# SYSTEMS
# =====================================================

board = Board()

state = GameState()

analysis = AnalysisEngine(board)

board_renderer = BoardRenderer()

inventory_renderer = InventoryRenderer()

ui_renderer = UIRenderer()


# =====================================================
# MAIN LOOP
# =====================================================

running = True

while running:

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # =================================================
    # EVENTS
    # =================================================

    for event in pygame.event.get():

        # -------------------------------------------------
        # QUIT
        # -------------------------------------------------

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        # -------------------------------------------------
        # WINDOW RESIZE
        # -------------------------------------------------

        elif event.type == pygame.VIDEORESIZE:

            new_width = max(event.w, MIN_WINDOW_WIDTH)
            new_height = max(event.h, MIN_WINDOW_HEIGHT)

            screen = pygame.display.set_mode(
                (new_width, new_height),
                pygame.RESIZABLE
            )

            window_style_applied = False

        # -------------------------------------------------
        # MOUSE DOWN
        # -------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                # =========================================
                # INVENTORY CLICK
                # =========================================

                clicked_inventory = (
                    inventory_renderer.handle_click(
                        state,
                        mouse_x,
                        mouse_y,
                        screen_width,
                        screen_height
                    )
                )

                # =========================================
                # PICK EXISTING TILE
                # =========================================

                if not clicked_inventory:

                    grid_x, grid_y = (
                        board_renderer.screen_to_grid(
                            screen,
                            mouse_x,
                            mouse_y,
                            screen_width,
                            screen_height
                        )
                    )

                    piece = state.get_piece_at(
                        grid_x,
                        grid_y
                    )

                    if piece:

                        state.remove_piece(piece)

                        state.return_tile(
                            piece.size
                        )

                        state.dragging_piece = piece

                        state.selected_size = (
                            piece.size
                        )

        # -------------------------------------------------
        # MOUSE UP
        # -------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                if state.dragging_piece:

                    piece = state.dragging_piece

                    grid_x, grid_y = (
                        board_renderer.screen_to_grid(
                            screen,
                            mouse_x,
                            mouse_y,
                            screen_width,
                            screen_height
                        )
                    )

                    valid = board.can_place(
                        state,
                        piece.size,
                        grid_x,
                        grid_y
                    )

                    if valid:

                        piece.grid_x = grid_x
                        piece.grid_y = grid_y

                        state.add_piece(piece)

                        state.take_tile(piece.size)

                    state.dragging_piece = None

        # -------------------------------------------------
        # MOUSE MOVE
        # -------------------------------------------------

        elif event.type == pygame.MOUSEMOTION:

            if state.dragging_piece:

                grid_x, grid_y = (
                    board_renderer.screen_to_grid(
                        screen,
                        mouse_x,
                        mouse_y,
                        screen_width,
                        screen_height
                    )
                )

                state.preview_x = grid_x
                state.preview_y = grid_y

                state.preview_valid = (
                    board.can_place(
                        state,
                        state.dragging_piece.size,
                        grid_x,
                        grid_y
                    )
                )

    # =====================================================
    # ANALYSIS
    # =====================================================

    analysis.update(state)

    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(BACKGROUND_COLOR)

    # -----------------------------------------------------
    # BOARD
    # -----------------------------------------------------

    board_renderer.draw(
        screen,
        state,
        board,
        mouse_x,
        mouse_y,
        screen_width,
        screen_height
    )

    # -----------------------------------------------------
    # INVENTORY
    # -----------------------------------------------------

    inventory_renderer.draw(
        screen,
        state,
        screen_width,
        screen_height
    )

    # -----------------------------------------------------
    # UI
    # -----------------------------------------------------

    ui_renderer.draw(
        screen,
        state,
        screen_width,
        screen_height
    )

    pygame.display.flip()
    clock.tick(FPS)