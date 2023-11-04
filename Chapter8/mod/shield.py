import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy
from mod.effect import Effect
from mod.sprite import Sprite
from mod.sound import SE_DAMAGE


class Shield():
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")

    shield: int
    muteki: int

    def __init__(self) -> None:
        self.shield = 100
        self.muteki = 0

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(source=self.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+self.shield*4, 680, (100-self.shield)*4, 12])
    
    def recover(self, rec: int) -> None:
        self.shield = min(100, self.shield+rec)

    def reset(self) -> None:
        self.shield = 100
        self.muteki = 0
