import pygame
from pygame.locals import K_SPACE

class Bullet():
    bullets = []

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @classmethod
    def set(cls, key, mother): # 自機の発射する弾をセットする
        if key[K_SPACE] == False: return
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
            

