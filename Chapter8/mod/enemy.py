import pygame
pygame.init()
from math import cos, sin, radians
from typing import Any, Callable, Literal

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
        self.hldgs: list[Enemy] = hldgs
        self.name: str = "----"
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.hp: int = 1
        self.timer: int = 0
        self.elapse_func: Callable[[Enemy], None] = self.move_linearly
        self.fire: Callable[[Enemy], None] = self.pass_func
    
    def elapse(self) -> Literal[False]: # 敵オブジェクトの移動
        '''Enemyをangleに従って直線運動させます。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        (self.elapse_func)(self)
        (self.fire)(self)
        if self.rect.centerx < self.LINE_L or self.LINE_R < self.rect.centerx or self.rect.centery < self.LINE_T or self.LINE_B < self.rect.centery:
            self.hldgs.remove(self)
        return False
    
    @classmethod
    def move_linearly(cls, enemy: 'Enemy') -> None:
        '''デフォルトの敵機運動としてself.elapseへ代入されている命令です。
        単純な等速直線運動を行います。'''
        enemy.rect.centerx += int(enemy.speed*cos(radians(enemy.angle)))
        enemy.rect.centery += int(enemy.speed*sin(radians(enemy.angle)))
