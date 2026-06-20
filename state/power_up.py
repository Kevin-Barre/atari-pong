from dataclasses import dataclass
from enum import Enum, auto


class PowerUpType(Enum):
    GROW   = auto()
    SHRINK = auto()


@dataclass
class PowerUp:
    type: PowerUpType
    x: float
    y: float
    radius: int = 12
    active: bool = True
