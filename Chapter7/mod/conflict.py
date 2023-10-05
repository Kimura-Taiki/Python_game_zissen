import pygame
pygame.init()
from math import cos, sin, radians
from random import randint

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.enemy import Enemy

class Conflict():
    
    @classmethod
    def hit_bullet_and_enemy(cls, bullets, enemies):
        for enemy in enemies:
            enemy.hit(bullets)


def get_dis(x1, y1, x2, y2): # 二点間の距離を求める
    return( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )
