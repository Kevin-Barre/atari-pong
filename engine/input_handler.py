from __future__ import annotations
from typing import Protocol
import pygame


class InputHandler(Protocol):
    def get_direction(self) -> int: ...


class PlayerInputHandler:
    def __init__(self, key_up: int, key_down: int) -> None:
        self._key_up   = key_up
        self._key_down = key_down

    def get_direction(self) -> int:
        keys = pygame.key.get_pressed()
        if keys[self._key_up]:
            return -1
        if keys[self._key_down]:
            return 1
        return 0
