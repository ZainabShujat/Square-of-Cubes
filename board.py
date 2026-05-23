import pygame

from settings import *
from colors import *


class Board:

    def __init__(self):

        self.grid = [
            [0 for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

    # =========================
    # DRAW BOARD
    # =========================

    def draw(self, screen):

        for row in range(GRID_SIZE):

            for col in range(GRID_SIZE):

                x = OFFSET_X + col * CELL_SIZE
                y = OFFSET_Y + row * CELL_SIZE

                rect = pygame.Rect(
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )

                value = self.grid[row][col]

                # Filled tile
                if value != 0:

                    color = TILE_COLORS[value]

                    inner_rect = pygame.Rect(
                        x + 1,
                        y + 1,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2
                    )

                    pygame.draw.rect(
                        screen,
                        color,
                        inner_rect,
                        border_radius=4
                    )

                    # Fake shiny effect
                    shine = pygame.Rect(
                        x + 3,
                        y + 3,
                        CELL_SIZE // 2,
                        CELL_SIZE // 3
                    )

                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        shine,
                        border_radius=3
                    )

                # Grid outline
                pygame.draw.rect(
                    screen,
                    GRID,
                    rect,
                    1
                )

    # =========================
    # DRAGGING TILE
    # =========================

    def draw_dragging_tile(
        self,
        screen,
        size,
        mouse_x,
        mouse_y
    ):

        color = TILE_COLORS[size]

        start_x = (
            mouse_x
            - (size * CELL_SIZE // 2)
        )

        start_y = (
            mouse_y
            - (size * CELL_SIZE // 2)
        )

        for row in range(size):

            for col in range(size):

                x = start_x + col * CELL_SIZE
                y = start_y + row * CELL_SIZE

                rect = pygame.Rect(
                    x + 1,
                    y + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                )

                pygame.draw.rect(
                    screen,
                    color,
                    rect,
                    border_radius=4
                )

                shine = pygame.Rect(
                    x + 3,
                    y + 3,
                    CELL_SIZE // 2,
                    CELL_SIZE // 3
                )

                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    shine,
                    border_radius=3
                )

    # =========================
    # PREVIEW
    # =========================

    def draw_preview(
        self,
        screen,
        size,
        grid_y,
        grid_x,
        valid
    ):

        color = (
            GREEN_PREVIEW
            if valid
            else RED_PREVIEW
        )

        preview_surface = pygame.Surface(
            (
                size * CELL_SIZE,
                size * CELL_SIZE
            ),
            pygame.SRCALPHA
        )

        preview_surface.set_alpha(120)

        pygame.draw.rect(
            preview_surface,
            color,
            (
                0,
                0,
                size * CELL_SIZE,
                size * CELL_SIZE
            ),
            border_radius=8
        )

        screen.blit(
            preview_surface,
            (
                OFFSET_X + grid_x * CELL_SIZE,
                OFFSET_Y + grid_y * CELL_SIZE
            )
        )