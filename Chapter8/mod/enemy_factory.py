import pygame
from random import randint, choice
from typing import Any, Final

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy

pygame.init()


class EnemyFactory():
    def __init__(self, **kwargs: Any) -> None:
        self._DIFFS: Final[dict[str, Any]] = kwargs

    def make(self, x: int, y: int, hldgs: list[Enemy], **kwargs: Any) -> Enemy:
        enemy = Enemy(x=x, y=y, hldgs=hldgs)
        for key, value in self._DIFFS.items():
            setattr(enemy, key, value)
        for key, value in kwargs.items():
            setattr(enemy, key, value)
        enemy.roll_image()
        return enemy

    @classmethod
    def bring_enemy(cls, enemies: list[Enemy], tmr: int) -> None:
        if tmr % 20 != 0: return
        match tmr:
            case _ if tmr < 450: 
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case 600:
                enemies.append(BOSS.make(x=480, y=Enemy.LINE_T/2, hldgs=enemies))
        # if tmr % 10 != 0: return
        # match tmr:
        #     case _ if tmr < 450: enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
        #     case _ if tmr < 900: enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
        #     case _ if tmr < 1350: enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
        #     case _ if tmr < 1800: enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))


def elapse_pillbox(enemy: Enemy) -> None:
    enemy.timer += 1
    if enemy.rect.centery > 240 and enemy.angle == 90:
        enemy.angle = choice([50, 70, 110, 130])
        enemy.hldgs.append(BULLET.make(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=enemy.hldgs))
    Enemy.move_linearly(enemy=enemy)
    angle = enemy.angle
    enemy.angle = 90+enemy.timer*10
    enemy.roll_image()
    enemy.angle = angle


BULLET = EnemyFactory(nega=pygame.image.load("image_gl/enemy0.png"), name="Bullet", speed=6, breakable=False)
RED_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy1.png"), name="RedCraft", speed=8)
BLUE_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy2.png"), name="BlueCraft", speed=12)
ABATIS = EnemyFactory(nega=pygame.image.load("image_gl/enemy3.png"), name="Abatis", speed=6, hp=3)
PILLBOX = EnemyFactory(nega=pygame.image.load("image_gl/enemy4.png"), name="Pillbox", speed=12, hp=2, elapse_func=elapse_pillbox)
BOSS = EnemyFactory(nega=pygame.image.load("image_gl/enemy_boss.png"), name="Boss", speed=4, hp=200)
