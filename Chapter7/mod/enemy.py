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
    def bring_enemy(cls, tmr): # 敵を出す
        if tmr%30 == 0:
            cls.enemies.append(Torpedoer(x=randint(20, 940), y=cls.LINE_T))
    
    def fire(self): # 弾を発射する、ここでは空処理にする
        pass

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies[:]:
            enemy.x += enemy.speed*cos(radians(enemy.angle))
            enemy.y += enemy.speed*sin(radians(enemy.angle))
            enemy.fire()
            if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
                cls.enemies.remove(enemy)

    @property
    def img(self):
        return self.IMG

    @classmethod
    def draw(cls, screen): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz = pygame.transform.rotozoom(enemy.img, -90-enemy.angle, 1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])

class Torpedoer(Enemy):
    IMG = pygame.image.load("image_gl/enemy1.png")

    def fire(self): # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
        if self.y > 360:
            self.enemies.append(Torpedo(x=self.x, y=self.y))
            self.angle = -45
            self.speed = 16

class Torpedo(Enemy):
    IMG = pygame.image.load("image_gl/enemy0.png")
    DEFAULT_SPEED = 10
    DEFAULT_BREAKABLE = False


class EnemyFactory():
    def no_func():
        pass

    DEFAULT_PARAMS = (('name', None), ('speed', 6), ('angle', 90), ('breakable', True), ('fire', no_func))

    def __init__(self, dict) -> None:
        self.img = pygame.image.load(dict['img'])
        for tuple in self.DEFAULT_PARAMS:
            if tuple[0] in dict.keys():
                setattr(self, tuple[0], dict[tuple[0]])
            else:
                setattr(self, tuple[0], tuple[1])
    
    def print(self):
        print(self.name, self.img, self.speed, self.angle, self.breakable, self.fire)

def torpedo_run(enemy: Enemy): # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
    if enemy.y > 360:
        enemy.enemies.append(Torpedo(x=enemy.x, y=enemy.y))
        enemy.angle = -45
        enemy.speed = 16


tac = EnemyFactory({'img':"image_gl/enemy1.png",    'name':"Torpedoer", 'fire':torpedo_run})
tpd = EnemyFactory({'img':"image_gl/enemy0.png",    'name':"Torpedo",   'speed':10, 'breakable':False})
print(tac, tpd)
tac.print()
tpd.print()