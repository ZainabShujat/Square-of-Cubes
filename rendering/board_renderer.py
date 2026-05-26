import math

import pygame

from utils.constants import *


class BoardRenderer:

    def __init__(self):

        self.base_cell_size = CELL_SIZE
        self.cell_size = CELL_SIZE

    def brighten_color(self, color, amount):

        return (
            min(255, int(color[0] * amount)),
            min(255, int(color[1] * amount)),
            min(255, int(color[2] * amount))
        )

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
        alpha=255,
        scale=1.0,
        shake_x=0,
        shake_y=0
    ):

        color = self.brighten_color(
            piece.color,
            1.12 if alpha >= 255 else 1.22
        )

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

        cell_size = max(1, int(self.cell_size * scale))

        if alpha < 255:

            tile_pixel_size = piece.size * cell_size

            piece_surface = pygame.Surface(
                (tile_pixel_size + 12, tile_pixel_size + 12),
                pygame.SRCALPHA
            )

            for row in range(piece.size):

                for col in range(piece.size):

                    x = 6 + col * cell_size + 2 + shake_x
                    y = 6 + row * cell_size + 2 + shake_y
                    size = max(1, cell_size - 4)

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

                    piece_surface.blit(
                        glow_surface,
                        (x - 5, y - 5)
                    )

                    pygame.draw.rect(
                        piece_surface,
                        color,
                        (x, y, size, size),
                        border_radius=6
                    )

                    pygame.draw.rect(
                        piece_surface,
                        dark_color,
                        (x, y, size, size),
                        2,
                        border_radius=6
                    )

                    pygame.draw.rect(
                        piece_surface,
                        (255, 255, 255, 70),
                        (
                            x + 2,
                            y + 2,
                            size - 4,
                            size // 3
                        ),
                        border_radius=4
                    )

            piece_surface.set_alpha(alpha)
            screen.blit(piece_surface, (offset_x - 6, offset_y - 6))

            return

        for row in range(piece.size):

            for col in range(piece.size):

                x = (
                    offset_x
                    + col * cell_size
                    + 2
                    + shake_x
                )

                y = (
                    offset_y
                    + row * cell_size
                    + 2
                    + shake_y
                )

                size = max(1, cell_size - 4)

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

    def draw_place_sparkles(
        self,
        screen,
        piece,
        offset_x,
        offset_y,
        progress
    ):

        tile_pixel_size = piece.size * self.cell_size
        center_x = offset_x + tile_pixel_size // 2
        center_y = offset_y + tile_pixel_size // 2
        half_size = tile_pixel_size // 2

        sparkle_count = min(12, 4 + piece.size)
        base_radius = max(
            5,
            int(tile_pixel_size * (0.12 + piece.size * 0.03))
        )

        for index in range(sparkle_count):

            edge_index = index % 4
            edge_progress = (index / sparkle_count + progress * 0.85) % 1.0

            if edge_index == 0:
                sparkle_x = offset_x + int(edge_progress * tile_pixel_size)
                sparkle_y = offset_y - 2
            elif edge_index == 1:
                sparkle_x = offset_x + tile_pixel_size + 2
                sparkle_y = offset_y + int(edge_progress * tile_pixel_size)
            elif edge_index == 2:
                sparkle_x = offset_x + int((1.0 - edge_progress) * tile_pixel_size)
                sparkle_y = offset_y + tile_pixel_size + 2
            else:
                sparkle_x = offset_x - 2
                sparkle_y = offset_y + int((1.0 - edge_progress) * tile_pixel_size)

            pull = int(base_radius * (0.2 + 0.8 * progress))

            if sparkle_x < center_x:
                sparkle_x -= pull
            elif sparkle_x > center_x:
                sparkle_x += pull

            if sparkle_y < center_y:
                sparkle_y -= pull
            elif sparkle_y > center_y:
                sparkle_y += pull

            sparkle_size = max(2, int(5 * (1.0 - progress * 0.7)))

            sparkle_color = (
                min(255, 220 + index * 5),
                min(255, 235 + index * 3),
                140
            )

            pygame.draw.circle(
                screen,
                sparkle_color,
                (sparkle_x, sparkle_y),
                sparkle_size
            )

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (sparkle_x - sparkle_size * 2, sparkle_y),
                (sparkle_x + sparkle_size * 2, sparkle_y),
                1
            )

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (sparkle_x, sparkle_y - sparkle_size * 2),
                (sparkle_x, sparkle_y + sparkle_size * 2),
                1
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

        theme = getattr(state.game_mode, "theme", {})
        play_area_color = theme.get("board_fill", (10, 10, 30))
        board_color = theme.get("panel_fill", (18, 18, 45))
        grid_color = theme.get("accent_soft", GRID_LINE_COLOR)

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
            play_area_color,
            play_area_rect,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            board_color,
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
                    grid_color,
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

        current_time = pygame.time.get_ticks()
        state.clear_finished_tile_animations(current_time)

        # placement / invalid-drop animations
        for animation in state.tile_animations:

            start_time = animation.get("start_time", current_time)
            duration = max(1, animation.get("duration", 1))
            elapsed = current_time - start_time
            progress = max(0.0, min(1.0, elapsed / duration))

            if animation["type"] == "place":

                piece = animation["piece"]
                grid_x = animation["grid_x"]
                grid_y = animation["grid_y"]
                pulse = 0.92 + 0.08 * (1.0 - abs(1.0 - progress * 2.0))

                px = board_rect.x + grid_x * self.cell_size
                py = board_rect.y + grid_y * self.cell_size

                self.draw_piece(
                    screen,
                    piece,
                    px,
                    py,
                    scale=pulse
                )

                self.draw_place_sparkles(
                    screen,
                    piece,
                    px,
                    py,
                    progress
                )

            elif animation["type"] == "invalid":

                piece = animation["piece"]
                grid_x = animation["grid_x"]
                grid_y = animation["grid_y"]
                shake_x = int(5 * math.sin(progress * 24.0))
                shake_y = int(2 * math.sin(progress * 48.0))

                px = board_rect.x + grid_x * self.cell_size
                py = board_rect.y + grid_y * self.cell_size

                self.draw_piece(
                    screen,
                    piece,
                    px,
                    py,
                    shake_x=shake_x,
                    shake_y=shake_y
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