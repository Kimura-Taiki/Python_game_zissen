import pygame
from pygame.locals import K_SPACE

class Bullet():
    bullets = []
    key_scp = 0

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @classmethod
    def set(cls, key, mother): # 自機の発射する弾をセットする
        cls.key_scp = (cls.key_scp+1)*key[K_SPACE]
        if cls.key_scp%5 !=1: return
        cls.bullets.append(Bullet(mother.x, mother.y-50))

    @classmethod
    def move(cls): # 弾の移動
        for bullet in cls.bullets:
            bullet.y -= 36
            if bullet.y < 0:
                del bullet
    
    @classmethod
    def draw(cls, screen): # 弾の描画
        for bullet in cls.bullets:
            screen.blit(cls.IMG_WEAPON, [bullet.x, bullet.y])
