from __future__ import annotations
import pygame
import constants


class GameOverScreen:
    def __init__(self) -> None:
        self._font_big   = pygame.font.Font(None, 80)
        self._font_body  = pygame.font.Font(None, 38)

    def draw(self, surface: pygame.Surface, winner: str) -> None:
        cy = constants.SCREEN_HEIGHT // 2
        self._blit_centered(surface, self._font_big,  f"¡{winner} gana!", cy - 70, constants.YELLOW)
        self._blit_centered(surface, self._font_body, "[ R ]  Reiniciar",  cy + 20, constants.WHITE)
        self._blit_centered(surface, self._font_body, "[ ESC ]  Menú",     cy + 65, constants.GRAY)

    def _blit_centered(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        y: int,
        color: tuple[int, int, int],
    ) -> None:
        surf = font.render(text, True, color)
        surface.blit(surf, (constants.SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
