import sys
import os
import pygame
import audio

from utils.constants import *
from utils.resource_path import resource_path

from core.board import Board
from core.state import GameState
from core.analysis import AnalysisEngine
from core.advisor import Advisor
from core.game_modes import GAME_MODES
from core.levels import LEARNING_LEVELS, get_next_learning_level
from core.player_store import PlayerStore

from core.history import HistoryManager

from core.tutorial_data import TUTORIAL_PAGES

from rendering.board_renderer import BoardRenderer
from rendering.inventory_renderer import InventoryRenderer
from rendering.ui_renderer import UIRenderer

from screen_manager import ScreenManager
from screens.about_screen import draw_about_screen
from screens.menu_screen import draw_menu

from ui.button import Button
from ui.text_block import TextBlock 


# =====================================================
# INIT
# =====================================================

pygame.init()


screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT),
    pygame.RESIZABLE
)


solved_board_bg = pygame.image.load(
    resource_path("assets/solvedboard.png")
).convert_alpha()
pygame.display.set_caption(TITLE)

audio.game_start.play()

clock = pygame.time.Clock()

menu_font = pygame.font.SysFont(
    "arial",
    38,
    bold=True
)

about_font = pygame.font.SysFont(
    "arial",
    22
)

about_small_font = pygame.font.SysFont(
    "arial",
    18
)

# =====================================================
# SYSTEMS
# =====================================================

board = Board()

state = GameState()

analysis = AnalysisEngine(board)

advisor = Advisor()

board_renderer = BoardRenderer()

inventory_renderer = InventoryRenderer()

ui_renderer = UIRenderer()

screen_manager = ScreenManager()

history = HistoryManager()

player_store = PlayerStore()


# =====================================================
# HELPERS
# =====================================================

def reset_game(initial_tile_counts=None):

    global state

    state = GameState(initial_tile_counts)


def configure_board(board_size):

    global board
    global analysis

    board = Board(board_size)
    analysis = AnalysisEngine(board)


def open_level_menu():

    global level_menu_page

    level_menu_page = 0
    screen_manager.set_screen(ScreenManager.LEVEL_SELECT)


def open_level_result():

    screen_manager.set_screen(ScreenManager.LEVEL_RESULT)


def active_player():

    return player_store.active_player()


def open_profile_select():

    screen_manager.set_screen(ScreenManager.PROFILE_SELECT)


def switch_player(player_id):

    player_store.set_active_player(player_id)
    screen_manager.set_screen(ScreenManager.MENU)


def create_local_player():

    player_store.create_player()
    screen_manager.set_screen(ScreenManager.MENU)


def clear_end_dialog_state():

    state.confirm_dialog = None
    state.game_won = False
    state.win_sound_played = False
    state.game_over = False
    state.game_over_sound_played = False


def start_game(mode, level=None):

    configure_board(level.board_size if level else BOARD_SIZE)

    reset_game(level.inventory if level else None)

    history.undo_stack.clear()
    state.game_mode = mode
    state.current_level = level
    state.current_level_index = (
        level.number - 1 if level else None
    )
    state.level_result = None
    state.return_screen = (
        ScreenManager.LEVEL_SELECT if level else ScreenManager.MODE_SELECT
    )
    screen_manager.set_screen(ScreenManager.GAME)


def begin_mode_transition(mode):

    state.mode_transition_active = True
    state.mode_transition_phase = "out"
    state.mode_transition_alpha = 0
    state.mode_transition_target = ScreenManager.GAME
    state.mode_transition_next_mode = mode


def build_mode_select_buttons():

    global mode_buttons
    global mode_back_button

    mode_buttons = []

    center_x = screen.get_width() // 2
    card_width = 560
    card_height = 132
    start_y = 198
    gap = 14

    mode_order = [
        GAME_MODES["STANDARD"],
        GAME_MODES["ENDLESS"],
        GAME_MODES["HARDCORE"],
    ]

    for index, mode in enumerate(mode_order):

        y = start_y + index * (card_height + gap)

        theme = getattr(mode, "theme", {})

        bg_color = theme.get("panel_fill", (20, 20, 54))
        hover_bg_color = theme.get("banner_fill", (36, 36, 84))
        border_color = theme.get("panel_border", (110, 120, 210))
        hover_border_color = theme.get("accent", (140, 150, 255))
        title_color = theme.get("accent", TEXT_COLOR)
        glow_color = theme.get("accent", None) if mode.name == "ENDLESS" else None
        glow_alpha = 72 if mode.name == "ENDLESS" else 0

        hover_sound = audio.gamemode_hover

        if mode.name == "STANDARD":
            click_sound = audio.standard_click
        elif mode.name == "ENDLESS":
            click_sound = audio.endless_click
        else:
            click_sound = audio.hardmode_click

        mode_buttons.append(
            Button(
                f"{mode.name} MODE",
                center_x - card_width // 2,
                y,
                card_width,
                card_height,
                callback=lambda selected_mode=mode: begin_mode_transition(selected_mode),
                font_size=20,
                hover_scale=1.015,
                bg_color=bg_color,
                hover_bg_color=hover_bg_color,
                border_color=border_color,
                hover_border_color=hover_border_color,
                text_color=title_color,
                text_offset_y=-22,
                pulse_amount=0.007,
                pulse_period=3600,
                glow_color=glow_color,
                glow_alpha=glow_alpha,
                hover_sound=hover_sound,
                click_sound=click_sound
            )
        )

    mode_back_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=lambda: screen_manager.set_screen(
            ScreenManager.MENU
        )
    )


# =====================================================
# MENU BUTTONS
# =====================================================

menu_buttons = []


# =====================================================
# GAME BUTTONS
# =====================================================

game_buttons = []

about_back_button = None

tutorial_index = 0

tutorial_menu_button = None

tutorial_prev_button = None

tutorial_next_button = None

tutorial_back_button = None

yes_button = None

no_button = None

extra_confirm_button = None

mode_buttons = []

mode_back_button = None

level_buttons = []

level_back_button = None

level_page_prev_button = None

level_page_next_button = None

level_page_levels = []

level_menu_page = 0

level_result_replay_button = None

level_result_next_button = None

level_result_menu_button = None

level_result_buttons = []

profile_buttons = []

profile_back_button = None

profile_new_button = None

# =====================================================
# BUILD MENU BUTTONS
# =====================================================

def build_menu_buttons():

    global menu_buttons

    center_x = (
        screen.get_width() // 2
        - BUTTON_WIDTH // 2
    )

    start_y = 180
    gap = 66

    menu_buttons = [

        Button(
            "PLAY",
            center_x,
            start_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.MODE_SELECT
            )
        ),

        Button(
            "LEARN / PRACTICE",
            center_x,
            start_y + gap,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=open_level_menu,
            font_size=18
        ),

        Button(
            "ABOUT",
            center_x,
            start_y + gap * 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.ABOUT
            )
        ),

        Button(
            "TUTORIAL",
            center_x,
            start_y + gap * 3,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.TUTORIAL
            )
        ),

        Button(
            "PLAYER",
            center_x,
            start_y + gap * 4,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=open_profile_select
        ),

        Button(
            "EXIT",
            center_x,
            start_y + gap * 5,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda: setattr(
            state,
            "confirm_dialog",
            "exit"
        ))
    ]


def build_level_buttons():

    global level_buttons
    global level_back_button
    global level_page_prev_button
    global level_page_next_button
    global level_page_levels
    global level_menu_page

    level_buttons = []
    level_page_levels = []

    columns = 4
    rows = 5
    per_page = columns * rows
    page_count = max(1, (len(LEARNING_LEVELS) + per_page - 1) // per_page)

    if level_menu_page >= page_count:
        level_menu_page = page_count - 1

    start_index = level_menu_page * per_page
    level_page_levels = LEARNING_LEVELS[start_index:start_index + per_page]

    button_width = 170
    button_height = 72
    gap_x = 18
    gap_y = 14
    grid_width = columns * button_width + (columns - 1) * gap_x
    start_x = (screen.get_width() - grid_width) // 2
    start_y = 112

    def shift_page(delta):

        global level_menu_page

        level_menu_page = max(0, min(page_count - 1, level_menu_page + delta))

    for index, level in enumerate(level_page_levels):

        row = index // columns
        col = index % columns

        x = start_x + col * (button_width + gap_x)
        y = start_y + row * (button_height + gap_y)

        level_buttons.append(
            Button(
                f"LEVEL {level.number}",
                x,
                y,
                button_width,
                button_height,
                callback=lambda selected_level=level: start_game(
                    None,
                    selected_level
                ),
                font_size=22,
                hover_scale=1.03,
                bg_color=(22, 22, 46),
                hover_bg_color=(40, 40, 74),
                border_color=(96, 108, 190),
                hover_border_color=(178, 186, 255),
                text_color=TEXT_COLOR,
                text_offset_y=-2,
                pulse_amount=0.004,
                pulse_period=3000
            )
        )

    level_back_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=lambda: screen_manager.set_screen(
            ScreenManager.MENU
        )
    )

    level_page_prev_button = Button(
        "<",
        screen.get_width() // 2 - 170,
        screen.get_height() - 96,
        52,
        42,
        callback=lambda: shift_page(-1),
        font_size=22,
        hover_scale=1.04
    )

    level_page_next_button = Button(
        ">",
        screen.get_width() // 2 + 118,
        screen.get_height() - 96,
        52,
        42,
        callback=lambda: shift_page(1),
        font_size=22,
        hover_scale=1.04
    )


def build_profile_buttons():

    global profile_buttons
    global profile_back_button
    global profile_new_button

    profile_buttons = []

    center_x = screen.get_width() // 2
    start_y = 180
    button_width = 300
    button_height = 58
    gap = 70

    for index, player in enumerate(player_store.players()[:6]):

        stats = player.get("stats", {})
        label = (
            f"{player.get('name', 'Player')}  "
            f"L{stats.get('best_level', 0)}  "
            f"{stats.get('total_stars', 0)} stars"
        )

        profile_buttons.append(
            Button(
                label,
                center_x - button_width // 2,
                start_y + index * gap,
                button_width,
                button_height,
                callback=lambda player_id=player["id"]: switch_player(player_id),
                font_size=18,
                hover_scale=1.03
            )
        )

    profile_new_button = Button(
        "NEW PLAYER",
        center_x - button_width // 2,
        screen.get_height() - 170,
        button_width,
        54,
        callback=create_local_player,
        font_size=20
    )

    profile_back_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=lambda: screen_manager.set_screen(
            ScreenManager.MENU
        )
    )


# =====================================================
# BUILD GAME BUTTONS
# =====================================================

def build_game_buttons():

    global game_buttons

    sidebar_x = screen.get_width() - SIDEBAR_WIDTH
    nav_x = sidebar_x + INNER_PADDING
    nav_y = 84

    undo_width = 48
    restart_width = 72
    menu_width = 48
    gap = 6

    total_width = undo_width + restart_width + menu_width + gap * 2
    start_x = nav_x + (SIDEBAR_WIDTH - INNER_PADDING * 2 - total_width) // 2

    game_buttons = [

        Button(
            "UNDO",
            start_x,
            nav_y,
            undo_width,
            SMALL_BUTTON_HEIGHT - 6,
            callback=lambda:
            history.undo(state),
            font_size=14,
            hover_scale=1.02
        ),

        Button(
            "RESTART",
            start_x + undo_width + gap,
            nav_y,
            restart_width,
            SMALL_BUTTON_HEIGHT - 6,
            callback=lambda: setattr(
            state,
            "confirm_dialog",
            "restart"
            ),
            font_size=14,
            hover_scale=1.02
        ),

        Button(
            "MENU",
            start_x + undo_width + gap + restart_width + gap,
            nav_y,
            menu_width,
            SMALL_BUTTON_HEIGHT - 6,
            callback=lambda: setattr(
                state,
                "confirm_dialog",
                "mode_menu"
            ),
            font_size=14,
            hover_scale=1.02
        )
    ]


# =====================================================
# EXIT
# =====================================================

def exit_game():

    pygame.quit()
    sys.exit()


# =====================================================
# DRAW MENU
# =====================================================


def draw_profile_select_screen(screen):

    screen.fill(BACKGROUND_COLOR)

    title = ui_renderer.title_font.render(
        "PLAYERS",
        True,
        TEXT_COLOR
    )

    title_rect = title.get_rect(
        center=(
            screen.get_width() // 2,
            80
        )
    )

    screen.blit(title, title_rect)

    subtitle = about_small_font.render(
        "Choose a local player profile for progress and game history.",
        True,
        (160, 170, 205)
    )

    subtitle_rect = subtitle.get_rect(
        center=(
            screen.get_width() // 2,
            120
        )
    )

    screen.blit(subtitle, subtitle_rect)

    active_id = player_store.data.get("active_player_id")

    for button in profile_buttons:

        button.draw(screen)

    for index, player in enumerate(player_store.players()[:6]):

        if player.get("id") != active_id:
            continue

        marker = about_small_font.render(
            "ACTIVE",
            True,
            (120, 255, 150)
        )

        screen.blit(
            marker,
            (
                screen.get_width() // 2 + 170,
                198 + index * 70
            )
        )

    profile_new_button.draw(screen)
    profile_back_button.draw(screen)


def build_about_button():

    global about_back_button

    about_back_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=lambda:
        screen_manager.set_screen(
            ScreenManager.MENU
        )
    )

def next_tutorial():

    global tutorial_index

    tutorial_index = min(
        tutorial_index + 1,
        len(TUTORIAL_PAGES) - 1
    )


def previous_tutorial():

    global tutorial_index

    tutorial_index = max(
        tutorial_index - 1,
        0
    )


def build_tutorial_buttons():

    global tutorial_menu_button
    global tutorial_prev_button
    global tutorial_next_button
    global tutorial_back_button

    tutorial_menu_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=lambda: screen_manager.set_screen(
            ScreenManager.MENU
        )
    )

    tutorial_prev_button = Button(
        "<",
        screen.get_width() - 170,
        screen.get_height() - 98,
        52,
        42,
        callback=previous_tutorial,
        font_size=22,
        hover_scale=1.04
    )

    tutorial_next_button = Button(
        ">",
        screen.get_width() - 104,
        screen.get_height() - 98,
        52,
        42,
        callback=next_tutorial,
        font_size=22,
        hover_scale=1.04
    )

    tutorial_back_button = tutorial_menu_button


def close_confirm_dialog():

    state.confirm_dialog = None


def stay_on_board():

    clear_end_dialog_state()


def confirm_dialog_yes():
    if state.confirm_dialog == "restart":
        start_game(state.game_mode, state.current_level)
        close_confirm_dialog()
    elif state.confirm_dialog in ("menu", "mode_menu"):
        screen_manager.set_screen(
            state.return_screen or ScreenManager.MODE_SELECT
        )
        close_confirm_dialog()
    elif state.confirm_dialog == "exit":
        pygame.quit()
        sys.exit()


def restart_current_mode():

    current_mode = state.game_mode
    start_game(current_mode, state.current_level)
    close_confirm_dialog()


def return_to_mode_menu():

    return_to_previous_menu()


def return_to_previous_menu():

    screen_manager.set_screen(
        state.return_screen or ScreenManager.MODE_SELECT
    )
    close_confirm_dialog()


def close_level_result():

    state.level_result = None


def return_to_level_menu():

    close_level_result()
    screen_manager.set_screen(ScreenManager.LEVEL_SELECT)


def replay_current_level():

    if state.current_level:
        start_game(state.game_mode, state.current_level)


def go_to_next_level():

    next_level = get_next_learning_level(state.current_level)

    if next_level:
        start_game(None, next_level)
    else:
        return_to_level_menu()


def level_stars_for_result(won, deadzone_count, gap_count, deadzone_limit):

    if not won:
        return 0

    if deadzone_count == 0 and gap_count == 0:
        return 3

    if deadzone_count <= max(1, deadzone_limit // 2):
        return 2

    return 1


def finalize_level_run(outcome):

    state.level_result = build_level_result_data(outcome)
    player_store.record_level_result(state.level_result)

    if outcome == "win" and not state.win_sound_played:

        audio.win.play()
        state.win_sound_played = True

    elif outcome == "lose" and not state.game_over_sound_played:

        audio.game_over.play()
        state.game_over_sound_played = True

    open_level_result()


def build_level_result_data(outcome):

    deadzone_count = state.deadzone_count
    gap_count = len(state.dead_regions)
    gap_cells = sum(len(region) for region in state.dead_regions)
    deadzone_limit = (
        state.current_level.deadzone_limit
        if state.current_level
        else state.game_mode.deadzone_limit or 0
    )
    won = outcome == "win"

    return {
        "outcome": outcome,
        "level_number": state.current_level.number if state.current_level else None,
        "board_size": board.size,
        "deadzone_limit": deadzone_limit,
        "deadzone_count": deadzone_count,
        "gap_count": gap_count,
        "gap_cells": gap_cells,
        "score": state.score,
        "moves": state.move_count,
        "stars": level_stars_for_result(
            won,
            deadzone_count,
            gap_count,
            deadzone_limit
        ),
        "max_stars": 3
    }


def return_to_main_menu():

    screen_manager.set_screen(
        ScreenManager.MENU
    )
    close_confirm_dialog()


def build_confirm_dialog_buttons():

    global yes_button
    global no_button
    global extra_confirm_button

    box_x = screen.get_width() // 2 - 260
    box_y = screen.get_height() // 2 - 120

    button_y = box_y + 150

    yes_text = "YES"
    no_text = "NO"
    extra_button = None
    yes_width = 150
    no_width = 150
    extra_width = 150
    gap = 20

    menu_label = (
        "LEVEL MENU"
        if state.return_screen == ScreenManager.LEVEL_SELECT
        else "MODE MENU"
    )

    if state.confirm_dialog == "game_over":
        yes_text = menu_label
        no_text = "RESTART"
        # center the two-button layout for game over as well
        total_width = yes_width + no_width + gap
        start_x = box_x + (520 - total_width) // 2
        yes_x = start_x
        no_x = yes_x + yes_width + gap
    elif state.confirm_dialog == "win":
        yes_text = "STAY"
        no_text = menu_label
        extra_button = Button(
            "MENU",
            0,
            button_y,
            extra_width,
            60,
            callback=return_to_main_menu
        )
        total_width = yes_width + no_width + extra_width + gap * 2
        start_x = box_x + (520 - total_width) // 2
        yes_x = start_x
        no_x = yes_x + yes_width + gap
        extra_x = no_x + no_width + gap
    else:
        total_width = yes_width + no_width + gap
        start_x = box_x + (520 - total_width) // 2
        yes_x = start_x
        no_x = yes_x + yes_width + gap

    yes_button = Button(
        yes_text,
        yes_x,
        button_y,
        yes_width,
        60,
        callback=stay_on_board if state.confirm_dialog == "win" else (return_to_mode_menu if state.confirm_dialog == "game_over" else confirm_dialog_yes)
    )

    no_button = Button(
        no_text,
        no_x,
        button_y,
        no_width,
        60,
        callback=return_to_mode_menu if state.confirm_dialog == "win" else (restart_current_mode if state.confirm_dialog == "game_over" else close_confirm_dialog)
    )

    if extra_button:
        extra_button.rect.x = extra_x

    extra_confirm_button = extra_button


def build_level_result_buttons():

    global level_result_replay_button
    global level_result_next_button
    global level_result_menu_button
    global level_result_buttons

    level_result_buttons = []

    result = state.level_result or {}
    outcome = result.get("outcome")
    next_level = get_next_learning_level(state.current_level) if state.current_level else None
    panel_y = screen.get_height() // 2 - 220
    panel_height = 440
    button_y = panel_y + panel_height - 72
    button_width = 150
    button_height = 60
    gap = 18

    if outcome == "win":

        has_next = next_level is not None
        total_width = button_width * (3 if has_next else 2) + gap * (2 if has_next else 1)
        start_x = screen.get_width() // 2 - total_width // 2

        level_result_replay_button = Button(
            "REPLAY",
            start_x,
            button_y,
            button_width,
            button_height,
            callback=replay_current_level
        )

        if has_next:
            level_result_next_button = Button(
                "NEXT LEVEL",
                start_x + button_width + gap,
                button_y,
                button_width,
                button_height,
                callback=go_to_next_level
            )

            level_result_menu_button = Button(
                "MENU",
                start_x + (button_width + gap) * 2,
                button_y,
                button_width,
                button_height,
                callback=return_to_level_menu
            )
        else:
            level_result_next_button = Button(
                "MENU",
                start_x + button_width + gap,
                button_y,
                button_width,
                button_height,
                callback=return_to_level_menu
            )

            level_result_menu_button = None

        level_result_buttons = [level_result_replay_button]

        if level_result_next_button:
            level_result_buttons.append(level_result_next_button)

        if level_result_menu_button:
            level_result_buttons.append(level_result_menu_button)

    else:

        total_width = button_width * 2 + gap
        start_x = screen.get_width() // 2 - total_width // 2

        level_result_replay_button = Button(
            "REPLAY",
            start_x,
            button_y,
            button_width,
            button_height,
            callback=replay_current_level
        )

        level_result_menu_button = Button(
            "MENU",
            start_x + button_width + gap,
            button_y,
            button_width,
            button_height,
            callback=return_to_level_menu
        )

        level_result_next_button = None

        level_result_buttons = [
            level_result_replay_button,
            level_result_menu_button
        ]


def draw_result_tile_pattern(screen, panel, is_win):

    pattern = [
        (1, panel.x + 34, panel.y + 42),
        (2, panel.x + 56, panel.y + 72),
        (3, panel.x + 92, panel.y + 38),
        (2, panel.right - 114, panel.y + 54),
        (1, panel.right - 52, panel.y + 96),
        (3, panel.right - 102, panel.bottom - 160),
        (2, panel.x + 54, panel.bottom - 152),
    ]

    alpha = 92 if is_win else 58

    for size, x, y in pattern:

        color = get_tile_color(size + (2 if is_win else 0))
        tile_size = size * 16
        tile_surface = pygame.Surface(
            (tile_size, tile_size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            tile_surface,
            (*color, alpha),
            tile_surface.get_rect(),
            border_radius=6
        )

        pygame.draw.rect(
            tile_surface,
            (*color, min(180, alpha + 56)),
            tile_surface.get_rect(),
            width=2,
            border_radius=6
        )

        screen.blit(tile_surface, (x, y))


def draw_result_star_marks(screen, panel, stars, max_stars):

    mark_width = 42
    gap = 12
    total_width = max_stars * mark_width + (max_stars - 1) * gap
    start_x = panel.centerx - total_width // 2
    y = panel.y + 116

    for index in range(max_stars):

        filled = index < stars
        rect = pygame.Rect(
            start_x + index * (mark_width + gap),
            y,
            mark_width,
            14
        )

        color = (255, 220, 120) if filled else (70, 76, 112)
        border = (255, 240, 170) if filled else (105, 112, 156)

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=7
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            width=2,
            border_radius=7
        )


def draw_result_metric_card(screen, rect, label, value, accent):

    pygame.draw.rect(
        screen,
        (18, 24, 50),
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        accent,
        rect,
        width=2,
        border_radius=12
    )

    label_surface = about_small_font.render(
        label,
        True,
        (150, 164, 205)
    )

    value_surface = about_font.render(
        value,
        True,
        TEXT_COLOR
    )

    screen.blit(
        label_surface,
        (rect.x + 14, rect.y + 10)
    )

    screen.blit(
        value_surface,
        (rect.x + 14, rect.y + 32)
    )


def draw_level_result_screen(screen):
    result = state.level_result or {}
    outcome = result.get("outcome", "lose")
    is_win = outcome == "win"

    overlay = pygame.Surface(
        (
            screen.get_width(),
            screen.get_height()
        ),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 176))
    screen.blit(overlay, (0, 0))

    panel = pygame.Rect(
        screen.get_width() // 2 - 360,
        screen.get_height() // 2 - 220,
        720,
        440
    )

    base_color = (12, 24, 44) if is_win else (36, 16, 28)
    panel_color = (14, 20, 42)
    accent = (110, 230, 255) if is_win else (255, 116, 126)
    soft_accent = (120, 255, 170) if is_win else (255, 176, 120)

    glow = pygame.Surface(
        (
            panel.width + 46,
            panel.height + 46
        ),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        glow,
        (*accent, 46),
        glow.get_rect(),
        border_radius=28
    )

    screen.blit(
        glow,
        (
            panel.x - 23,
            panel.y - 23
        )
    )

    pygame.draw.rect(
        screen,
        base_color,
        panel,
        border_radius=24
    )

    inner_panel = panel.inflate(-24, -24)

    pygame.draw.rect(
        screen,
        panel_color,
        inner_panel,
        border_radius=18
    )

    draw_result_tile_pattern(screen, inner_panel, is_win)

    pygame.draw.rect(
        screen,
        accent,
        panel,
        width=2,
        border_radius=24
    )

    level_surface = about_small_font.render(
        f"LEVEL {result.get('level_number', '?')}",
        True,
        soft_accent
    )

    screen.blit(
        level_surface,
        (
            panel.centerx - level_surface.get_width() // 2,
            panel.y + 34
        )
    )

    title = menu_font.render(
        "BOARD SEALED" if is_win else "TOPOLOGY BROKE",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (
            panel.centerx - title.get_width() // 2,
            panel.y + 58
        )
    )

    stars = result.get("stars", 0)
    max_stars = result.get("max_stars", 3)

    subtitle_text = (
        "Clean fill, low fragmentation, progress saved."
        if is_win
        else "Dead zones exceeded the level allowance."
    )

    star_text = about_font.render(
        subtitle_text,
        True,
        (255, 220, 120)
    )

    screen.blit(
        star_text,
        (
            panel.centerx - star_text.get_width() // 2,
            panel.y + 54
        )
    )

    metrics = [
        f"Level {result.get('level_number', '?')}  |  {result.get('board_size', '?')}x{result.get('board_size', '?')} board",
        f"Dead zones: {result.get('deadzone_count', 0)} / {result.get('deadzone_limit', 0)}",
        f"Gaps: {result.get('gap_count', 0)} regions, {result.get('gap_cells', 0)} cells",
        f"No. of moves: {result.get('moves', 0)}",
        f"Solvability score: {result.get('score', 0)}",
    ]

    start_y = panel.y + 102

    for index, line in enumerate(metrics):

        line_surface = about_font.render(
            line,
            True,
            (220, 225, 240)
        )

        screen.blit(
            line_surface,
            (
                panel.centerx - line_surface.get_width() // 2,
                start_y + index * 28
            )
        )

    for button in level_result_buttons:
        button.draw(screen)

def load_tutorial_image(path):

    if not path:
        return None

    resolved_path = resource_path(path)

    if not os.path.exists(resolved_path):
        return None

    image = pygame.image.load(resolved_path)

    return image.convert_alpha()    

def draw_confirm_dialog(screen):

    overlay = pygame.Surface(
        (
            screen.get_width(),
            screen.get_height()
        ),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    box = pygame.Rect(
        screen.get_width() // 2 - 260,
        screen.get_height() // 2 - 120,
        520,
        240
    )

    pygame.draw.rect(
        screen,
        (20, 20, 45),
        box,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        (100, 120, 255),
        box,
        width=2,
        border_radius=20
    )
    if state.confirm_dialog == "restart":

        text = "Restart the board?"

    elif state.confirm_dialog == "win":

        text = "You Win!"

    elif state.confirm_dialog == "game_over":

        text = "Game Over"

    elif state.confirm_dialog == "mode_menu":

        text = (
            "Return to level menu?"
            if state.return_screen == ScreenManager.LEVEL_SELECT
            else "Return to mode menu?"
        )

    elif state.confirm_dialog == "menu":

        text = (
            "Return to level menu?"
            if state.return_screen == ScreenManager.LEVEL_SELECT
            else "Return to mode menu?"
        )

    else:

        text = "Exit the game?"

    surface = menu_font.render(
        text,
        True,
        TEXT_COLOR
    )

    screen.blit(
        surface,
        (
            box.centerx - surface.get_width() // 2,
            box.y + 50
        )
    )
    yes_button.draw(screen)
    no_button.draw(screen)
    if state.confirm_dialog == "win" and extra_confirm_button:
        extra_confirm_button.draw(screen)
        
# =====================================================
# MAIN LOOP
# =====================================================

running = True

while running:

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    build_menu_buttons()

    build_game_buttons()

    build_mode_select_buttons()

    build_level_buttons()

    build_profile_buttons()

    build_about_button()

    build_tutorial_buttons()

    build_confirm_dialog_buttons()

    build_level_result_buttons()

    # =================================================
    # EVENTS
    # =================================================

    for event in pygame.event.get():

        # -------------------------------------------------
        # QUIT
        # -------------------------------------------------

        if event.type == pygame.QUIT:

            if state.confirm_dialog == "exit":

                pygame.quit()
                sys.exit()

            state.confirm_dialog = "exit"

            continue

        # -------------------------------------------------
        # WINDOW RESIZE
        # -------------------------------------------------

        elif event.type == pygame.VIDEORESIZE:

            MIN_WIDTH = 1200
            MIN_HEIGHT = 800

            new_width = max(
                MIN_WIDTH,
                event.w
            )

            new_height = max(
                MIN_HEIGHT,
                event.h
            )

        # -------------------------------------------------
        # CONFIRM DIALOG
        # -------------------------------------------------

        elif state.confirm_dialog:

            yes_button.handle_event(event)

            no_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    close_confirm_dialog()

            continue

        # -------------------------------------------------
        # MODE TRANSITION LOCK
        # -------------------------------------------------

        elif state.mode_transition_active:

            continue

        # -------------------------------------------------
        # MENU EVENTS
        # -------------------------------------------------

        if screen_manager.is_menu():

            for button in menu_buttons:

                button.handle_event(event)

        # -------------------------------------------------
        # PROFILE SELECT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_profile_select():

            for button in profile_buttons:

                button.handle_event(event)

            profile_new_button.handle_event(event)

            profile_back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

        # -------------------------------------------------
        # ABOUT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_about():

            about_back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    state.confirm_dialog = "menu"

        # -------------------------------------------------
        # TUTORIAL SCREEN
        # -------------------------------------------------

        elif screen_manager.is_tutorial():

            tutorial_menu_button.handle_event(event)

            tutorial_prev_button.handle_event(event)

            tutorial_next_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

        # -------------------------------------------------
        # MODE SELECT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_mode_select():

            for button in mode_buttons:

                button.handle_event(event)

            mode_back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

        # -------------------------------------------------
        # LEVEL SELECT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_level_select():

            for button in level_buttons:

                button.handle_event(event)

            level_page_prev_button.handle_event(event)

            level_page_next_button.handle_event(event)

            level_back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

        # -------------------------------------------------
        # LEVEL RESULT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_level_result():

            for button in level_result_buttons:

                button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    return_to_level_menu()

        # -------------------------------------------------
        # GAME EVENTS
        # -------------------------------------------------

        elif screen_manager.is_game():

            for button in game_buttons:

                button.handle_event(event)

            # =============================================
            # ESC TO MENU
            # =============================================

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

            # =============================================
            # MOUSE DOWN
            # =============================================

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    clicked_inventory = (
                        inventory_renderer.handle_click(
                            state,
                            mouse_x,
                            mouse_y,
                            screen_width,
                            screen_height
                        )
                    )

                    if not clicked_inventory:

                        grid_x, grid_y = (
                            board_renderer.screen_to_grid(
                                screen,
                                mouse_x,
                                mouse_y,
                                screen_width,
                                screen_height,
                                board.size
                            )
                        )

                        piece = state.get_piece_at(
                            grid_x,
                            grid_y
                        )

                        if piece:

                            state.remove_piece(piece)

                            state.return_tile(
                                piece.size
                            )

                            state.dragging_piece = piece

                            state.selected_size = (
                                piece.size
                            )

            # =============================================
            # MOUSE UP
            # =============================================

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:

                    if state.dragging_piece:

                        piece = state.dragging_piece

                        state.move_count += 1

                        grid_x, grid_y = (
                            board_renderer.screen_to_grid(
                                screen,
                                mouse_x,
                                mouse_y,
                                screen_width,
                                screen_height,
                                board.size
                            )
                        )

                        valid = board.can_place(
                            state,
                            piece.size,
                            grid_x,
                            grid_y
                        )

                        if valid:
                            history.save_state(state)

                            piece.grid_x = grid_x
                            piece.grid_y = grid_y

                            state.add_piece(piece)

                            state.take_tile(piece.size)

                            audio.tile_place.play()

                            state.add_tile_animation(
                                "place",
                                piece=piece,
                                grid_x=grid_x,
                                grid_y=grid_y,
                                start_time=pygame.time.get_ticks(),
                                duration=180
                            )

                        else:
                            audio.tile_invalid.play()

                            state.add_tile_animation(
                                "invalid",
                                piece=piece,
                                grid_x=grid_x,
                                grid_y=grid_y,
                                start_time=pygame.time.get_ticks(),
                                duration=160
                            )

                        state.dragging_piece = None

            # =============================================
            # MOUSE MOVE
            # =============================================

            elif event.type == pygame.MOUSEMOTION:

                if state.dragging_piece:

                    grid_x, grid_y = (
                        board_renderer.screen_to_grid(
                            screen,
                            mouse_x,
                            mouse_y,
                            screen_width,
                            screen_height,
                            board.size
                        )
                    )

                    state.preview_x = grid_x
                    state.preview_y = grid_y

                    state.preview_valid = (
                        board.can_place(
                            state,
                            state.dragging_piece.size,
                            grid_x,
                            grid_y
                        )
                    )

    # =====================================================
    # UPDATE
    # =====================================================

    if screen_manager.is_game():

        analysis.update(state)

        if state.current_level:

            if state.game_won and not state.level_result:

                finalize_level_run("win")

            elif state.game_over and not state.level_result:

                finalize_level_run("lose")

        elif state.game_won and not state.confirm_dialog:

            if not state.win_sound_played:

                audio.win.play()
                state.win_sound_played = True

            state.confirm_dialog = "win"

        elif state.game_over and not state.confirm_dialog:

            if not state.game_over_sound_played:

                audio.game_over.play()
                state.game_over_sound_played = True

            state.confirm_dialog = "game_over"

        current_time = pygame.time.get_ticks()

        if state.alert_kind == "deadzone":

            elapsed = current_time - state.alert_message_time

            if elapsed >= state.alert_message_duration:

                state.alert_kind = ""

        # update advisor message after analysis unless a fresh deadzone alert is active
        try:
            new_msg = advisor.evaluate(state)
        except Exception:
            new_msg = ""

        if (
            state.alert_kind != "deadzone"
            and new_msg
            and new_msg != state.alert_message
        ):
            state.alert_message = new_msg
            state.alert_message_time = current_time
            state.alert_kind = "advisor"

    if state.mode_transition_active:

        transition_step = 18

        if state.mode_transition_phase == "out":

            state.mode_transition_alpha = min(
                255,
                state.mode_transition_alpha + transition_step
            )

            if state.mode_transition_alpha >= 255:

                next_mode = state.mode_transition_next_mode

                start_game(next_mode)

                state.mode_transition_active = True
                state.mode_transition_phase = "in"
                state.mode_transition_alpha = 255
                state.mode_transition_target = ScreenManager.GAME
                state.mode_transition_next_mode = next_mode

        elif state.mode_transition_phase == "in":

            state.mode_transition_alpha = max(
                0,
                state.mode_transition_alpha - transition_step
            )

            if state.mode_transition_alpha <= 0:

                state.mode_transition_alpha = 0
                state.mode_transition_active = False
                state.mode_transition_phase = ""
                state.mode_transition_target = None
                state.mode_transition_next_mode = None

    # =====================================================
    # DRAW
    # =====================================================

    if screen_manager.is_menu():

        bg = pygame.transform.smoothscale(
            solved_board_bg,
            (
                screen.get_width(),
                screen.get_height()
            )
        )

        screen.blit(bg, (0, 0))

        overlay = pygame.Surface(
            (
                screen.get_width(),
                screen.get_height()
            ),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 25, 140))

        screen.blit(overlay, (0, 0))

        draw_menu(
    screen,
    menu_font,
    about_small_font,
    active_player,
    menu_buttons
)

    elif screen_manager.is_profile_select():

        draw_profile_select_screen(screen)

    elif screen_manager.is_about():

        draw_about_screen(
            screen,
            ui_renderer,
            about_font,
            about_back_button
        )

    elif screen_manager.is_tutorial():

        screen.fill(BACKGROUND_COLOR)

        page = TUTORIAL_PAGES[
            tutorial_index
        ]

        title = ui_renderer.title_font.render(
            page["title"],
            True,
            TEXT_COLOR
        )

        screen.blit(
            title,
            (80, 60)
        )

        image_y = 160

        # =================================================
        # SINGLE IMAGE
        # =================================================

        if "image" in page and page["image"]:

            image = load_tutorial_image(
                page["image"]
            )

            if image:

                max_width = 520
                max_height = 320

                scale = min(
                    max_width / image.get_width(),
                    max_height / image.get_height()
                )

                width = int(
                    image.get_width() * scale
                )

                height = int(
                    image.get_height() * scale
                )

                image = pygame.transform.smoothscale(
                    image,
                    (width, height)
                )

                screen.blit(
                    image,
                    (80, image_y)
                )

        # =================================================
        # DOUBLE IMAGE
        # =================================================

        elif (
            "image_left" in page
            and
            "image_right" in page
        ):

            left = load_tutorial_image(
                page["image_left"]
            )

            right = load_tutorial_image(
                page["image_right"]
            )

            if left and right:

                max_width = 260
                max_height = 260

                def scale_image(img):

                    scale = min(
                        max_width / img.get_width(),
                        max_height / img.get_height()
                    )

                    w = int(
                        img.get_width() * scale
                    )

                    h = int(
                        img.get_height() * scale
                    )

                    return pygame.transform.smoothscale(
                        img,
                        (w, h)
                    )

                left = scale_image(left)

                right = scale_image(right)

                left_x = 80

                right_x = 420

                screen.blit(
                    left,
                    (left_x, image_y)
                )

                screen.blit(
                    right,
                    (right_x, image_y)
                )

                arrow = menu_font.render(
                    "→",
                    True,
                    (180, 180, 255)
                )

                screen.blit(
                    arrow,
                    (350, 260)
                )

        # =================================================
        # IMAGE GRID
        # =================================================

        elif "images" in page and page["images"]:

            grid_images = [
                load_tutorial_image(path)
                for path in page["images"]
            ]

            grid_images = [
                image for image in grid_images if image
            ]

            if grid_images:

                left_x = 80
                top_y = image_y
                cell_max_width = 180
                cell_max_height = 150
                gap_x = 16
                gap_y = 16

                positions = [
                    (left_x, top_y),
                    (left_x + cell_max_width + gap_x, top_y),
                    (left_x, top_y + cell_max_height + gap_y),
                    (left_x + cell_max_width + gap_x, top_y + cell_max_height + gap_y)
                ]

                for image, (x_pos, y_pos) in zip(grid_images, positions):

                    scale = min(
                        cell_max_width / image.get_width(),
                        cell_max_height / image.get_height()
                    )

                    width = int(
                        image.get_width() * scale
                    )

                    height = int(
                        image.get_height() * scale
                    )

                    image = pygame.transform.smoothscale(
                        image,
                        (width, height)
                    )

                    image_rect = image.get_rect()
                    image_rect.center = (
                        x_pos + cell_max_width // 2,
                        y_pos + cell_max_height // 2
                    )

                    screen.blit(
                        image,
                        image_rect
                    )

        # =================================================
        # BODY TEXT
        # =================================================

        if (
            "image_left" in page
            and "image_right" in page
        ):

            text_x = 740

        elif "images" in page and page["images"]:

            text_x = 620

        else:

            text_x = 620

        block = TextBlock(
            about_font,
            (220, 220, 235),
            260,
            line_gap=12
        )

        block.draw(
            screen,
            page["body"],
            text_x,
            220
        )

        counter = about_small_font.render(
            f"{tutorial_index + 1} / {len(TUTORIAL_PAGES)}",
            True,
            (120, 120, 160)
        )

        screen.blit(
            counter,
            (80, screen.get_height() - 160)
        )

        controls = about_small_font.render(
            "Use the buttons below to move through the tutorial.",
            True,
            (120, 120, 160)
        )

        screen.blit(
            controls,
            (80, screen.get_height() - 130)
        )

        if page.get("footer_source"):

            footer_source = about_small_font.render(
                page["footer_source"],
                True,
                (150, 180, 255)
            )

            footer_source_rect = footer_source.get_rect(
                center=(
                    screen.get_width() // 2,
                    screen.get_height() - 58
                )
            )

            screen.blit(
                footer_source,
                footer_source_rect
            )

        if page.get("footer_note"):

            footer_note = about_small_font.render(
                page["footer_note"],
                True,
                (120, 120, 160)
            )

            footer_note_rect = footer_note.get_rect(
                center=(
                    screen.get_width() // 2,
                    screen.get_height() - 34
                )
            )

            screen.blit(
                footer_note,
                footer_note_rect
            )

        tutorial_menu_button.draw(screen)

        tutorial_prev_button.draw(screen)

        tutorial_next_button.draw(screen)

    elif screen_manager.is_mode_select():

        mode_order = [
            GAME_MODES["STANDARD"],
            GAME_MODES["ENDLESS"],
            GAME_MODES["HARDCORE"],
        ]

        hovered_theme = mode_order[0].theme

        for index, button in enumerate(mode_buttons):
            if button.is_hovered():
                hovered_theme = mode_order[index].theme
                break

        screen.fill(hovered_theme.get("screen_tint", BACKGROUND_COLOR))

        tint = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA
        )

        tint.fill(
            (*hovered_theme.get("screen_tint", (8, 8, 24)), 70)
        )
        screen.blit(tint, (0, 0))

        title = ui_renderer.title_font.render(
            "SELECT MODE",
            True,
            hovered_theme.get("accent", TEXT_COLOR)
        )

        subtitle = about_small_font.render(
            "Choose the rules for this run.",
            True,
            hovered_theme.get("accent_soft", (160, 170, 200))
        )

        screen.blit(
            title,
            (
                screen.get_width() // 2 - title.get_width() // 2,
                104
            )
        )

        screen.blit(
            subtitle,
            (
                screen.get_width() // 2 - subtitle.get_width() // 2,
                152
            )
        )

        for index, button in enumerate(mode_buttons):

            mode = mode_order[index]
            button.draw(screen)

            desc = about_small_font.render(
                mode.description,
                True,
                mode.theme.get("accent_soft", (165, 170, 200))
            )

            desc_x = button.rect.centerx - desc.get_width() // 2
            desc_y = button.rect.y + 68

            screen.blit(
                desc,
                (
                    desc_x,
                    desc_y
                )
            )

        mode_back_button.draw(screen)

    elif screen_manager.is_level_select():

        screen.fill((12, 18, 30))

        tint = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA
        )

        tint.fill((24, 28, 48, 80))
        screen.blit(tint, (0, 0))

        title = ui_renderer.title_font.render(
            "SELECT LEVEL",
            True,
            (210, 225, 255)
        )

        subtitle = about_small_font.render(
            "Select a practice level.",
            True,
            (170, 180, 210)
        )

        screen.blit(
            title,
            (
                screen.get_width() // 2 - title.get_width() // 2,
                48
            )
        )

        screen.blit(
            subtitle,
            (
                screen.get_width() // 2 - subtitle.get_width() // 2,
                76
            )
        )

        for index, button in enumerate(level_buttons):

            button.draw(screen)

        page_count = max(1, (len(LEARNING_LEVELS) + 19) // 20)

        page_label = about_small_font.render(
            f"Page {level_menu_page + 1} / {page_count}",
            True,
            (150, 160, 190)
        )

        screen.blit(
            page_label,
            (
                screen.get_width() // 2 - page_label.get_width() // 2,
                screen.get_height() - 90
            )
        )

        level_page_prev_button.draw(screen)

        level_page_next_button.draw(screen)

        level_back_button.draw(screen)

    elif screen_manager.is_level_result():

        draw_level_result_screen(screen)

    elif screen_manager.is_game():

        game_theme = getattr(state.game_mode, "theme", {})

        screen.fill(
            game_theme.get("screen_tint", BACKGROUND_COLOR)
        )

        overlay_alpha = game_theme.get("overlay_alpha", 24)

        tint = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA
        )
        tint.fill((*game_theme.get("screen_tint", (8, 8, 24)), overlay_alpha))
        screen.blit(tint, (0, 0))

        board_renderer.draw(
            screen,
            state,
            board,
            mouse_x,
            mouse_y,
            screen_width,
            screen_height
        )

        inventory_renderer.draw(
            screen,
            state,
            screen_width,
            screen_height
        )

        # compute board rect and pass to ui renderer so advisor tip can be drawn near board
        board_rect = board_renderer.get_board_rect(
            screen_width,
            screen_height,
            board.size
        )

        ui_renderer.draw(
            screen,
            state,
            screen_width,
            screen_height,
            board_rect
        )

        for button in game_buttons:

            button.draw(screen)

    if state.mode_transition_active:

        fade = pygame.Surface(
            (screen_width, screen_height),
            pygame.SRCALPHA
        )

        fade.fill((0, 0, 0, state.mode_transition_alpha))
        screen.blit(fade, (0, 0))
        
    if state.confirm_dialog:

        draw_confirm_dialog(screen)

    pygame.display.flip()

    clock.tick(FPS)
