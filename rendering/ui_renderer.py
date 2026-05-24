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

        if len(state.dead_regions) > 0:

            return (
                "UNSOLVABLE",
                (255, 100, 100)
            )

        return (
            "STABLE",
            (120, 255, 120)
        )

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
        screen_height
    ):

        panel_width = SIDEBAR_WIDTH

        panel_x = (
            screen_width
            - SIDEBAR_WIDTH
            + INNER_PADDING
        )

        pygame.draw.rect(
            screen,
            SIDEBAR_COLOR,
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
            TEXT_COLOR
        )

        screen.blit(
            title,
            (panel_x, OUTER_PADDING + 12)
        )

        score = self.text_font.render(
            f"Solvability: {state.score}",
            True,
            TEXT_COLOR
        )

        screen.blit(
            score,
            (panel_x, 104)
        )

        label, color = self.get_status_text(state)

        status = self.status_font.render(
            label,
            True,
            color
        )

        screen.blit(
            status,
            (panel_x, 152)
        )

        descriptions = [
            "Drag tiles onto the board.",
            "Placed tiles remain movable.",
            "Grey regions indicate dead zones.",
            "Avoid fragmented topology."
        ]

        y = 240
        text_width = panel_width - 40

        for line in descriptions:
            y = self.draw_wrapped_text(
                screen,
                line,
                self.small_font,
                (170, 170, 190),
                panel_x,
                y,
                text_width,
                line_gap=4
            )

            y += 14