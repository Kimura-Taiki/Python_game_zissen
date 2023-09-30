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

    def __init__(self, x, y, angle, speed) -> None:
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed

    @classmethod
    def bring_enemy(cls, tmr): # 敵を出す
        if tmr%30 == 0:
            cls.enemies.append(Torpedoer(x=randint(20, 940), y=cls.LINE_T, angle=90, speed=6))
    
    def fire(self): # 弾を発射する、ここでは空処理にする
        pass

    # def hit(self): # 弾と

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies:
            enemy.x += enemy.speed*cos(radians(enemy.angle))
            enemy.y += enemy.speed*sin(radians(enemy.angle))
            enemy.fire()
            if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
                del enemy

    @property
    def img(self):
        pass

    @classmethod
    def draw(cls, screen): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz = pygame.transform.rotozoom(enemy.img, -90-enemy.angle, 1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])

class Torpedoer(Enemy):
    IMG = pygame.image.load("image_gl/enemy1.png")

    def fire(self): # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
        if self.y > 360:
            self.enemies.append(Torpedo(x=self.x, y=self.y, angle=90, speed=8))
            self.angle = -45
            self.speed = 16

    @property
    def img(self):
        return self.IMG

class Torpedo(Enemy):
    IMG = pygame.image.load("image_gl/enemy0.png")
    @property
    def img(self):
        return self.IMG