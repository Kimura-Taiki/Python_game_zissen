import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy
from mod.starship import StarShip
from mod.effect import Effect


class Shield():
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")

    shield: int = 100
    muteki: int = 0

    @classmethod
    def draw(cls, screen: pygame.surface.Surface) -> None:
        screen.blit(source=cls.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+cls.shield*4, 680, (100-cls.shield)*4, 12])
    
    @classmethod
    def hit_ss_and_enemy(cls, enemies: list[Enemy], s_ship: StarShip, effects: list[Effect]) -> None:
        if cls.muteki > 0:
            cls.muteki -= 1
            return
        craft = s_ship.craft
        hitten: list[Enemy] = pygame.sprite.spritecollide(sprite=craft, group=pygame.sprite.Group(enemies), dokill=False)
        if hitten == []: return
        cls.muteki = 60 if cls.muteki == 0 else cls.muteki
        for enemy in hitten[:]:
            effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
            cls.shield = max(0, cls.shield-10)
            enemy.hldgs.remove(enemy)

    @classmethod
    def recover(cls, rec: int) -> None:
        cls.shield = min(100, cls.shield+rec)
