import pygame
pygame.init()
from pygame.locals import K_SPACE, K_z
from math import cos, sin, radians

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.starship import StarShip

class Bullet():
    bullets = []
    key_scp = 0
    key_z = 0

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")

    def __init__(self, x: int, y: int, a :int=270, hldgs=None) -> None:
        self.x = x
        self.y = y
        self.a = a
        self.hldgs: list[Bullet] = hldgs

    # @classmethod
    # def set(cls, key: pygame.key.ScancodeWrapper, mother: StarShip) -> None: # 自機の発射する弾をセットする
    #     cls.key_scp = (cls.key_scp+1)*key[K_SPACE]
    #     if cls.key_scp%5 ==1:
    #         cls.bullets.append(Bullet(mother.x, mother.y-50))
    #     cls.key_z = (cls.key_z+1)*key[K_z]
    #     if cls.key_z == 1:
    #         for a in range(160, 390, 10):
    #             cls.bullets.append(Bullet(mother.x, mother.y-50, a))

    @classmethod
    def move(cls) -> None: # 弾の移動
        for bullet in cls.bullets:
            bullet.x += 36*cos(radians(bullet.a))
            bullet.y += 36*sin(radians(bullet.a))
            if bullet.y < 0 or bullet.x < 0 or bullet.x > 960:
                del bullet
    
    @classmethod
    def draw(cls, screen: pygame.surface.Surface) -> None: # 弾の描画
        for bullet in cls.bullets:
            img_rz = pygame.transform.rotozoom(cls.IMG_WEAPON, -90-bullet.a, 1.0)
            screen.blit(img_rz, [bullet.x-img_rz.get_width()/2, bullet.y-img_rz.get_height()/2])

key_scp: int = 0
key_z: int = 0
def bullet_set(key: pygame.key.ScancodeWrapper, bullets: list[Bullet], x: int, y: int) -> None: # 自機の発射する弾をセットする
    global key_scp, key_z
    key_scp = (key_scp+1)*key[K_SPACE]
    if key_scp%5 ==1:
        bullets.append(Bullet(x, y-50))
    key_z = (key_z+1)*key[K_z]
    if key_z == 1:
        for a in range(160, 390, 10):
            bullets.append(Bullet(x, y-50, a))


