import pygame
pygame.init()

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.enemy import Enemy

class Conflict():
    @classmethod
    def hit_bullet_and_enemy(cls, bullets: list[Bullet], enemies: list[Enemy]):
        for enemy in enemies:
            if enemy.breakable == False: continue
            hit(enemy, bullets)

def hit(enemy: Enemy, bullets: list[Bullet]) : # 自弾とのヒットチェック
    w = enemy.img.get_width()
    h = enemy.img.get_height()
    r = int((w+h)/4)+12
    for bullet in bullets[:]:
        if get_dis(enemy.x, enemy.y, bullet.x, bullet.y) < r*r:
            bullets.remove(bullet)
            enemy.enemies.remove(enemy)
            return

def get_dis(x1: int, y1: int, x2: int, y2: int): # 二点間の距離を求める
    return( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )
