import pygame


class TextBlock:

    def __init__(
        self,
        font,
        color,
        max_width,
        line_gap=8
    ):

        self.font = font

        self.color = color

        self.max_width = max_width

        self.line_gap = line_gap

    # =====================================================
    # WRAP
    # =====================================================

    def wrap_text(self, text):

        words = text.split()

        lines = []

        current_line = ""

        for word in words:

            test = (
                word
                if not current_line
                else f"{current_line} {word}"
            )

            if self.font.size(test)[0] <= self.max_width:

                current_line = test

            else:

                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:

            lines.append(current_line)

        return lines

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen,
        text,
        x,
        y
    ):

        lines = self.wrap_text(text)

        current_y = y

        for line in lines:

            surface = self.font.render(
                line,
                True,
                self.color
            )

            screen.blit(
                surface,
                (x, current_y)
            )

            current_y += (
                self.font.get_height()
                + self.line_gap
            )

        return current_y