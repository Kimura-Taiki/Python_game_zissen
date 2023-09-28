import pygame
pygame.init()
# import math
# import random
from math import cos, sin, radians
from random import randint

class Enemy():

    IMG_ENEMY = (
        pygame.image.load("image_gl/enemy0.png"),
        pygame.image.load("image_gl/enemy1.png")
    )

    enemies = []

    LINE_T = -80
    LINE_B = 800
    LINE_L = -80
    LINE_R = 1040

    def __init__(self, x, y, angle, type, speed) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.type = type
        self.speed = speed

    @classmethod
    def bring_enemy(cls, tmr): # 敵を出す
        if tmr%30 == 0:
            cls.enemies.append(Enemy(x=randint(20, 940), y=cls.LINE_T, angle=90, type=1, speed=6))
    
    def fire(self): # 弾を発射する
        if self.type == 1 and self.y > 360:
            self.enemies.append(Enemy(x=self.x, y=self.y, angle=90, type=0, speed=8))
            self.angle = -45
            self.speed = 16

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies:
            enemy.x += enemy.speed*cos(radians(enemy.angle))
            enemy.y += enemy.speed*sin(radians(enemy.angle))
            enemy.fire()
            # if enemy.type == 1 and enemy.y > 360:
            #     cls.enemies.append(Enemy(x=enemy.x, y=enemy.y, angle=90, type=0, speed=8))
            #     enemy.angle = -45
            #     enemy.speed = 16
            if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
                del enemy

    @classmethod
    def draw(cls, screen): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz = pygame.transform.rotozoom(cls.IMG_ENEMY[enemy.type], -90-enemy.angle, 1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])
