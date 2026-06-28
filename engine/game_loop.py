from __future__ import annotations
from state.game_state import GameState, GameStatus
from state.ball import Ball
from state.paddle import Paddle
from logic.ball_physics import BallPhysics
from logic.collision import CollisionEngine, CollisionType
from logic.score_manager import ScoreManager
from logic.ai_controller import AIController
from logic.power_up_manager import PowerUpManager
from engine.input_handler import WebInputHandler
import constants


class GameLoop:
    def __init__(self) -> None:
        self._state = GameState()
        self._keys: set[str] = set()

        self._ball_physics  = BallPhysics()
        self._collision     = CollisionEngine()
        self._score_manager = ScoreManager()
        self._ai            = AIController()
        self._power_up_mgr  = PowerUpManager()

        self._input_p1 = WebInputHandler('KeyW',    'KeyS',       self._keys)
        self._input_p2 = WebInputHandler('ArrowUp', 'ArrowDown',  self._keys)

    def on_key_down(self, code: str) -> None:
        self._keys.add(code)
        self._handle_menu_key(code)

    def on_key_up(self, code: str) -> None:
        self._keys.discard(code)

    def update(self, delta: float) -> None:
        if self._state.status != GameStatus.PLAYING:
            return
        self._move_paddles()
        self._ball_physics.move(self._state.ball)
        self._resolve_collisions()
        self._power_up_mgr.try_spawn(self._state, delta)
        self._power_up_mgr.update_timers(self._state, delta)

    def to_dict(self) -> dict:
        s = self._state
        return {
            "status":           s.status.name,
            "ball":             {"x": s.ball.x, "y": s.ball.y, "radius": s.ball.radius},
            "paddleLeft":       {"x": s.paddle_left.x,  "y": s.paddle_left.y,
                                 "width": s.paddle_left.width,  "height": s.paddle_left.height},
            "paddleRight":      {"x": s.paddle_right.x, "y": s.paddle_right.y,
                                 "width": s.paddle_right.width, "height": s.paddle_right.height},
            "scoreLeft":        s.score_left,
            "scoreRight":       s.score_right,
            "powerUp":          {"x": s.power_up.x, "y": s.power_up.y,
                                 "radius": s.power_up.radius, "type": s.power_up.type.name}
                                if s.power_up else None,
            "effectTimerLeft":  s.effect_timer_left,
            "effectTimerRight": s.effect_timer_right,
            "winner":           s.winner,
            "twoPlayerMode":    s.two_player_mode,
        }

    def _handle_menu_key(self, code: str) -> None:
        status = self._state.status

        if status == GameStatus.MENU:
            if code == 'Enter':
                self._state.status = GameStatus.MODE_SELECTION

        elif status == GameStatus.MODE_SELECTION:
            if code == 'Digit1':
                self._state.two_player_mode = False
                self._start_game()
            elif code == 'Digit2':
                self._state.two_player_mode = True
                self._start_game()
            elif code == 'Escape':
                self._state.status = GameStatus.MENU

        elif status == GameStatus.PLAYING:
            if code == 'KeyP':
                self._state.status = GameStatus.PAUSED

        elif status == GameStatus.PAUSED:
            if code == 'KeyP':
                self._state.status = GameStatus.PLAYING

        elif status == GameStatus.GAME_OVER:
            if code == 'KeyR':
                self._reset_game()
            elif code == 'Escape':
                self._state.status = GameStatus.MENU

    def _move_paddles(self) -> None:
        dir_left = self._input_p1.get_direction()
        self._clamp_paddle(self._state.paddle_left, dir_left * constants.PADDLE_SPEED)

        if self._state.two_player_mode:
            dir_right = self._input_p2.get_direction()
            speed = constants.PADDLE_SPEED
        else:
            dir_right = self._ai.get_direction(self._state.ball, self._state.paddle_right)
            speed = constants.AI_SPEED
        self._clamp_paddle(self._state.paddle_right, dir_right * speed)

    def _clamp_paddle(self, paddle: Paddle, dy: float) -> None:
        paddle.y = max(0.0, min(constants.SCREEN_HEIGHT - paddle.height, paddle.y + dy))

    def _resolve_collisions(self) -> None:
        ball  = self._state.ball
        state = self._state
        wall  = self._collision.check_walls(ball)

        if wall == CollisionType.WALL_TOP:
            self._ball_physics.bounce_vertical(ball)
            ball.y = float(ball.radius)
        elif wall == CollisionType.WALL_BOTTOM:
            self._ball_physics.bounce_vertical(ball)
            ball.y = float(constants.SCREEN_HEIGHT - ball.radius)
        elif wall == CollisionType.OUT_LEFT:
            self._score_manager.award_point_right(state)
            if state.status == GameStatus.PLAYING:
                self._ball_physics.reset(ball, direction=1)
        elif wall == CollisionType.OUT_RIGHT:
            self._score_manager.award_point_left(state)
            if state.status == GameStatus.PLAYING:
                self._ball_physics.reset(ball, direction=-1)

        if ball.vx < 0 and self._collision.check_paddle(ball, state.paddle_left):
            self._ball_physics.bounce_off_paddle(ball, state.paddle_left.y, state.paddle_left.height)
            ball.x = state.paddle_left.x + state.paddle_left.width + ball.radius
        elif ball.vx > 0 and self._collision.check_paddle(ball, state.paddle_right):
            self._ball_physics.bounce_off_paddle(ball, state.paddle_right.y, state.paddle_right.height)
            ball.x = state.paddle_right.x - ball.radius

        if state.power_up is not None and self._collision.check_power_up(ball, state.power_up):
            if ball.vx > 0:
                self._power_up_mgr.apply_to_right(state)
            else:
                self._power_up_mgr.apply_to_left(state)

    def _start_game(self) -> None:
        self._score_manager.reset(self._state)
        self._state.power_up              = None
        self._state.power_up_effect_left  = None
        self._state.power_up_effect_right = None
        self._state.effect_timer_left     = 0.0
        self._state.effect_timer_right    = 0.0
        self._state.power_up_timer        = 0.0
        self._state.paddle_left           = Paddle.create_left()
        self._state.paddle_right          = Paddle.create_right()
        self._ball_physics.reset(self._state.ball)
        self._state.status = GameStatus.PLAYING

    def _reset_game(self) -> None:
        self._state.ball = Ball.create_default()
        self._start_game()
