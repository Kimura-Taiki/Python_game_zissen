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
        enemy.roll_image()
        return enemy
    
    @classmethod
    def bring_enemy(cls, enemies: list[Enemy], tmr: int) -> None: # 敵を出す
        # if tmr%30 == 0:
        # if tmr%10 == 0:
        #     enemies.append(TORPEDOER.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
        if tmr%10 != 0: return
        match tmr:
            case _ if tmr < 450: enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if tmr < 900: enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if tmr < 1350: enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies,
                                                             add_diffs={'angle':randint(60, 120)}))
            case _ if tmr < 1800: enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
    
# def torpedo_run(enemy: Enemy) -> None: # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
#     if enemy.rect.centery > 360:
#         enemy.hldgs.append(TORPEDO.make(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=enemy.hldgs))
#         enemy.angle = -45
#         enemy.roll_image()
#         enemy.speed = 16

# TORPEDO =   EnemyFactory({'nega':pygame.image.load("image_gl/enemy0.png"),   'name':"Torpedo",   'speed':10, 'breakable':False})
# TORPEDOER = EnemyFactory({'nega':pygame.image.load("image_gl/enemy1.png"),   'name':"Torpedoer", 'fire':torpedo_run})


def abatis_angle() -> int: return randint(60, 120)
def const(a: Any) -> Any: return a

BULLET =    EnemyFactory({'nega':pygame.image.load("image_gl/enemy0.png"),  'name':"Bullet",    'speed':10, 'breakable':False})
RED_CRAFT = EnemyFactory({'nega':pygame.image.load("image_gl/enemy1.png"),  'name':"RedCraft",  'speed': 8})
BLUE_CRAFT =EnemyFactory({'nega':pygame.image.load("image_gl/enemy2.png"),  'name':"BlueCraft", 'speed':12})
ABATIS =    EnemyFactory({'nega':pygame.image.load("image_gl/enemy3.png"),  'name':"Abatis",    'speed': 6, 'hp':3})
PILLBOX =   EnemyFactory({'nega':pygame.image.load("image_gl/enemy4.png"),  'name':"Pillbox",   'speed':12, 'hp':2})
