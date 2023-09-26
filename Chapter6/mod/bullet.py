import pygame

class Bullet():
    exist = False
    x = 0
    y = 0

    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")


    @classmethod
    def set(cls, mother): # 自機の発射する弾をセットする
        if cls.exist == False:
            cls.exist = True
            cls.x = mother.x
            cls.y = mother.y-50

    @classmethod
    def move(cls, screen): # 弾の移動
        if cls.exist == True:
            cls.y -= 36
            screen.blit(cls.IMG_WEAPON, [cls.x-10, cls.y-32])
            if cls.y < 0:
                cls.exist = False

