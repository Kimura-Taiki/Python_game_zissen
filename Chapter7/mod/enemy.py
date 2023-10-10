import pygame
pygame.init()
from math import cos, sin, radians
from random import randint

class Enemy():

    enemies = []

    LINE_T = -80
    LINE_B = 800
    LINE_L = -80
    LINE_R = 1040

    IMG = None
    DEFAULT_ANGLE = 90
    DEFAULT_SPEED = 6
    DEFAULT_BREAKABLE = True

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.angle = self.DEFAULT_ANGLE
        self.speed = self.DEFAULT_SPEED
        self.breakable = self.DEFAULT_BREAKABLE

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies[:]:
            enemy.x += enemy.speed*cos(radians(enemy.angle))
            enemy.y += enemy.speed*sin(radians(enemy.angle))
            enemy.fire(enemy)
            if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
                cls.enemies.remove(enemy)

    @classmethod
    def draw(cls, screen): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz = pygame.transform.rotozoom(surface=enemy.img, angle=-90-enemy.angle, scale=1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])
