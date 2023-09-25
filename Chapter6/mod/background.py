import pygame
pygame.init()

from mod.screen import WIN_Y


# 背景関連の処理をBackGroundクラスへ集約
class BackGround():
    bg_y = 0
    IMG_GALAXY = pygame.image.load("image_gl/galaxy.png")
    
    @classmethod
    def scroll(cls, speed):
        BackGround.bg_y = (BackGround.bg_y+speed)%WIN_Y

    @classmethod
    def draw(cls, screen):
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y-WIN_Y])
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y])
