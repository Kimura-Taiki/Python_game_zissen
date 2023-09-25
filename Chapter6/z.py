def __z__():
    pass


import sys
import pygame
from functools import partial


def quit_event():
    pygame.quit()
    sys.exit()

def fullscreen_event(screen, size):
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen, size):
    screen = pygame.display.set_mode(size=size)

WIN_SIZE = (960, 720)
screen = pygame.display.set_mode(WIN_SIZE)

event_mapping = [
    {"type":pygame.QUIT,                            "func":quit_event},
    {"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)}]

# event_mapping = []
event_mapping.append({"type":pygame.QUIT,                            "func":quit_event},)
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)},)

print(event_mapping)
