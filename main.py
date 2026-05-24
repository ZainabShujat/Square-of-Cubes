import sys
import os
import pygame
import audio

from utils.constants import *

from core.board import Board
from core.state import GameState
from core.analysis import AnalysisEngine

from core.history import HistoryManager

from core.tutorial_data import TUTORIAL_PAGES

from rendering.board_renderer import BoardRenderer
from rendering.inventory_renderer import InventoryRenderer
from rendering.ui_renderer import UIRenderer

from screen_manager import ScreenManager

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
    "assets/solvedboard.png"
).convert_alpha()
pygame.display.set_caption(TITLE)

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

board_renderer = BoardRenderer()

inventory_renderer = InventoryRenderer()

ui_renderer = UIRenderer()

screen_manager = ScreenManager()

history = HistoryManager()


# =====================================================
# HELPERS
# =====================================================

def reset_game():

    global state

    state = GameState()


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

tutorial_next_button = None

tutorial_back_button = None

yes_button = None

no_button = None

# =====================================================
# BUILD MENU BUTTONS
# =====================================================

def build_menu_buttons():

    global menu_buttons

    center_x = (
        screen.get_width() // 2
        - BUTTON_WIDTH // 2
    )

    start_y = 240

    menu_buttons = [

        Button(
            "PLAY",
            center_x,
            start_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.GAME
            )
        ),

        Button(
            "ABOUT",
            center_x,
            start_y + 90,
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
            start_y + 180,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.TUTORIAL
            )
        ),

        Button(
            "EXIT",
            center_x,
            start_y + 270,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            callback=lambda: setattr(
            state,
            "confirm_dialog",
            "exit"
        ))
    ]


# =====================================================
# BUILD GAME BUTTONS
# =====================================================

def build_game_buttons():

    global game_buttons

    right_x = (
        screen.get_width()
        - SIDEBAR_WIDTH
        + 30
    )

    top_y = screen.get_height() - 190

    game_buttons = [

        Button(
            "UNDO",
            right_x,
            top_y,
            SMALL_BUTTON_WIDTH,
            SMALL_BUTTON_HEIGHT,
            callback=lambda:
            history.undo(state)
        ),

        Button(
            "RESTART",
            right_x,
            top_y + 60,
            SMALL_BUTTON_WIDTH,
            SMALL_BUTTON_HEIGHT,
            callback=lambda: setattr(
            state,
            "confirm_dialog",
            "restart"
            )
        ),

        Button(
            "MENU",
            right_x,
            top_y + 120,
            SMALL_BUTTON_WIDTH,
            SMALL_BUTTON_HEIGHT,
            callback=lambda:
            screen_manager.set_screen(
                ScreenManager.MENU
            )
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

def draw_menu(screen):

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

    for button in menu_buttons:

        button.draw(screen)

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

    global tutorial_next_button
    global tutorial_back_button

    tutorial_back_button = Button(
        "BACK",
        80,
        screen.get_height() - 100,
        140,
        50,
        callback=previous_tutorial
    )

    tutorial_next_button = Button(
        "NEXT",
        screen.get_width() - 220,
        screen.get_height() - 100,
        140,
        50,
        callback=next_tutorial
    )


def close_confirm_dialog():

    state.confirm_dialog = None


def confirm_dialog_yes():

    if state.confirm_dialog == "restart":
        reset_game()
    elif state.confirm_dialog == "exit":
        pygame.quit()
        sys.exit()


def build_confirm_dialog_buttons():

    global yes_button
    global no_button

    box_x = screen.get_width() // 2 - 220
    box_y = screen.get_height() // 2 - 120

    button_y = box_y + 150

    yes_button = Button(
        "YES",
        box_x + 70,
        button_y,
        140,
        60,
        callback=confirm_dialog_yes
    )

    no_button = Button(
        "NO",
        box_x + 230,
        button_y,
        140,
        60,
        callback=close_confirm_dialog
    )

def load_tutorial_image(path):

    if not path:
        return None

    if not os.path.exists(path):
        return None

    image = pygame.image.load(path)

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
        screen.get_width() // 2 - 220,
        screen.get_height() // 2 - 120,
        440,
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

    build_about_button()

    build_tutorial_buttons()

    build_confirm_dialog_buttons()

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
        # MENU EVENTS
        # -------------------------------------------------

        if screen_manager.is_menu():

            for button in menu_buttons:

                button.handle_event(event)

        # -------------------------------------------------
        # ABOUT SCREEN
        # -------------------------------------------------

        elif screen_manager.is_about():

            about_back_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

        # -------------------------------------------------
        # TUTORIAL SCREEN
        # -------------------------------------------------

        elif screen_manager.is_tutorial():

            tutorial_back_button.handle_event(event)

            tutorial_next_button.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    screen_manager.set_screen(
                        ScreenManager.MENU
                    )

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
                                screen_height
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

                        grid_x, grid_y = (
                            board_renderer.screen_to_grid(
                                screen,
                                mouse_x,
                                mouse_y,
                                screen_width,
                                screen_height
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
                            screen_height
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

        draw_menu(screen)

    elif screen_manager.is_about():
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

        controls = about_small_font.render(
            "ESC to return to menu",
            True,
            (120, 120, 160)
        )

        screen.blit(
            controls,
            (80, screen.get_height() - 140)
        )

        about_back_button.draw(screen)

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
        # BODY TEXT
        # =================================================

        if (
            "image_left" in page
            and "image_right" in page
        ):

            text_x = 740

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
            "ESC to return to menu",
            True,
            (120, 120, 160)
        )

        screen.blit(
            controls,
            (80, screen.get_height() - 130)
        )

        tutorial_back_button.draw(screen)

        tutorial_next_button.draw(screen)

    elif screen_manager.is_game():

        screen.fill(BACKGROUND_COLOR)

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

        ui_renderer.draw(
            screen,
            state,
            screen_width,
            screen_height
        )

        for button in game_buttons:

            button.draw(screen)
        
    if state.confirm_dialog:

        draw_confirm_dialog(screen)

    pygame.display.flip()

    clock.tick(FPS)