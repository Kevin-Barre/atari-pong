from __future__ import annotations
import math
import random
from state.ball import Ball
import constants


class BallPhysics:
    def move(self, ball: Ball) -> None:
        ball.x += ball.vx
        ball.y += ball.vy

    def bounce_vertical(self, ball: Ball) -> None:
        ball.vy = -ball.vy

    def bounce_off_paddle(
        self,
        ball: Ball,
        paddle_y: float,
        paddle_height: float,
    ) -> None:
        relative = (ball.y - (paddle_y + paddle_height / 2)) / (paddle_height / 2)
        relative = max(-1.0, min(1.0, relative))

        angle_rad = math.radians(relative * constants.MAX_BOUNCE_ANGLE)
        current_speed = math.hypot(ball.vx, ball.vy)
        new_speed = min(
            current_speed * (1.0 + constants.BALL_SPEED_INCREMENT),
            constants.BALL_MAX_SPEED,
        )

        direction_x = 1.0 if ball.vx < 0 else -1.0
        ball.vx = direction_x * new_speed * math.cos(angle_rad)
        ball.vy = new_speed * math.sin(angle_rad)

    def reset(self, ball: Ball, direction: int = 1) -> None:
        angle = math.radians(random.choice([-20, -10, 0, 10, 20]))
        ball.x = float(constants.SCREEN_WIDTH // 2)
        ball.y = float(constants.SCREEN_HEIGHT // 2)
        ball.vx = direction * constants.BALL_BASE_SPEED * math.cos(angle)
        ball.vy = constants.BALL_BASE_SPEED * math.sin(angle)
