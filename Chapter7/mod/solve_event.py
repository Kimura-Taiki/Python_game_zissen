import pygame
pygame.init()
import sys

def quit_event():
    pygame.quit()
    sys.exit()

event_mapping = [{"type":pygame.QUIT,                            "func":quit_event}]

def solve_event(mapping: list[dict]):
    for event in pygame.event.get():
        for map in mapping:
            if event.type == map["type"] and (event.type != pygame.KEYDOWN or event.key == map["key"]):
                map["func"]()
                break

