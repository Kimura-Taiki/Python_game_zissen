import pygame
pygame.init()
from random import randint

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy


class EnemyFactory():
    def __init__(self, diffs: dict) -> None:
        self.diffs = diffs
    
    def make(self, x: int, y: int, add_diffs: dict={}) -> Enemy:
        enemy = Enemy(x=x, y=y)
        for key, value in self.diffs.items():
            setattr(enemy, key, value)
        for key, value in add_diffs.items():
            setattr(enemy, key, value)
        return enemy
    
    @classmethod
    def bring_enemy(cls, enemies: list[Enemy], tmr: int): # 敵を出す
        # if tmr%30 == 0:
        if tmr%10 == 0:
            enemies.append(TORPEDOER.make(x=randint(20, 940), y=Enemy.LINE_T))
    
def torpedo_run(enemy: Enemy): # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
    if enemy.y > 360:
        enemy.enemies.append(TORPEDO.make(x=enemy.x, y=enemy.y))
        enemy.angle = -45
        enemy.speed = 16

TORPEDOER = EnemyFactory({'img':pygame.image.load("image_gl/enemy1.png"),   'name':"Torpedoer", 'fire':torpedo_run})
TORPEDO =   EnemyFactory({'img':pygame.image.load("image_gl/enemy0.png"),   'name':"Torpedo",   'speed':10, 'breakable':False})
