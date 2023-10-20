import pygame
pygame.init()

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.enemy import Enemy
from mod.effect import Effect

class Conflict():
    @classmethod
    def hit_bullet_and_enemy(cls, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect]) -> int:
        shots_down: int = 0
        for enemy in enemies:
            if enemy.breakable == False: continue
            shots_down += hit(enemy=enemy, bullets=bullets, effects=effects)
        return shots_down

def hit(enemy: Enemy, bullets: list[Bullet], effects: list[Effect]) -> int: # 自弾とのヒットチェック
    w: int = enemy.image.get_width()
    h: int = enemy.image.get_height()
    r: int = int((w+h)/4)+12
    for bullet in bullets[:]:
        if get_dis(enemy.x, enemy.y, bullet.x, bullet.y) < r*r:
            effects.append(Effect(x=enemy.x, y=enemy.y, hldgs=effects))
            bullets.remove(bullet)
            enemy.hldgs.remove(enemy)
            return 1
    return 0

def get_dis(x1: int, y1: int, x2: int, y2: int) -> int: # 二点間の距離を求める
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
