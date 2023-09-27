import pygame
from pygame.locals import K_SPACE

class Bullet():
    MISSILE_MAX = 200
    exist = [False]*MISSILE_MAX
    x = [0]*MISSILE_MAX
    y = [0]*MISSILE_MAX
    no = 0

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")


    @classmethod
    def set(cls, key, mother): # 自機の発射する弾をセットする
        if key[K_SPACE] == False: return
        cls.exist[cls.no] = True
        cls.x[cls.no] = mother.x
        cls.y[cls.no] = mother.y-50
        cls.no = (cls.no+1)%cls.MISSILE_MAX

    @classmethod
    def move(cls): # 弾の移動
        for i in range(cls.MISSILE_MAX):
            if cls.exist[i] == False: continue
            cls.y[i] -= 36
            if cls.y[i] < 0:
                cls.exist[i] = False
    
    @classmethod
    def draw(cls, screen): # 弾の描画
        for i in range(cls.MISSILE_MAX):
            if cls.exist[i] == False: continue
            screen.blit(cls.IMG_WEAPON, [cls.x[i]-10, cls.y[i]-32])

