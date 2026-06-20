from __future__ import annotations
import random
from abc import ABC, abstractmethod
from state.game_state import GameState
from state.paddle import Paddle
from state.power_up import PowerUp, PowerUpType
import constants


class PowerUpEffect(ABC):
    @abstractmethod
    def apply(self, paddle: Paddle) -> None: ...

    @abstractmethod
    def revert(self, paddle: Paddle) -> None: ...


class GrowPaddleEffect(PowerUpEffect):
    def apply(self, paddle: Paddle) -> None:
        paddle.height = int(paddle.height * constants.GROW_FACTOR)

    def revert(self, paddle: Paddle) -> None:
        paddle.height = constants.PADDLE_HEIGHT


class ShrinkPaddleEffect(PowerUpEffect):
    def apply(self, paddle: Paddle) -> None:
        paddle.height = int(paddle.height * constants.SHRINK_FACTOR)

    def revert(self, paddle: Paddle) -> None:
        paddle.height = constants.PADDLE_HEIGHT


_EFFECT_FOR: dict[PowerUpType, type[PowerUpEffect]] = {
    PowerUpType.GROW:   GrowPaddleEffect,
    PowerUpType.SHRINK: ShrinkPaddleEffect,
}


class PowerUpManager:
    def try_spawn(self, state: GameState, delta: float) -> None:
        if state.power_up is not None:
            return
        state.power_up_timer += delta
        if state.power_up_timer >= constants.POWER_UP_SPAWN_INTERVAL:
            state.power_up_timer = 0.0
            self._spawn(state)

    def apply_to_left(self, state: GameState) -> None:
        self._apply(state, state.paddle_left, side="left")

    def apply_to_right(self, state: GameState) -> None:
        self._apply(state, state.paddle_right, side="right")

    def update_timers(self, state: GameState, delta: float) -> None:
        if state.power_up_effect_left is not None:
            state.effect_timer_left -= delta
            if state.effect_timer_left <= 0.0:
                state.power_up_effect_left.revert(state.paddle_left)
                state.power_up_effect_left = None

        if state.power_up_effect_right is not None:
            state.effect_timer_right -= delta
            if state.effect_timer_right <= 0.0:
                state.power_up_effect_right.revert(state.paddle_right)
                state.power_up_effect_right = None

    def _spawn(self, state: GameState) -> None:
        x = random.randint(constants.SCREEN_WIDTH  // 4, constants.SCREEN_WIDTH  * 3 // 4)
        y = random.randint(60, constants.SCREEN_HEIGHT - 60)
        pu_type = random.choice(list(PowerUpType))
        state.power_up = PowerUp(type=pu_type, x=float(x), y=float(y))

    def _apply(self, state: GameState, paddle: Paddle, side: str) -> None:
        if state.power_up is None:
            return
        effect = _EFFECT_FOR[state.power_up.type]()
        effect.apply(paddle)
        state.power_up = None
        if side == "left":
            state.power_up_effect_left = effect
            state.effect_timer_left    = constants.POWER_UP_DURATION
        else:
            state.power_up_effect_right = effect
            state.effect_timer_right    = constants.POWER_UP_DURATION
