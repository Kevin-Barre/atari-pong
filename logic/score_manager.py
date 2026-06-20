from __future__ import annotations
from state.game_state import GameState, GameStatus
import constants


class ScoreManager:
    def award_point_left(self, state: GameState) -> None:
        state.score_left += 1
        self._check_winner(state)

    def award_point_right(self, state: GameState) -> None:
        state.score_right += 1
        self._check_winner(state)

    def reset(self, state: GameState) -> None:
        state.score_left = 0
        state.score_right = 0
        state.winner = ""

    def _check_winner(self, state: GameState) -> None:
        if state.score_left >= constants.WINNING_SCORE:
            state.winner = "Jugador 1"
            state.status = GameStatus.GAME_OVER
        elif state.score_right >= constants.WINNING_SCORE:
            state.winner = "Jugador 2" if state.two_player_mode else "IA"
            state.status = GameStatus.GAME_OVER
