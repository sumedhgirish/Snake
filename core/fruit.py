import pygame
from pygame.math import Vector2
from pathlib import Path
import random

FRUIT_SPRITESHEET = Path("./assets/items/food.png")
SPRITESIZE = 128


class Fruit(object):

    def __init__(self, x_bounds, y_bounds, size) -> None:
        self.get_new_position = lambda: Vector2(
            random.randint(0, x_bounds - 1), random.randint(0, y_bounds - 1)
        )
        self.position = self.get_new_position()

        self.spritesheet = pygame.image.load(FRUIT_SPRITESHEET).convert_alpha()
        self.sprite_pos = Vector2(0, 0)
        self.sprite = pygame.transform.scale(
            self.spritesheet.subsurface(
                pygame.Rect(self.sprite_pos * SPRITESIZE, (SPRITESIZE, SPRITESIZE)),
            ),
            size,
        )

    def blit(self, runtime):
        runtime.screen.blit(self.sprite, self.position * runtime.settings["blocksize"])
