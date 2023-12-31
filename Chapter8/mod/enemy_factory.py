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
        match tmr:
            case _ if 0 < tmr and tmr < 25*30 and tmr % 15 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 30*30 < tmr and tmr < 55*30 and tmr % 10 == 0:
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 60*30 < tmr and tmr < 85*30 and tmr % 15 == 0:
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
            case _ if 90*30 < tmr and tmr < 115*30 and tmr % 20 == 0:
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 120*30 < tmr and tmr < 145*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
            case _ if 150*30 < tmr and tmr < 175*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_B, hldgs=enemies, angle=270))
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies, angle=randint(70, 110)))
            case _ if 180*30 < tmr and tmr < 205*30 and tmr % 20 == 0:
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 210*30 < tmr and tmr < 235*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=Enemy.LINE_L, y=randint(40, 680), hldgs=enemies, angle=0))
                enemies.append(BLUE_CRAFT.make(x=Enemy.LINE_R, y=randint(40, 680), hldgs=enemies, angle=180))
            case _ if 240*30 < tmr and tmr < 265*30 and tmr % 30 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if tmr == 270*30:
                enemies.append(BOSS.make(x=480, y=int(Enemy.LINE_T/2), hldgs=enemies))


def elapse_pillbox(enemy: Enemy) -> None:
    enemy.timer += 1
    if enemy.rect.centery > 240 and enemy.angle == 90:
        enemy.angle = choice([50, 70, 110, 130])
        enemy.hldgs.append(BULLET.make(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=enemy.hldgs))
    Enemy.move_linearly(enemy=enemy)
    enemy.roll_image(angle=90+enemy.timer*10)

def elapse_boss(enemy: Enemy) -> None:
    enemy.timer += 1
    Enemy.move_linearly(enemy=enemy)
    match enemy.mode:
        case 0:
            if enemy.y >= 200: enemy.mode, enemy.angle = 1, 180
        case 1:
            if enemy.x < 200:
                enemy.hldgs.extend(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=i*20) for i in range(0, 10))
                enemy.mode, enemy.angle = 2, 0
        case 2:
            if enemy.x > 760:
                enemy.hldgs.extend(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=i*20) for i in range(0, 10))
                enemy.mode, enemy.angle = 1, 180
    if enemy.hp < 100 and enemy.timer % 30 == 0: enemy.hldgs.append(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=randint(60, 120)))


BULLET = EnemyFactory(nega=pygame.image.load("image_gl/enemy0.png"), name="Bullet", speed=6, breakable=False)
RED_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy1.png"), name="RedCraft", speed=8)
BLUE_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy2.png"), name="BlueCraft", speed=12)
ABATIS = EnemyFactory(nega=pygame.image.load("image_gl/enemy3.png"), name="Abatis", speed=6, hp=3)
PILLBOX = EnemyFactory(nega=pygame.image.load("image_gl/enemy4.png"), name="Pillbox", speed=12, hp=2, elapse_func=elapse_pillbox)
BOSS = EnemyFactory(nega=pygame.image.load("image_gl/enemy_boss.png"), name="Boss", speed=4, hp=200, elapse_func=elapse_boss, is_boss=True)
