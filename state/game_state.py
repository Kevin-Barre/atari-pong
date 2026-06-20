from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any
from state.ball import Ball
from state.paddle import Paddle
from state.power_up import PowerUp


class GameStatus(Enum):
    MENU           = auto()
    MODE_SELECTION = auto()
    PLAYING        = auto()
    PAUSED         = auto()
    GAME_OVER      = auto()


@dataclass
class GameState:
    status:                GameStatus     = GameStatus.MENU
    ball:                  Ball           = field(default_factory=Ball.create_default)
    paddle_left:           Paddle         = field(default_factory=Paddle.create_left)
    paddle_right:          Paddle         = field(default_factory=Paddle.create_right)
    score_left:            int            = 0
    score_right:           int            = 0
    power_up:              PowerUp | None = None
    power_up_effect_left:  Any            = None
    power_up_effect_right: Any            = None
    effect_timer_left:     float          = 0.0
    effect_timer_right:    float          = 0.0
    power_up_timer:        float          = 0.0
    two_player_mode:       bool           = False
    winner:                str            = ""
