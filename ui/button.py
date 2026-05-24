import pygame
import audio

from utils.constants import *


class Button:

    _hovered_keys = set()

    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        callback=None
    ):
        self.text = text

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.callback = callback

        self.font = pygame.font.SysFont(
            "arial",
            24,
            bold=True
        )
        self._hover_key = (
            self.text,
            x,
            y,
            width,
            height
        )

    # =====================================================
    # HOVER
    # =====================================================

    def is_hovered(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        return self.rect.collidepoint(
            mouse_x,
            mouse_y
        )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        hovered = self.is_hovered()

        if hovered and self._hover_key not in Button._hovered_keys:
            audio.button_hover.stop()
            audio.button_hover.play()

            Button._hovered_keys.add(self._hover_key)

        elif not hovered:
            Button._hovered_keys.discard(self._hover_key)

        scale = 1.06 if hovered else 1.0
        draw_width = int(self.rect.width * scale)
        draw_height = int(self.rect.height * scale)
        draw_rect = pygame.Rect(0, 0, draw_width, draw_height)
        draw_rect.center = self.rect.center

        bg = (
            BUTTON_HOVER
            if hovered
            else BUTTON_BG
        )

        border = (
            (120, 140, 255)
            if hovered
            else GRID_LINE_COLOR
        )

        pygame.draw.rect(
            screen,
            bg,
            draw_rect,
            border_radius=BUTTON_RADIUS
        )

        pygame.draw.rect(
            screen,
            border,
            draw_rect,
            width=2,
            border_radius=BUTTON_RADIUS
        )

        text_surface = self.font.render(
            self.text,
            True,
            BUTTON_TEXT
        )

        text_rect = text_surface.get_rect(
            center=draw_rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    # =====================================================
    # CLICK
    # =====================================================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            

            if event.button == 1:

                if self.is_hovered():
                    audio.button_click.play()

                    if self.callback:
                        self.callback()

                    return True

        return False