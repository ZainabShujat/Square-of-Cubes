import pygame
from settings import CELL_SIZE
from settings import OFFSET_X
from settings import OFFSET_Y


class SquarePiece:

    def __init__(self, x, y, size, color):

        self.x = x
        self.y = y

        self.size = size
        self.color = color

    def draw(self, screen):

        rect = pygame.Rect(
            OFFSET_X + self.x * CELL_SIZE,
            OFFSET_Y + self.y * CELL_SIZE,
            CELL_SIZE * self.size,
            CELL_SIZE * self.size
        )

        pygame.draw.rect(
            screen,
            self.color,
            rect
        )