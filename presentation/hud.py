from __future__ import annotations
import pygame
import constants


class HUD:
    def __init__(self) -> None:
        self._font = pygame.font.Font(None, 54)

    def draw_pause(self, surface: pygame.Surface) -> None:
        self._draw_centered(surface, "PAUSA", constants.SCREEN_HEIGHT // 2 - 20)
        self._draw_centered_small(surface, "[ P ] continuar", constants.SCREEN_HEIGHT // 2 + 30)

    def _draw_centered(self, surface: pygame.Surface, text: str, y: int) -> None:
        surf = self._font.render(text, True, constants.WHITE)
        surface.blit(surf, (constants.SCREEN_WIDTH // 2 - surf.get_width() // 2, y))

    def _draw_centered_small(self, surface: pygame.Surface, text: str, y: int) -> None:
        font = pygame.font.Font(None, 32)
        surf = font.render(text, True, constants.GRAY)
        surface.blit(surf, (constants.SCREEN_WIDTH // 2 - surf.get_width() // 2, y))
