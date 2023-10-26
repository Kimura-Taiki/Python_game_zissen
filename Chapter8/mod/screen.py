import pygame
pygame.init()
from functools import partial

from mod.solve_event import event_mapping

WIN_X: int = 960
WIN_Y: int = 720
WIN_SIZE: tuple[int, int] = (WIN_X, WIN_Y)

pygame.display.set_caption("Galaxy Lancer")
screen: pygame.surface.Surface = pygame.display.set_mode(WIN_SIZE)

def fullscreen_event(screen: pygame.surface.Surface, size: tuple[int, int]) -> None:
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen: pygame.surface.Surface, size: tuple[int, int]) -> None:
    screen = pygame.display.set_mode(size=size)

event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})
