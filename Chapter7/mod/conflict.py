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
            hitten: list[Bullet] = pygame.sprite.spritecollide(sprite=enemy, group=pygame.sprite.Group(bullets), dokill=False)
            for bullet in hitten:
                shots_down += 1
                effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
                bullet.hldgs.remove(bullet)
                enemy.hldgs.remove(enemy)
                break
        return shots_down
