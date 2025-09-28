from pathlib import Path
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
            "blocksize": 30,
            "current_working_directory": ".",
        }
        self.inputs = {"direction": "right"}

        self.screen = pygame.display.set_mode(self.settings["default_screensize"])

        self.clock = pygame.Clock()
        self.dt = 0

        self.player = Snake(Vector2(5, 5))
        self.player.speed = 8

        self.running = True

        self.cwd = Path(self.settings["current_working_directory"])

        self._init_screen()
        self.update()

    def _init_screen(self):
        self.background = pygame.image.load(
            self.cwd / "assets" / "general" / "background.png"
        ).convert_alpha()

    def update(self):
        while self.running:
            self.handle_events()
            self.blit()
            pygame.display.flip()

            self.dt = self.clock.tick(self.settings["framerate"])
            self.player.update(self)

        sys.exit(0)

    def blit(self):
        self.screen.blit(self.background)
        self.player.blit(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.player.facing[-1] != "left":
                    self.inputs["direction"] = "right"
                if event.key == pygame.K_LEFT and self.player.facing[-1] != "right":
                    self.inputs["direction"] = "left"
                if event.key == pygame.K_UP and self.player.facing[-1] != "down":
                    self.inputs["direction"] = "up"
                if event.key == pygame.K_DOWN and self.player.facing[-1] != "up":
                    self.inputs["direction"] = "down"


if __name__ == "__main__":
    App()
