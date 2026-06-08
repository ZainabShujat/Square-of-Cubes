# screens/menu_screen.py

from utils.constants import TEXT_COLOR


def draw_menu(
    screen,
    menu_font,
    about_small_font,
    active_player,
    menu_buttons
):

    title = menu_font.render(
        "SUM OF CUBES",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            screen.get_width() // 2,
            140
        )
    )

    screen.blit(title, title_rect)

    player = active_player()

    if player:

        stats = player.get("stats", {})

        profile_text = about_small_font.render(
            (
                f"Player: {player.get('name', 'Player')}  "
                f"Best level {stats.get('best_level', 0)}  "
                f"{stats.get('total_stars', 0)} stars"
            ),
            True,
            (170, 190, 235)
        )

        profile_rect = profile_text.get_rect(
            center=(
                screen.get_width() // 2,
                176
            )
        )

        screen.blit(
            profile_text,
            profile_rect
        )

    for button in menu_buttons:

        button.draw(screen)