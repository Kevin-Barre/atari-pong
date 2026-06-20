from __future__ import annotations


class WebInputHandler:
    def __init__(self, key_up: str, key_down: str, key_state: set) -> None:
        self._key_up    = key_up
        self._key_down  = key_down
        self._key_state = key_state

    def get_direction(self) -> int:
        if self._key_up   in self._key_state: return -1
        if self._key_down in self._key_state: return  1
        return 0
