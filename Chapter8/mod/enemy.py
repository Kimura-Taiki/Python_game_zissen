import pygame
pygame.init()
from math import cos, sin, radians
from typing import Any, Callable, Literal
from random import randint

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite
from mod.effect import Effect
from mod.sound import SE_EXPLOSION

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
        self.is_boss: bool = False
        self.flash_duration: int = 0
        self.hp: int = 1
        self.timer: int = 0
        self.mode: int = 0
        self.elapse_func: Callable[[Enemy], None] = self.move_linearly
        self.fire: Callable[[Enemy], None] = self.pass_func
    
    def elapse(self) -> Literal[False]:
        '''Enemyをangleに従って直線運動させます。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        (self.elapse_func)(self)
        (self.fire)(self)
        if self.rect.centerx < self.LINE_L or self.LINE_R < self.rect.centerx or self.rect.centery < self.LINE_T or self.LINE_B < self.rect.centery:
            self.hldgs.remove(self)
        return False
    
    def damaged(self, damage: int, effects: list[Effect], shoot_down_func: Callable[[], None]) -> None:
        '''Enemyの被弾時処理です。
        
        Conflict側で抱えてしまうと被弾時処理が嵩張りがち且つ敵個体毎に処理が変わる為、
        Enemyクラスに被弾時処理を委譲しています。'''
        dx, dy = int(self.rect.w/2), int(self.rect.h/2)
        effects.append(Effect(x=self.rect.centerx+randint(-dx, dx), y=self.rect.centery+randint(-dy, dy), hldgs=effects))
        SE_EXPLOSION.play()
        self.hp -= damage
        if self.hp <= 0:
            shoot_down_func()
            self.hldgs.remove(self)

    @classmethod
    def move_linearly(cls, enemy: 'Enemy') -> None:
        '''デフォルトの敵機運動としてself.elapseへ代入されている命令です。
        単純な等速直線運動を行います。'''
        enemy.rect.centerx += int(enemy.speed*cos(radians(enemy.angle)))
        enemy.rect.centery += int(enemy.speed*sin(radians(enemy.angle)))
