import math

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
        callback=None,
        font_size=24,
        hover_scale=1.06,
        bg_color=BUTTON_BG,
        hover_bg_color=BUTTON_HOVER,
        border_color=GRID_LINE_COLOR,
        hover_border_color=(120, 140, 255),
        text_color=BUTTON_TEXT,
        text_offset_y=0,
        pulse_amount=0.0,
        pulse_period=3200,
        glow_color=None,
        glow_alpha=0,
        hover_sound=None,
        click_sound=None
    ):
        self.text = text

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.callback = callback
        self.hover_scale = hover_scale
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.border_color = border_color
        self.hover_border_color = hover_border_color
        self.text_color = text_color
        self.text_offset_y = text_offset_y
        self.pulse_amount = pulse_amount
        self.pulse_period = pulse_period
        self.glow_color = glow_color
        self.glow_alpha = glow_alpha
        self.hover_sound = hover_sound
        self.click_sound = click_sound

        self.font = pygame.font.SysFont(
            "arial",
            font_size,
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
            hover_sound = self.hover_sound or audio.button_hover
            hover_sound.stop()
            hover_sound.play()

            Button._hovered_keys.add(self._hover_key)

        elif not hovered:
            Button._hovered_keys.discard(self._hover_key)

        scale = self.hover_scale if hovered else 1.0

        if hovered and self.pulse_amount:
            wave = math.sin(pygame.time.get_ticks() / max(1, self.pulse_period))
            scale += self.pulse_amount * wave

        draw_width = int(self.rect.width * scale)
        draw_height = int(self.rect.height * scale)
        draw_rect = pygame.Rect(0, 0, draw_width, draw_height)
        draw_rect.center = self.rect.center

        bg = self.hover_bg_color if hovered else self.bg_color

        border = self.hover_border_color if hovered else self.border_color

        if hovered and self.glow_color and self.glow_alpha > 0:
            glow_surface = pygame.Surface(
                (draw_rect.width + 26, draw_rect.height + 26),
                pygame.SRCALPHA
            )

            glow_rect = glow_surface.get_rect()
            glow_rect.inflate_ip(-10, -10)

            glow_alpha = self.glow_alpha
            if self.pulse_amount:
                wave = math.sin(pygame.time.get_ticks() / max(1, self.pulse_period))
                glow_alpha = max(0, min(180, int(glow_alpha + wave * 20)))

            pygame.draw.rect(
                glow_surface,
                (*self.glow_color, glow_alpha),
                glow_rect,
                border_radius=BUTTON_RADIUS + 8
            )

            screen.blit(
                glow_surface,
                (draw_rect.x - 13, draw_rect.y - 13)
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
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=draw_rect.center
        )
        text_rect.y += self.text_offset_y

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
                    click_sound = self.click_sound or audio.button_click
                    click_sound.play()

                    if self.callback:
                        self.callback()

                    return True

        return False