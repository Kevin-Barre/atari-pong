from __future__ import annotations
from enum import Enum, auto
from state.ball import Ball
from state.paddle import Paddle
from state.power_up import PowerUp
import constants


class CollisionType(Enum):
    NONE        = auto()
    WALL_TOP    = auto()
    WALL_BOTTOM = auto()
    OUT_LEFT    = auto()
    OUT_RIGHT   = auto()


class CollisionEngine:
    def check_walls(self, ball: Ball) -> CollisionType:
        if ball.y - ball.radius <= 0:
            return CollisionType.WALL_TOP
        if ball.y + ball.radius >= constants.SCREEN_HEIGHT:
            return CollisionType.WALL_BOTTOM
        if ball.x - ball.radius <= 0:
            return CollisionType.OUT_LEFT
        if ball.x + ball.radius >= constants.SCREEN_WIDTH:
            return CollisionType.OUT_RIGHT
        return CollisionType.NONE

    def check_paddle(self, ball: Ball, paddle: Paddle) -> bool:
        return (
            ball.x + ball.radius >= paddle.x
            and ball.x - ball.radius <= paddle.x + paddle.width
            and ball.y + ball.radius >= paddle.y
            and ball.y - ball.radius <= paddle.y + paddle.height
        )

    def check_power_up(self, ball: Ball, power_up: PowerUp) -> bool:
        if not power_up.active:
            return False
        dx = ball.x - power_up.x
        dy = ball.y - power_up.y
        return (dx * dx + dy * dy) <= (ball.radius + power_up.radius) ** 2
