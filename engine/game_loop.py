from __future__ import annotations
import sys
import pygame
import constants
from state.game_state import GameState, GameStatus
from state.paddle import Paddle
from state.ball import Ball
from logic.ball_physics       import BallPhysics
from logic.collision          import CollisionEngine, CollisionType
from logic.score_manager      import ScoreManager
from logic.ai_controller      import AIController
from logic.power_up_manager   import PowerUpManager
from engine.input_handler     import PlayerInputHandler
from engine.renderer          import Renderer
from presentation.hud              import HUD
from presentation.menu             import Menu
from presentation.game_over_screen import GameOverScreen


class GameLoop:
    def __init__(self) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Atari Pong")
        self._clock = pygame.time.Clock()

        self._state = GameState()

        self._renderer    = Renderer(self._screen)
        self._input_p1    = PlayerInputHandler(pygame.K_w,  pygame.K_s)
        self._input_p2    = PlayerInputHandler(pygame.K_UP, pygame.K_DOWN)

        self._ball_physics  = BallPhysics()
        self._collision     = CollisionEngine()
        self._score_manager = ScoreManager()
        self._ai            = AIController()
        self._power_up_mgr  = PowerUpManager()

        self._hud        = HUD()
        self._menu       = Menu()
        self._game_over  = GameOverScreen()

    def run(self) -> None:
        while True:
            delta = self._clock.tick(constants.FPS) / 1000.0
            self._handle_events()
            self._update(delta)
            self._render()
            pygame.display.flip()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._on_key(event.key)

    def _on_key(self, key: int) -> None:
        status = self._state.status

        if status == GameStatus.MENU:
            if key == pygame.K_RETURN:
                self._state.status = GameStatus.MODE_SELECTION

        elif status == GameStatus.MODE_SELECTION:
            if key == pygame.K_1:
                self._state.two_player_mode = False
                self._start_game()
            elif key == pygame.K_2:
                self._state.two_player_mode = True
                self._start_game()
            elif key == pygame.K_ESCAPE:
                self._state.status = GameStatus.MENU

        elif status == GameStatus.PLAYING:
            if key == pygame.K_p:
                self._state.status = GameStatus.PAUSED

        elif status == GameStatus.PAUSED:
            if key == pygame.K_p:
                self._state.status = GameStatus.PLAYING

        elif status == GameStatus.GAME_OVER:
            if key == pygame.K_r:
                self._reset_game()
            elif key == pygame.K_ESCAPE:
                self._state.status = GameStatus.MENU

    def _update(self, delta: float) -> None:
        if self._state.status != GameStatus.PLAYING:
            return
        self._move_paddles()
        self._ball_physics.move(self._state.ball)
        self._resolve_collisions()
        self._power_up_mgr.try_spawn(self._state, delta)
        self._power_up_mgr.update_timers(self._state, delta)

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
        paddle.y = max(
            0.0,
            min(constants.SCREEN_HEIGHT - paddle.height, paddle.y + dy),
        )

    def _resolve_collisions(self) -> None:
        ball  = self._state.ball
        state = self._state

        wall = self._collision.check_walls(ball)

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
            self._ball_physics.bounce_off_paddle(
                ball, state.paddle_left.y, state.paddle_left.height,
            )
            ball.x = state.paddle_left.x + state.paddle_left.width + ball.radius

        elif ball.vx > 0 and self._collision.check_paddle(ball, state.paddle_right):
            self._ball_physics.bounce_off_paddle(
                ball, state.paddle_right.y, state.paddle_right.height,
            )
            ball.x = state.paddle_right.x - ball.radius

        if state.power_up is not None and self._collision.check_power_up(ball, state.power_up):
            if ball.vx > 0:
                self._power_up_mgr.apply_to_right(state)
            else:
                self._power_up_mgr.apply_to_left(state)

    def _render(self) -> None:
        status = self._state.status

        if status == GameStatus.MENU:
            self._menu.draw_main(self._screen)

        elif status == GameStatus.MODE_SELECTION:
            self._menu.draw_mode_selection(self._screen)

        elif status in (GameStatus.PLAYING, GameStatus.PAUSED):
            self._renderer.draw_game(self._state)
            if status == GameStatus.PAUSED:
                self._hud.draw_pause(self._screen)

        elif status == GameStatus.GAME_OVER:
            self._renderer.draw_game(self._state)
            self._game_over.draw(self._screen, self._state.winner)

    def _start_game(self) -> None:
        self._score_manager.reset(self._state)
        self._state.power_up               = None
        self._state.power_up_effect_left   = None
        self._state.power_up_effect_right  = None
        self._state.effect_timer_left      = 0.0
        self._state.effect_timer_right     = 0.0
        self._state.power_up_timer         = 0.0
        self._state.paddle_left            = Paddle.create_left()
        self._state.paddle_right           = Paddle.create_right()
        self._ball_physics.reset(self._state.ball)
        self._state.status = GameStatus.PLAYING

    def _reset_game(self) -> None:
        self._state.ball = Ball.create_default()
        self._start_game()
