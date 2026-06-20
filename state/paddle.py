from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import constants


class Side(Enum):
    LEFT  = auto()
    RIGHT = auto()


@dataclass
class Paddle:
    x: int
    y: float
    width: int
    height: int
    side: Side

    @classmethod
    def create_left(cls) -> Paddle:
        return cls(
            x=constants.PADDLE_MARGIN,
            y=float(constants.SCREEN_HEIGHT // 2 - constants.PADDLE_HEIGHT // 2),
            width=constants.PADDLE_WIDTH,
            height=constants.PADDLE_HEIGHT,
            side=Side.LEFT,
        )

    @classmethod
    def create_right(cls) -> Paddle:
        return cls(
            x=constants.SCREEN_WIDTH - constants.PADDLE_MARGIN - constants.PADDLE_WIDTH,
            y=float(constants.SCREEN_HEIGHT // 2 - constants.PADDLE_HEIGHT // 2),
            width=constants.PADDLE_WIDTH,
            height=constants.PADDLE_HEIGHT,
            side=Side.RIGHT,
        )

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
