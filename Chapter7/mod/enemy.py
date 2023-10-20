import pygame
pygame.init()
from math import cos, sin, radians
from typing import Any, Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite

class Enemy(Sprite):
    LINE_T: int = -80
    LINE_B: int = 800
    LINE_L: int = -80
    LINE_R: int = 1040

    DEFAULT_IMG: pygame.surface.Surface = pygame.image.load("image_gl/enemy1.png")

    @staticmethod
    def pass_func(enemy: Any=None) -> None:
        pass

    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.DEFAULT_IMG, cx=x, cy=y)
        self.x: int = x
        self.y: int = y
        self.hldgs: list[Enemy] = hldgs
        self.name: str = "----"
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.fire: Callable[[Enemy], None] = self.pass_func
    
    def move(self) -> None: # 敵オブジェクトの移動
        self.x += int(self.speed*cos(radians(self.angle)))
        self.rect.centerx = self.x
        self.y += int(self.speed*sin(radians(self.angle)))
        self.rect.centery = self.y
        (self.fire)(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.hldgs.remove(self)

def enemies_move(enemies: list[Enemy]) -> None:
    for enemy in enemies[:]:
        enemy.move()

def enemies_draw(screen: pygame.surface.Surface, enemies: list[Enemy]) -> None:
    pygame.sprite.Group(enemies).draw(surface=screen)
