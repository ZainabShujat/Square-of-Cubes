import pygame

from utils.constants import *


class UIRenderer:

    def __init__(self):

        self.title_font = pygame.font.SysFont(
            "arial",
            34,
            bold=True
        )

        self.status_font = pygame.font.SysFont(
            "arial",
            32,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            24
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            18
        )

    def get_status_text(self, state):

        deadzone_count = getattr(state, "deadzone_count", len(state.dead_regions))
        limit = getattr(state.game_mode, "deadzone_limit", None)

        if limit is not None and deadzone_count >= limit:

            return (
                "UNSOLVABLE",
                (255, 90, 90)
            )

        if limit is not None and deadzone_count >= max(1, limit - 1):

            return (
                "CRITICAL",
                (255, 150, 90)
            )

        if deadzone_count > 0:

            return (
                "WARNING",
                (255, 210, 90)
            )

        return (
            "STABLE",
            (120, 255, 120)
        )

    def get_board_health_text(self, state):

        mobility = getattr(state, "mobility_data", {})
        total_moves = mobility.get("total_moves", 0)
        largest_tile = mobility.get("largest_available_tile", 0)
        deadzone_count = getattr(state, "deadzone_count", len(state.dead_regions))

        if deadzone_count > 0 or total_moves < 20:
            return ("Tight", (255, 170, 90))

        if total_moves > 900 or largest_tile >= 4:
            return ("Healthy", (120, 255, 150))

        return ("Open", (150, 220, 255))

    def get_mode_theme(self, state):

        return getattr(state.game_mode, "theme", {})

    def draw_panel_card(self, screen, rect, fill_color=(18, 18, 42), border_color=(84, 92, 160)):

        pygame.draw.rect(screen, fill_color, rect, border_radius=14)
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=14)

    def draw_label_value(
        self,
        screen,
        label,
        value,
        label_font,
        value_font,
        x,
        y,
        label_color,
        value_color
    ):

        label_surf = label_font.render(label, True, label_color)
        value_surf = value_font.render(value, True, value_color)

        screen.blit(label_surf, (x, y))
        screen.blit(value_surf, (x, y + label_surf.get_height() + 4))

        return y + label_surf.get_height() + value_surf.get_height() + 10

    def draw_wrapped_text(
        self,
        screen,
        text,
        font,
        color,
        x,
        y,
        max_width,
        line_gap=8
    ):

        words = text.split()
        lines = []
        current_line = ""

        for word in words:

            test_line = word if not current_line else f"{current_line} {word}"

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        current_y = y

        for line in lines:
            surf = font.render(line, True, color)
            screen.blit(surf, (x, current_y))
            current_y += font.get_height() + line_gap

        return current_y

    def draw(
        self,
        screen,
        state,
        screen_width,
        screen_height,
        board_rect
    ):

        theme = self.get_mode_theme(state)
        sidebar_bg = theme.get("sidebar_bg", SIDEBAR_COLOR)
        panel_fill = theme.get("panel_fill", (18, 18, 42))
        panel_border = theme.get("panel_border", (84, 92, 160))
        title_accent = theme.get("accent", TEXT_COLOR)
        label_accent = theme.get("accent_soft", (165, 170, 195))

        panel_width = SIDEBAR_WIDTH

        panel_x = (
            screen_width
            - SIDEBAR_WIDTH
            + INNER_PADDING
        )

        pygame.draw.rect(
            screen,
            sidebar_bg,
            (
                screen_width - SIDEBAR_WIDTH,
                0,
                SIDEBAR_WIDTH,
                screen_height
            )
        )

        title = self.title_font.render(
            "Sum of Cubes",
            True,
            title_accent
        )

        screen.blit(
            title,
            (panel_x, OUTER_PADDING + 12)
        )

        navbar_rect = pygame.Rect(
            screen_width - SIDEBAR_WIDTH + 8,
            76,
            SIDEBAR_WIDTH - 16,
            52
        )

        pygame.draw.rect(
            screen,
            theme.get("banner_fill", (12, 12, 50)),
            navbar_rect,
            border_radius=14
        )

        pygame.draw.line(
            screen,
            theme.get("banner_border", theme.get("accent_soft", (90, 100, 170))),
            (navbar_rect.x + 10, navbar_rect.bottom),
            (navbar_rect.right - 10, navbar_rect.bottom),
            1
        )

        section_x = panel_x
        section_width = panel_width - 40

        label, color = self.get_status_text(state)

        status_rect = pygame.Rect(section_x - 10, 142, section_width + 20, 78)
        mode_rect = pygame.Rect(section_x - 10, 236, section_width + 20, 72)
        deadzone_rect = pygame.Rect(section_x - 10, 330, section_width + 20, 78)
        health_rect = pygame.Rect(section_x - 10, 426, section_width + 20, 72)

        self.draw_panel_card(screen, status_rect, fill_color=panel_fill, border_color=panel_border)
        self.draw_panel_card(screen, mode_rect, fill_color=panel_fill, border_color=panel_border)
        self.draw_panel_card(screen, deadzone_rect, fill_color=panel_fill, border_color=panel_border)
        self.draw_panel_card(screen, health_rect, fill_color=panel_fill, border_color=panel_border)

        status_label = self.small_font.render(
            "Main Status",
            True,
            label_accent
        )
        screen.blit(status_label, (section_x + 10, 150))

        status = self.status_font.render(
            label,
            True,
            color
        )
        screen.blit(status, (section_x + 10, 172))

        mode_name = getattr(state.game_mode, "name", "STANDARD")
        mode_value = f"{mode_name} MODE"

        self.draw_label_value(
            screen,
            "Game Mode",
            mode_value,
            self.small_font,
            self.text_font,
            section_x + 10,
            244,
            label_accent,
            TEXT_COLOR
        )

        deadzone_count = getattr(state, "deadzone_count", len(state.dead_regions))
        limit = getattr(state.game_mode, "deadzone_limit", None)
        if limit is None:
            deadzone_value = f"Dead Zones: {deadzone_count}"
        else:
            deadzone_value = f"Dead Zones: {deadzone_count} / {limit}"

        deadzone_color = self.get_status_text(state)[1]

        self.draw_label_value(
            screen,
            "Run Tension",
            deadzone_value,
            self.small_font,
            self.text_font,
            section_x + 10,
            338,
            label_accent,
            deadzone_color
        )

        health_label, health_color = self.get_board_health_text(state)
        self.draw_label_value(
            screen,
            "Board Health",
            health_label,
            self.small_font,
            self.text_font,
            section_x + 10,
            434,
            label_accent,
            health_color
        )

        # alert banner above the board
        msg = getattr(state, "alert_message", None)
        start = getattr(state, "alert_message_time", 0)
        duration = getattr(state, "alert_message_duration", 2400)
        kind = getattr(state, "alert_kind", "")

        if msg and start > 0:

            current = pygame.time.get_ticks()
            elapsed = current - start

            if elapsed < duration:

                alpha = int(255 * (1.0 - elapsed / duration))

                banner_color = theme.get("banner_fill", (28, 28, 58))
                border_color = theme.get("banner_border", (130, 140, 220))
                text_color = theme.get("accent", (210, 224, 255))

                if kind == "deadzone":
                    banner_color = (58, 20, 28)
                    border_color = (255, 120, 120)
                    text_color = (255, 220, 220)

                text_surface = self.text_font.render(msg, True, text_color)
                text_width = text_surface.get_width()
                banner_width = min(
                    board_rect.width,
                    max(180, text_width + 28)
                )
                banner_x = board_rect.x + (board_rect.width - banner_width) // 2
                banner_y = max(10, board_rect.y - 56)

                banner_surface = pygame.Surface(
                    (banner_width, 44),
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    banner_surface,
                    banner_color,
                    banner_surface.get_rect(),
                    border_radius=14
                )

                pygame.draw.rect(
                    banner_surface,
                    border_color,
                    banner_surface.get_rect(),
                    width=2,
                    border_radius=14
                )

                banner_surface.set_alpha(alpha)
                screen.blit(banner_surface, (banner_x, banner_y))

                text_surface.set_alpha(alpha)
                text_x = banner_x + (banner_width - text_surface.get_width()) // 2
                text_y = banner_y + (44 - text_surface.get_height()) // 2 - 1
                screen.blit(text_surface, (text_x, text_y))