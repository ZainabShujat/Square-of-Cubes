import pygame
from utils.resource_path import resource_path

pygame.mixer.init()

button_hover = pygame.mixer.Sound(
    resource_path("assets/sounds/button_hover.mp3")
)

button_click = pygame.mixer.Sound(
    resource_path("assets/sounds/button_click.mp3")
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

tile_pickup.set_volume(0.19)

tile_place.set_volume(0.18)

tile_invalid.set_volume(0.12)