import pygame
from typing import Any

class Effect():
    IMG_EXPLODE: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/explosion1.png"),
        pygame.image.load("image_gl/explosion2.png"),
        pygame.image.load("image_gl/explosion3.png"),
        pygame.image.load("image_gl/explosion4.png"),
        pygame.image.load("image_gl/explosion5.png")
    ]
    
    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        self.x: int = x
        self.y: int = y
        self.hldgs: list[Effect] = hldgs
        self.duration: int = 0
    
    def elapse(self, t: int=1) -> None:
        self.duration += t
        if self.duration >= 5:
            self.hldgs.remove(self)
    
    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(source=self.IMG_EXPLODE[self.duration], dest=(self.x-48, self.y-48))

def effects_elapse(effects: list[Effect]) -> None:
    for effect in effects:
        effect.elapse(t=1)

def effects_draw(screen: pygame.surface.Surface, effects: list[Effect]) -> None:
    for effect in effects:
        effect.draw(screen=screen)
