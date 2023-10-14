import pygame
pygame.init()
from random import randint
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy


class EnemyFactory():
    def __init__(self, diffs: dict[str, Any]) -> None:
        self.diffs = diffs
    
    def make(self, x: int, y: int, hldgs: list[Enemy], add_diffs: dict[str, Any]={}) -> Enemy:
        enemy = Enemy(x=x, y=y, hldgs=hldgs)
        for key, value in self.diffs.items():
            setattr(enemy, key, value)
        for key, value in add_diffs.items():
            setattr(enemy, key, value)
        return enemy
    
    @classmethod
    def bring_enemy(cls, enemies: list[Enemy], tmr: int) -> None: # 敵を出す
        # if tmr%30 == 0:
        if tmr%10 == 0:
            enemies.append(TORPEDOER.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
    
def torpedo_run(enemy: Enemy) -> None: # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
    if enemy.y > 360:
        enemy.hldgs.append(TORPEDO.make(x=enemy.x, y=enemy.y, hldgs=enemy.hldgs))
        enemy.angle = -45
        enemy.speed = 16

TORPEDOER = EnemyFactory({'img':pygame.image.load("image_gl/enemy1.png"),   'name':"Torpedoer", 'fire':torpedo_run})
TORPEDO =   EnemyFactory({'img':pygame.image.load("image_gl/enemy0.png"),   'name':"Torpedo",   'speed':10, 'breakable':False})
