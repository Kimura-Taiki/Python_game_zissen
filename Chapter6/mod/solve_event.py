import pygame
import sys
from functools import partial
from mod.screen import screen, WIN_SIZE

def quit_event():
    pygame.quit()
    sys.exit()

def fullscreen_event(screen, size):
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen, size):
    screen = pygame.display.set_mode(size=size)

event_mapping = [
    {"type":pygame.QUIT,                            "func":quit_event},
    {"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)}]

def solve_event(mapping):
    for event in pygame.event.get():
        for map in mapping:
            if event.type == map["type"] and (event.type != pygame.KEYDOWN or event.key == map["key"]):
                map["func"]()
                break

