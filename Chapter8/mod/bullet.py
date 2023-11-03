import pygame
pygame.init()
from pygame.locals import K_SPACE, K_z
from math import cos, sin, radians
from typing import Any, Literal

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sound import SE_SHOT, SE_BARRAGE

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite

class Bullet(Sprite):
    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")
    SPEED = 36

    def __init__(self, x: int, y: int, angle: int=270, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.IMG_WEAPON, cx=x, cy=y)
        self.angle: int = angle
        self.roll_image()
        self.hldgs: list[Bullet] = hldgs

    def move(self) -> Literal[False]:
        '''Bulletをangleに従って直線運動させます。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        self.rect.centerx += int(self.SPEED*cos(radians(self.angle)))
        self.rect.centery += int(self.SPEED*sin(radians(self.angle)))
        if self.rect.centery < 0 or self.rect.centerx < 0 or self.rect.centerx > 960:
            self.hldgs.remove(self)
        return False

key_scp: int = 0
key_z: int = 0
def bullet_set(key: pygame.key.ScancodeWrapper, bullets: list[Bullet], x: int, y: int, may_z: bool) -> bool: # 自機の発射する弾をセットする
    global key_scp, key_z
    key_scp = (key_scp+1)*key[K_SPACE]
    if key_scp%5 ==1:
        bullets.append(Bullet(x=x, y=y-50, hldgs=bullets))
        SE_SHOT.play()
    key_z = (key_z+1)*key[K_z]
    if key_z == 1 and may_z == True:
        for a in range(160, 390, 10):
            bullets.append(Bullet(x=x, y=y-50, angle=a, hldgs=bullets))
        SE_BARRAGE.play()
        return True
    return False
