from __future__ import annotations
import math
import random
from dataclasses import dataclass
import constants


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: int = constants.BALL_RADIUS

    @classmethod
    def create_default(cls) -> Ball:
        angle = math.radians(random.choice([-20, -10, 0, 10, 20]))
        direction = random.choice([-1, 1])
        return cls(
            x=float(constants.SCREEN_WIDTH // 2),
            y=float(constants.SCREEN_HEIGHT // 2),
            vx=direction * constants.BALL_BASE_SPEED * math.cos(angle),
            vy=constants.BALL_BASE_SPEED * math.sin(angle),
        )
