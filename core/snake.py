import pygame
import pygame.mixer as mixer
from pygame.math import Vector2
import pathlib

DIRECTIONS = {
    "right": Vector2(1, 0),
    "left": Vector2(-1, 0),
    "up": Vector2(0, -1),
    "down": Vector2(0, 1),
}

MOVEMENT_AUDIO_BASE = pathlib.Path("./audio/movement/")
SNAKE_AUDIO_BASE = pathlib.Path("./audio/snake/")


class Snake:

    def __init__(
        self,
        start_pos: Vector2,
        start_facing="right",
        start_length=4,
        color=(79, 120, 248),
    ):
        self.facing: list[str] = [start_facing] * start_length
        self.body: list[Vector2] = [
            start_pos - DIRECTIONS[self.facing[i]] * i for i in range(start_length)
        ][::-1]

        self.speed: float = 0  # blocks per second
        self.dx: float = 0

        self.color = color
        self.alive = True

        self.sfx = {
            "left": mixer.Sound(MOVEMENT_AUDIO_BASE / "left.wav"),
            "right": mixer.Sound(MOVEMENT_AUDIO_BASE / "right.wav"),
            "up": mixer.Sound(MOVEMENT_AUDIO_BASE / "up.wav"),
            "down": mixer.Sound(MOVEMENT_AUDIO_BASE / "down.wav"),
            "chomp": mixer.Sound(SNAKE_AUDIO_BASE / "chomp.wav"),
            "death": mixer.Sound(SNAKE_AUDIO_BASE / "death.wav"),
        }

    def update(self, runtime):
        if not self.alive:
            return

        self.dx += runtime.dt * self.speed / 1000
        if self.dx >= 1:
            assert self.dx < 2, "Snake trying to move too fast"
            self.dx -= 1

            self.facing.append(runtime.inputs["direction"])
            self.body.append(self.body[-1] + DIRECTIONS[self.facing[-2]])

            self.body.pop(0)
            self.facing.pop(0)

            if runtime.out_of_bounds(self.body[-1] + DIRECTIONS[self.facing[-1]]):
                self.alive = False
                self.sfx["death"].play()
                return

            if self.body[-1] == runtime.fruit.position:
                self.sfx["chomp"].play()
                runtime.fruit.position = runtime.fruit.get_new_position()

            if self.facing[-1] != self.facing[-2]:
                self.sfx[self.facing[-1]].play()

    def blit(self, runtime):
        for i, ele in enumerate(self.body):
            pygame.draw.rect(
                runtime.screen,
                self.color,
                pygame.Rect(
                    (ele + DIRECTIONS[self.facing[i]] * self.dx)
                    * runtime.settings["blocksize"],
                    (
                        runtime.settings["blocksize"],
                        runtime.settings["blocksize"],
                    ),
                ),
            )

        for i in range(len(self.body) - 1):
            if self.facing[i] != self.facing[i + 1]:
                pygame.draw.circle(
                    runtime.screen,
                    self.color,
                    (self.body[i] + Vector2(0.5, 0.5) + DIRECTIONS[self.facing[i]])
                    * runtime.settings["blocksize"],
                    runtime.settings["blocksize"] / 2,
                )

        pygame.draw.circle(
            runtime.screen,
            self.color,
            (
                self.body[-1]
                + Vector2(0.5, 0.5)
                + DIRECTIONS[self.facing[-1]] * (0.5 + self.dx)
            )
            * runtime.settings["blocksize"],
            runtime.settings["blocksize"] / 2,
        )

        pygame.draw.circle(
            runtime.screen,
            self.color,
            (
                self.body[0]
                + Vector2(0.5, 0.5)
                + DIRECTIONS[self.facing[0]] * (-0.5 + self.dx)
            )
            * runtime.settings["blocksize"],
            runtime.settings["blocksize"] / 2,
        )
