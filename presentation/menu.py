from __future__ import annotations
import pygame
import constants


class Menu:
    def __init__(self) -> None:
        self._font_title = pygame.font.Font(None, 90)
        self._font_body  = pygame.font.Font(None, 38)
        self._font_small = pygame.font.Font(None, 28)

    def draw_main(self, surface: pygame.Surface) -> None:
        surface.fill(constants.BLACK)
        cy = constants.SCREEN_HEIGHT // 2
        self._blit_centered(surface, self._font_title, "ATARI PONG",                           cy - 70,  constants.WHITE)
        self._blit_centered(surface, self._font_body,  "[ ENTER ]  Jugar",                     cy + 20,  constants.GRAY)
        self._blit_centered(surface, self._font_small, "Universidad Internacional del Ecuador", cy + 130, constants.GRAY)

    def draw_mode_selection(self, surface: pygame.Surface) -> None:
        surface.fill(constants.BLACK)
        cy = constants.SCREEN_HEIGHT // 2
        self._blit_centered(surface, self._font_title, "MODO DE JUEGO",            cy - 80,  constants.WHITE)
        self._blit_centered(surface, self._font_body,  "[ 1 ]  1 Jugador  (vs IA)", cy,       constants.CYAN)
        self._blit_centered(surface, self._font_body,  "[ 2 ]  2 Jugadores",        cy + 50,  constants.GREEN)
        self._blit_centered(surface, self._font_small, "[ ESC ]  volver",           cy + 110, constants.GRAY)

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
