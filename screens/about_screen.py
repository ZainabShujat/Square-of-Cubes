# screens/about_screen.py

import pygame

from utils.constants import *
from ui.text_block import TextBlock


def draw_about_screen(
    screen,
    ui_renderer,
    about_font,
    about_back_button
):

    screen.fill(BACKGROUND_COLOR)

    title = ui_renderer.title_font.render(
        "ABOUT",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (80, 60)
    )

    formula = about_font.render(
        "1³ + 2³ + 3³ + ... + 9³ = 45² = 2025",
        True,
        (140, 180, 255)
    )

    screen.blit(
        formula,
        (80, 130)
    )

    block = TextBlock(
        about_font,
        (210, 210, 230),
        900,
        line_gap=10
    )

    y = 210

    paragraphs = [

        (
            "Sum of Cubes is a topology-based "
            "spatial puzzle game built around "
            "the mathematical identity above."
        ),

        (
            "The total area of all square tiles "
            "perfectly fills a 45×45 board."
        ),

        (
            "The challenge is not merely filling "
            "space, but preserving long-term "
            "solvability and avoiding fragmented "
            "regions."
        ),

        (
            "Placed tiles remain movable, allowing "
            "the board topology to evolve dynamically "
            "throughout play."
        ),

        (
            "This project explores geometry, "
            "fragmentation, recoverability, and "
            "spatial reasoning."
        )
    ]

    for paragraph in paragraphs:

        y = block.draw(
            screen,
            paragraph,
            80,
            y
        )

        y += 26

    about_back_button.draw(screen)