import pygame
from utils.resource_path import resource_path

pygame.mixer.init()

button_hover = pygame.mixer.Sound(
    resource_path("assets/sounds/button_hover.mp3")
)

button_click = pygame.mixer.Sound(
    resource_path("assets/sounds/button_click.mp3")
)

gamemode_hover = pygame.mixer.Sound(
    resource_path("assets/sounds/gamemode_hover.mp3")
)

standard_click = pygame.mixer.Sound(
    resource_path("assets/sounds/standard_click.mp3")
)

endless_click = pygame.mixer.Sound(
    resource_path("assets/sounds/endless_click.mp3")
)

hardmode_click = pygame.mixer.Sound(
    resource_path("assets/sounds/hardmode_click.mp3")
)

game_start = pygame.mixer.Sound(
    resource_path("assets/sounds/game_start.mp3")
)

game_over = pygame.mixer.Sound(
    resource_path("assets/sounds/game_over.mp3")
)

win = pygame.mixer.Sound(
    resource_path("assets/sounds/win.mp3")
)

tile_pickup = pygame.mixer.Sound(
    resource_path("assets/sounds/tile_pickup.mp3")
)

tile_place = pygame.mixer.Sound(
    resource_path("assets/sounds/tile_place.mp3")
)

tile_invalid = pygame.mixer.Sound(
    resource_path("assets/sounds/tile_invalid.mp3")
)

# -----------------------------------
# VOLUMES
# -----------------------------------

button_hover.set_volume(0.12)

button_click.set_volume(0.20)

gamemode_hover.set_volume(0.13)

standard_click.set_volume(0.20)

endless_click.set_volume(0.20)

hardmode_click.set_volume(0.23)

game_start.set_volume(0.22)

game_over.set_volume(0.23)

win.set_volume(0.24)

tile_pickup.set_volume(0.20)

tile_place.set_volume(0.20)

tile_invalid.set_volume(0.20)