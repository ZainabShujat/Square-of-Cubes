import pygame

from utils.constants import *


class BoardRenderer:

    def __init__(self):

        self.base_cell_size = CELL_SIZE
        self.cell_size = CELL_SIZE

    # =====================================================
    # BOARD RECT
    # =====================================================

    def get_board_rect(
        self,
        screen_width,
        screen_height
    ):

        available_width = (
            screen_width
            - SIDEBAR_WIDTH
            - OUTER_PADDING * 2
        )

        available_height = (
            screen_height
            - INVENTORY_HEIGHT
            - OUTER_PADDING * 2
        )

        max_board_size = min(
            available_width,
            available_height
        )

        self.cell_size = max(
            8,
            min(
                self.base_cell_size,
                max_board_size // GRID_SIZE
            )
        )

        board_pixel_size = GRID_SIZE * self.cell_size

        board_x = OUTER_PADDING + max(
            0,
            (available_width - board_pixel_size) // 2
        )

        board_y = OUTER_PADDING + max(
            0,
            (available_height - board_pixel_size) // 2
        )

        return pygame.Rect(
            board_x,
            board_y,
            board_pixel_size,
            board_pixel_size
        )

    # =====================================================
    # SCREEN TO GRID
    # =====================================================

    def screen_to_grid(
        self,
        screen,
        mouse_x,
        mouse_y,
        screen_width,
        screen_height
    ):

        board_rect = self.get_board_rect(
            screen_width,
            screen_height
        )

        grid_x = (
            mouse_x - board_rect.x
        ) // self.cell_size

        grid_y = (
            mouse_y - board_rect.y
        ) // self.cell_size

        return int(grid_x), int(grid_y)

    # =====================================================
    # DRAW PIECE
    # =====================================================

    def draw_piece(
        self,
        screen,
        piece,
        offset_x,
        offset_y,
        alpha=255
    ):

        color = piece.color

        dark_color = (
            max(color[0] - 55, 0),
            max(color[1] - 55, 0),
            max(color[2] - 55, 0)
        )

        glow_color = (
            min(color[0] + 50, 255),
            min(color[1] + 50, 255),
            min(color[2] + 50, 255)
        )

        for row in range(piece.size):

            for col in range(piece.size):

                x = (
                    offset_x
                    + col * self.cell_size
                    + 2
                )

                y = (
                    offset_y
                    + row * self.cell_size
                    + 2
                )

                size = self.cell_size - 4

                # outer glow
                glow_surface = pygame.Surface(
                    (size + 10, size + 10),
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    glow_surface,
                    (*glow_color, 50),
                    (0, 0, size + 10, size + 10),
                    border_radius=8
                )

                screen.blit(
                    glow_surface,
                    (x - 5, y - 5)
                )

                # main cube
                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, size, size),
                    border_radius=6
                )

                # dark border
                pygame.draw.rect(
                    screen,
                    dark_color,
                    (x, y, size, size),
                    2,
                    border_radius=6
                )

                # top shine
                pygame.draw.rect(
                    screen,
                    (255, 255, 255, 70),
                    (
                        x + 2,
                        y + 2,
                        size - 4,
                        size // 3
                    ),
                    border_radius=4
                )

    # =====================================================
    # DRAW BOARD
    # =====================================================

    def draw(
        self,
        screen,
        state,
        board,
        mouse_x,
        mouse_y,
        screen_width,
        screen_height
    ):

        board_rect = self.get_board_rect(
            screen_width,
            screen_height
        )

        play_area_rect = pygame.Rect(
            OUTER_PADDING,
            OUTER_PADDING,
            screen_width - SIDEBAR_WIDTH - OUTER_PADDING * 2,
            screen_height - INVENTORY_HEIGHT - OUTER_PADDING * 2
        )

        pygame.draw.rect(
            screen,
            (10, 10, 30),
            play_area_rect,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (18, 18, 45),
            board_rect,
            border_radius=16
        )

        for row in range(GRID_SIZE):

            for col in range(GRID_SIZE):

                rect = pygame.Rect(
                    board_rect.x + col * self.cell_size,
                    board_rect.y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(
                    screen,
                    GRID_LINE_COLOR,
                    rect,
                    1
                )

        # dead regions
        for region in state.dead_regions:

            for cell in region:

                x, y = cell

                rect = pygame.Rect(
                    board_rect.x + x * self.cell_size,
                    board_rect.y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(
                    screen,
                    DEAD_ZONE_COLOR,
                    rect
                )

        # placed pieces
        for piece in state.placed_pieces:

            px = (
                board_rect.x
                + piece.grid_x * self.cell_size
            )

            py = (
                board_rect.y
                + piece.grid_y * self.cell_size
            )

            self.draw_piece(
                screen,
                piece,
                px,
                py
            )

        # dragging preview
        if state.dragging_piece:

            piece = state.dragging_piece

            grid_x, grid_y = self.screen_to_grid(
                screen,
                mouse_x,
                mouse_y,
                screen_width,
                screen_height
            )

            preview_x = (
                board_rect.x
                + grid_x * self.cell_size
            )

            preview_y = (
                board_rect.y
                + grid_y * self.cell_size
            )

            self.draw_piece(
                screen,
                piece,
                preview_x,
                preview_y,
                alpha=120
            )

            drag_x = (
                mouse_x
                - (
                    piece.size * self.cell_size
                ) // 2
            )

            drag_y = (
                mouse_y
                - (
                    piece.size * self.cell_size
                ) // 2
            )

            self.draw_piece(
                screen,
                piece,
                drag_x,
                drag_y
            )