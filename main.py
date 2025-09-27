import pygame
from pygame.math import Vector2
import sys

from core.snake import Snake


class App(object):
    def __init__(self) -> None:
        _, nerr = pygame.init()
        assert (
            nerr == 0
        ), f"Encountered {nerr} errors while initialising pygame, exiting."

        self.settings = {
            "default_screensize": (720, 480),
            "framerate": 60,
            "blocksize": 16,
        }
        self.inputs = {"direction": "right"}

        self.screen = pygame.display.set_mode(self.settings["default_screensize"])

        self.clock = pygame.Clock()
        self.dt = 0

        self.player = Snake(Vector2(5, 5))
        self.player.speed = 8

        self.running = True

        self.update()

    def update(self):
        while self.running:
            self.handle_events()

            self.player.update(self)

            self.screen.fill((0, 0, 0))
            self.player.blit(self)
            pygame.display.flip()
            self.dt = self.clock.tick(self.settings["framerate"])

        sys.exit(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.player.facing != "left":
                    self.inputs["direction"] = "right"
                if event.key == pygame.K_LEFT and self.player.facing != "right":
                    self.inputs["direction"] = "left"
                if event.key == pygame.K_UP and self.player.facing != "down":
                    self.inputs["direction"] = "up"
                if event.key == pygame.K_DOWN and self.player.facing != "up":
                    self.inputs["direction"] = "down"


if __name__ == "__main__":
    App()
