import pygame
pygame.init()
from functools import partial

from mod.solve_event import event_mapping

WIN_X = 960
WIN_Y = 720
WIN_SIZE = (WIN_X, WIN_Y)

pygame.display.set_caption("Galaxy Lancer")
screen = pygame.display.set_mode(WIN_SIZE)

def fullscreen_event(screen, size):
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen, size):
    screen = pygame.display.set_mode(size=size)

event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})
