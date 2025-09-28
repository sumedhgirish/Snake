import pygame
from pygame.math import Vector2

DIRECTIONS = {
    "right": Vector2(1, 0),
    "left": Vector2(-1, 0),
    "up": Vector2(0, -1),
    "down": Vector2(0, 1),
}


class Snake:

    def __init__(
        self,
        start_pos: Vector2,
        start_facing="right",
        start_length=4,
        color=(255, 255, 255),
    ):
        self.facing: list[str] = [start_facing] * 4
        self.body: list[Vector2] = [
            start_pos - DIRECTIONS[self.facing[i]] * i for i in range(start_length)
        ][::-1]

        self.speed: float = 0  # blocks per second
        self.dx: float = 0

        self.color = color

    def update(self, runtime):
        self.dx += runtime.dt * self.speed / 1000
        if self.dx >= 1:
            assert self.dx < 2, "Snake trying to move too fast"
            self.dx -= 1

            self.facing.append(runtime.inputs["direction"])
            self.body.append(self.body[-1] + DIRECTIONS[self.facing[-2]])

            self.body.pop(0)
            self.facing.pop(0)

    def blit(self, runtime):
        for i, ele in enumerate(self.body):
            pygame.draw.rect(
                runtime.screen,
                self.color,
                pygame.Rect(
                    (ele + DIRECTIONS[self.facing[i]] * self.dx)
                    * runtime.settings["blocksize"],
                    (runtime.settings["blocksize"], runtime.settings["blocksize"]),
                ),
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
