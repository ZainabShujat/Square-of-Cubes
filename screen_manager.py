class ScreenManager:

    MENU = "menu"
    MODE_SELECT = "mode_select"
    GAME = "game"
    ABOUT = "about"
    TUTORIAL = "tutorial"

    def __init__(self):

        self.current_screen = self.MENU

    def set_screen(self, screen):

        self.current_screen = screen

    def is_menu(self):

        return self.current_screen == self.MENU

    def is_mode_select(self):

        return self.current_screen == self.MODE_SELECT

    def is_game(self):

        return self.current_screen == self.GAME

    def is_about(self):

        return self.current_screen == self.ABOUT

    def is_tutorial(self):

        return self.current_screen == self.TUTORIAL