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
        for enemy in enemies[:]:
            cls.hit(enemy=enemy, s_ship=s_ship, effects=effects)
    
    @classmethod
    def hit(cls, enemy: Enemy, s_ship: StarShip, effects: list[Effect]) -> None:
        w: int = enemy.image.get_width()
        h: int = enemy.image.get_height()
        r: int = int((w+h)/4 + (74+96)/4)
        # if get_dis(x1=enemy.x, y1=enemy.y, x2=s_ship.x, y2=s_ship.y) < r*r:
        if get_dis(x1=enemy.x, y1=enemy.y, x2=s_ship.x, y2=s_ship.y) < r*r:
            effects.append(Effect(x=enemy.x, y=enemy.y, hldgs=effects))
            cls.shield = max(0, cls.shield-10)
            if cls.muteki == 0:
                cls.muteki = 60
            enemy.hldgs.remove(enemy)

    @classmethod
    def recover(cls, rec: int) -> None:
        cls.shield = min(100, cls.shield+rec)

def get_dis(x1: int, y1: int, x2: int, y2: int) -> int: # 二点間の距離を求める
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
