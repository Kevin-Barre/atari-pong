from __future__ import annotations
from state.ball import Ball
from state.paddle import Paddle


class AIController:
    _DEAD_ZONE = 5.0

    def get_direction(self, ball: Ball, paddle: Paddle) -> int:
        diff = ball.y - paddle.center_y
        if abs(diff) <= self._DEAD_ZONE:
            return 0
        return 1 if diff > 0 else -1
