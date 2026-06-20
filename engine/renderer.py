from __future__ import annotations
import pygame
from state.game_state import GameState
from state.power_up import PowerUpType
import constants


class Renderer:
    def __init__(self, surface: pygame.Surface) -> None:
        self._surface    = surface
        self._font_score = pygame.font.Font(None, 80)
        self._font_ui    = pygame.font.Font(None, 34)

    def draw_game(self, state: GameState) -> None:
        self._surface.fill(constants.BLACK)
        self._draw_center_line()
        self._draw_paddles(state)
        self._draw_ball(state)
        self._draw_power_up(state)
        self._draw_scores(state)
        self._draw_effect_timers(state)

    def _draw_center_line(self) -> None:
        cx = constants.SCREEN_WIDTH // 2
        for y in range(10, constants.SCREEN_HEIGHT, 30):
            pygame.draw.rect(self._surface, constants.GRAY, (cx - 2, y, 4, 16))

    def _draw_paddles(self, state: GameState) -> None:
        for paddle in (state.paddle_left, state.paddle_right):
            pygame.draw.rect(
                self._surface, constants.WHITE,
                (paddle.x, int(paddle.y), paddle.width, paddle.height),
                border_radius=4,
            )

    def _draw_ball(self, state: GameState) -> None:
        b = state.ball
        pygame.draw.circle(
            self._surface, constants.WHITE,
            (int(b.x), int(b.y)), b.radius,
        )

    def _draw_power_up(self, state: GameState) -> None:
        pu = state.power_up
        if pu is None or not pu.active:
            return
        color = constants.GREEN if pu.type == PowerUpType.GROW else constants.RED
        pygame.draw.circle(self._surface, color,        (int(pu.x), int(pu.y)), pu.radius)
        pygame.draw.circle(self._surface, constants.WHITE, (int(pu.x), int(pu.y)), pu.radius, 2)

    def _draw_scores(self, state: GameState) -> None:
        left_surf  = self._font_score.render(str(state.score_left),  True, constants.WHITE)
        right_surf = self._font_score.render(str(state.score_right), True, constants.WHITE)
        cx = constants.SCREEN_WIDTH // 2
        self._surface.blit(left_surf,  (cx // 2 - left_surf.get_width()  // 2, 15))
        self._surface.blit(right_surf, (cx + cx // 2 - right_surf.get_width() // 2, 15))

    def _draw_effect_timers(self, state: GameState) -> None:
        if state.power_up_effect_left is not None:
            label = self._font_ui.render(
                f"P1  {state.effect_timer_left:.0f}s", True, constants.YELLOW,
            )
            self._surface.blit(label, (10, constants.SCREEN_HEIGHT - 36))

        if state.power_up_effect_right is not None:
            label = self._font_ui.render(
                f"P2  {state.effect_timer_right:.0f}s", True, constants.YELLOW,
            )
            self._surface.blit(
                label,
                (constants.SCREEN_WIDTH - label.get_width() - 10, constants.SCREEN_HEIGHT - 36),
            )
