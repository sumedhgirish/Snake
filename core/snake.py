import pygame
from pygame.math import Vector2

DIRECTIONS = {
    "right": Vector2(1, 0),
    "left": Vector2(-1, 0),
    "up": Vector2(0, -1),
    "down": Vector2(0, 1),
}


# TODO: Remove this later
TAIL_OFFSETS = {
    "right": Vector2(1, 0.5),
    "left": Vector2(0, 0.5),
    "up": Vector2(0.5, 0),
    "down": Vector2(0.5, 1),
}

HEAD_OFFSETS = {
    "right": Vector2(0, 0.5),
    "left": Vector2(1, 0.5),
    "up": Vector2(0.5, 1),
    "down": Vector2(0.5, 0),
}


class Snake:

    def __init__(
        self,
        start_pos: Vector2,
        start_facing="right",
        color=(255, 255, 255),
    ):
        self.tail: Vector2 = start_pos - DIRECTIONS[start_facing] * 2
        self.head: Vector2 = start_pos
        self.next: Vector2 = start_pos + DIRECTIONS[start_facing]
        self.body: list[Vector2] = [start_pos - DIRECTIONS[start_facing]]
        self.facing = start_facing

        self.speed: float = 0  # blocks per second
        self.dx: float = 0

        self.color = color

    def update(self, runtime):
        if self.dx < 1:
            self.dx += runtime.dt * self.speed / 1000
        else:
            self.body.append(self.head)
            self.head = self.next
            self.next = self.head + DIRECTIONS[runtime.inputs["direction"]]
            self.facing = runtime.inputs["direction"]
            self.tail = self.body.pop(0)
            self.dx = 0

    def blit(self, runtime):
        pygame.draw.circle(
            runtime.screen,
            self.color,
            (
                self.tail
                + (self.body[0] - self.tail) * self.dx
                + TAIL_OFFSETS[self.facing]
            )
            * runtime.settings["blocksize"],
            runtime.settings["blocksize"] * 0.5,
        )
        pygame.draw.circle(
            runtime.screen,
            self.color,
            (
                self.head
                + (DIRECTIONS[self.facing]) * self.dx
                + HEAD_OFFSETS[self.facing]
            )
            * runtime.settings["blocksize"],
            runtime.settings["blocksize"] * 0.5,
        )
