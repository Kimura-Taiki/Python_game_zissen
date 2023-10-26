import pygame
pygame.init()
import sys
from typing import Any

def quit_event() -> None:
    pygame.quit()
    sys.exit()

event_mapping: list[dict[str, Any]] = [{"type":pygame.QUIT,                            "func":quit_event}]

def solve_event(mapping: list[dict[str, Any]]) -> None:
    for event in pygame.event.get():
        for map in mapping:
            if event.type == map["type"] and (event.type != pygame.KEYDOWN or event.key == map["key"]):
                map["func"]()
                break

