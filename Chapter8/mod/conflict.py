import pygame
pygame.init()

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.enemy import Enemy
from mod.effect import Effect
from mod.sound import SE_EXPLOSION, SE_DAMAGE
from mod.starship import StarShip

class Conflict():
    @classmethod
    def hit_bullet_and_enemy(cls, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect]) -> int:
        shots_down: int = 0
        for enemy in [enemy for enemy in enemies if enemy.breakable == True][:]:
            hitten: list[Bullet] = pygame.sprite.spritecollide(sprite=enemy, group=pygame.sprite.Group(bullets), dokill=False)
            for bullet in hitten:
                shots_down += 1
                effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
                SE_EXPLOSION.play()
                bullet.hldgs.remove(bullet)
                enemy.hldgs.remove(enemy)
                break
        return shots_down

def hit_ss_and_enemy(self: StarShip, enemies: list[Enemy], effects: list[Effect]) -> None:
    if self.shield.muteki > 0:
        self.shield.muteki -= 1
        return
    hitten: list[Enemy] = pygame.sprite.spritecollide(sprite=self.craft, group=pygame.sprite.Group(enemies), dokill=False)
    if hitten == []: return
    self.shield.muteki = 60 if self.shield.muteki == 0 else self.shield.muteki
    for enemy in hitten[:]:
        effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
        SE_DAMAGE.play()
        self.hp = max(0, self.hp-10)
        enemy.hldgs.remove(enemy)
