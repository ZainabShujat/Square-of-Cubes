import pygame

from utils.constants import *

from core.piece import Piece


class InventoryRenderer:

    def __init__(self):

        self.tile_boxes = {}
        self.preview_cell = 8
        self.count_font = pygame.font.SysFont(
            "arial",
            18,
            bold=True
        )

    # =====================================================
    # BACKGROUND
    # =====================================================

    def draw_background(
        self,
        screen
    ):

        rect = pygame.Rect(
            OUTER_PADDING,
            screen.get_height() - INVENTORY_HEIGHT,
            screen.get_width() - SIDEBAR_WIDTH - OUTER_PADDING,
            INVENTORY_HEIGHT
        )

        pygame.draw.rect(
            screen,
            INVENTORY_BG,
            rect,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (18, 18, 44),
            rect,
            width=2,
            border_radius=14
        )

        pygame.draw.line(
            screen,
            (40, 40, 70),
            (
                OUTER_PADDING,
                rect.y
            ),
            (
                screen.get_width() - SIDEBAR_WIDTH,
                rect.y
            ),
            3
        )

    # =====================================================
    # LAYOUT
    # =====================================================

    def compute_positions(
        self,
        screen,
        state,
        screen_width,
        screen_height
    ):

        self.tile_boxes = {}

        available_sizes = []

        for size, count in state.remaining_tiles.items():
            if count > 0:
                available_sizes.append(size)

        available_width = (
            screen_width
            - SIDEBAR_WIDTH
            - OUTER_PADDING * 2
        )

        gap = 20
        padding = 24
        preview_cell = 8

        while preview_cell > 4:
            total_width = 0

            for size in available_sizes:
                preview_size = size * preview_cell
                box_size = max(
                    58,
                    preview_size + padding
                )
                total_width += box_size

            total_width += max(0, len(available_sizes) - 1) * gap

            if total_width <= available_width:
                break

            preview_cell -= 1

        self.preview_cell = preview_cell

        box_sizes = {}
        total_width = 0

        for size in available_sizes:
            preview_size = size * self.preview_cell
            box_size = max(
                58,
                preview_size + padding
            )
            box_sizes[size] = box_size
            total_width += box_size

        total_width += max(0, len(available_sizes) - 1) * gap

        start_x = OUTER_PADDING + max(0, (available_width - total_width) // 2)
        current_x = start_x

        for size in available_sizes:
            box_size = box_sizes[size]

            rect = pygame.Rect(
                current_x,
                screen_height - INVENTORY_HEIGHT + OUTER_PADDING // 2,
                box_size,
                box_size
            )

            self.tile_boxes[size] = rect
            current_x += box_size + gap

    # =====================================================
    # TILE BOX
    # =====================================================

    def draw_tile_box(
        self,
        screen,
        state,
        size,
        rect
    ):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        hovered = rect.collidepoint(mouse_x, mouse_y)
        selected = state.selected_size == size

        if selected:
            bg = (60, 60, 120)
        elif hovered:
            bg = (42, 42, 72)
        else:
            bg = NORMAL_TILE_BG

        pygame.draw.rect(
            screen,
            bg,
            rect,
            border_radius=18
        )

        border_color = TILE_COLORS[size] if selected else GRID_COLOR

        pygame.draw.rect(
            screen,
            border_color,
            rect,
            width=2,
            border_radius=18
        )

        preview_cell = self.preview_cell
        preview_size = size * preview_cell

        start_x = rect.x + (rect.width - preview_size) // 2
        start_y = rect.y + (rect.height - preview_size) // 2

        color = TILE_COLORS[size]

        for row in range(size):
            for col in range(size):
                x = start_x + col * preview_cell
                y = start_y + row * preview_cell

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        x,
                        y,
                        7,
                        7
                    ),
                    border_radius=2
                )

        count = state.remaining_tiles[size]

        text = self.count_font.render(
            str(count),
            True,
            TEXT_COLOR
        )

        screen.blit(
            text,
            (
                rect.right - 18,
                rect.top + 6
            )
        )

    # =====================================================
    # CLICK
    # =====================================================

    def handle_click(
        self,
        state,
        mouse_x,
        mouse_y,
        screen_width,
        screen_height
    ):
        self.compute_positions(None, state, screen_width, screen_height)

        if mouse_y < screen_height - INVENTORY_HEIGHT:
            return False

        for size, rect in self.tile_boxes.items():
            if rect.collidepoint(mouse_x, mouse_y):
                if state.remaining_tiles[size] > 0:
                    state.selected_size = size
                    state.dragging_piece = Piece(size)
                    return True

        return False

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen,
        state,
        screen_width,
        screen_height
    ):

        self.draw_background(screen)
        self.compute_positions(screen, state, screen_width, screen_height)

        for size, rect in self.tile_boxes.items():
            self.draw_tile_box(
                screen,
                state,
                size,
                rect
            )
