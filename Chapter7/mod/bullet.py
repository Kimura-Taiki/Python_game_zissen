import pygame
pygame.init()
from pygame.locals import K_SPACE, K_z
from math import cos, sin, radians

class Bullet():
    bullets = []
    key_scp = 0
    key_z = 0

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")

    def __init__(self, x, y, a=270) -> None:
        self.x = x
        self.y = y
        self.a = a

    @classmethod
    def set(cls, key, mother): # 自機の発射する弾をセットする
        cls.key_scp = (cls.key_scp+1)*key[K_SPACE]
        if cls.key_scp%5 ==1:
            cls.bullets.append(Bullet(mother.x, mother.y-50))
        cls.key_z = (cls.key_z+1)*key[K_z]
        if cls.key_z == 1:
            for a in range(160, 390, 10):
                cls.bullets.append(Bullet(mother.x, mother.y-50, a))

    @classmethod
    def move(cls): # 弾の移動
        for bullet in cls.bullets:
            bullet.x += 36*cos(radians(bullet.a))
            bullet.y += 36*sin(radians(bullet.a))
            if bullet.y < 0 or bullet.x < 0 or bullet.x > 960:
                del bullet
    
    @classmethod
    def draw(cls, screen): # 弾の描画
        for bullet in cls.bullets:
            img_rz = pygame.transform.rotozoom(cls.IMG_WEAPON, -90-bullet.a, 1.0)
            screen.blit(img_rz, [bullet.x-img_rz.get_width()/2, bullet.y-img_rz.get_height()/2])
