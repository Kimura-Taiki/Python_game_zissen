import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy
from mod.starship import StarShip
from mod.effect import Effect


class Shield():
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")

    shield: int
    muteki: int

    def __init__(self) -> None:
        self.shield = 100
        self.muteki = 0

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(source=self.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+self.shield*4, 680, (100-self.shield)*4, 12])
    
    def hit_ss_and_enemy(self, enemies: list[Enemy], s_ship: StarShip, effects: list[Effect]) -> None:
        if self.muteki > 0:
            self.muteki -= 1
            return
        craft = s_ship.craft
        hitten: list[Enemy] = pygame.sprite.spritecollide(sprite=craft, group=pygame.sprite.Group(enemies), dokill=False)
        if hitten == []: return
        self.muteki = 60 if self.muteki == 0 else self.muteki
        for enemy in hitten[:]:
            effects.append(Effect(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=effects))
            self.shield = max(0, self.shield-10)
            enemy.hldgs.remove(enemy)

    def recover(self, rec: int) -> None:
        self.shield = min(100, self.shield+rec)
