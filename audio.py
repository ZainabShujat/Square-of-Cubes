import pygame

pygame.mixer.init()

button_hover = pygame.mixer.Sound(
    "assets/sounds/button_hover.mp3"
)

button_click = pygame.mixer.Sound(
    "assets/sounds/button_click.mp3"
)

tile_pickup = pygame.mixer.Sound(
    "assets/sounds/tile_pickup.mp3"
)

tile_place = pygame.mixer.Sound(
    "assets/sounds/tile_place.mp3"
)

tile_invalid = pygame.mixer.Sound(
    "assets/sounds/tile_invalid.mp3"
)

# -----------------------------------
# VOLUMES
# -----------------------------------

button_hover.set_volume(0.08)

button_click.set_volume(0.20)

tile_pickup.set_volume(0.15)

tile_place.set_volume(0.18)

tile_invalid.set_volume(0.12)