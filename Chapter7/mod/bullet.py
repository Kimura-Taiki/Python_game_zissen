import pygame
pygame.init()
from pygame.locals import K_SPACE, K_z
from math import cos, sin, radians
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite

class Bullet(Sprite):
    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")
    SPEED = 36

    def __init__(self, x: int, y: int, angle: int=270, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.IMG_WEAPON, cx=x, cy=y)
        self.x: int = x
        self.y: int = y
        self.angle: int = angle
        self.roll_image()
        self.hldgs: list[Bullet] = hldgs

    def move(self) -> None:
        self.x += int(self.SPEED*cos(radians(self.angle)))
        self.rect.centerx = self.x
        self.y += int(self.SPEED*sin(radians(self.angle)))
        self.rect.centery = self.y
        if self.y < 0 or self.x < 0 or self.x > 960:
            self.hldgs.remove(self)

    def draw(self, screen: pygame.surface.Surface) -> None:
        img_rz = pygame.transform.rotozoom(surface=self.IMG_WEAPON, angle=-90-self.angle, scale=1.0)
        screen.blit(source=img_rz, dest=(self.x-img_rz.get_width()/2, self.y-img_rz.get_height()/2))

key_scp: int = 0
key_z: int = 0
def bullet_set(key: pygame.key.ScancodeWrapper, bullets: list[Bullet], x: int, y: int, may_z: bool) -> bool: # 自機の発射する弾をセットする
    global key_scp, key_z
    key_scp = (key_scp+1)*key[K_SPACE]
    if key_scp%5 ==1:
        bullets.append(Bullet(x=x, y=y-50, hldgs=bullets))
    key_z = (key_z+1)*key[K_z]
    if key_z == 1 and may_z == True:
        for a in range(160, 390, 10):
            bullets.append(Bullet(x=x, y=y-50, angle=a, hldgs=bullets))
        return True
    return False

def bullets_move(bullets: list[Bullet]) -> None:
    for bullet in bullets[:]:
        bullet.move()

def bullets_draw(screen: pygame.surface.Surface, bullets: list[Bullet]) -> None:
    pygame.sprite.Group(bullets).draw(surface=screen)
