import pygame
pygame.init()
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.enemy import Enemy
from mod.effect import Effect
from mod.sound import SE_EXPLOSION, SE_DAMAGE
from mod.starship import StarShip

def nie_shoot_down() -> None: raise NotImplementedError("敵機撃墜時の命令が設定されていません")
def nie_damaged() -> None: raise NotImplementedError("自機被弾時の命令が設定されていません")

class Conflict():
    shoot_down_func: Callable[[], None] = nie_shoot_down
    damaged_func: Callable[[], None] = nie_damaged

    @classmethod
    def hit_bullet_and_enemy(cls, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect]) -> None:
        for enemy in [enemy for enemy in enemies if enemy.breakable == True][:]:
            hitten: list[Bullet] = pygame.sprite.spritecollide(sprite=enemy, group=pygame.sprite.Group(bullets), dokill=False)
            for bullet in hitten:
                cls.shoot_down_func()
                effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
                SE_EXPLOSION.play()
                bullet.hldgs.remove(bullet)
                enemy.hldgs.remove(enemy)
                break

    @classmethod
    def hit_ss_and_enemy(cls, s_ship: StarShip, enemies: list[Enemy], effects: list[Effect]) -> None:
        if s_ship.muteki > 0:
            s_ship.muteki -= 1
            return
        hitten: list[Enemy] = pygame.sprite.spritecollide(sprite=s_ship.craft, group=pygame.sprite.Group(enemies), dokill=False)
        if hitten == []: return
        s_ship.muteki = 60 if s_ship.muteki == 0 else s_ship.muteki
        for enemy in hitten[:]:
            effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
            SE_DAMAGE.play()
            s_ship.hp -= 10
            enemy.hldgs.remove(enemy)
