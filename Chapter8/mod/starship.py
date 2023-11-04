import pygame
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite

class StarShip():
    # 画像の読み込み
    IMG_SSHIP: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/starship.png"),
        pygame.image.load("image_gl/starship_l.png"),
        pygame.image.load("image_gl/starship_r.png"),
        pygame.image.load("image_gl/starship_burner.png")
    ]
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")
    DEFAULT_X: int = 480
    DEFAULT_Y: int = 600
    V = 20
    MOVE_MAPPING = (0, -V, V, 0)
    ROLL_MAPPING = (0,  1, 2, 0)
    MAX_HP = 100

    def __init__(self) -> None:
        self.group: Any = pygame.sprite.Group()
        self.craft: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[0], cx=self.DEFAULT_X, cy=self.DEFAULT_Y)
        self.burner: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[3], cx=self.DEFAULT_X, cy=self.DEFAULT_Y+56)
        self._hp: int = self.MAX_HP
        self.muteki: int = 0

    def move(self, key: pygame.key.ScancodeWrapper) -> None: # 自機の移動
        self.craft.image = self.IMG_SSHIP[self.ROLL_MAPPING[key[K_LEFT]+key[K_RIGHT]*2]]
        self.craft.rect.centerx = min(max(self.craft.rect.centerx+self.MOVE_MAPPING[key[K_LEFT]+key[K_RIGHT]*2], 40), 920)
        self.craft.rect.centery = min(max(self.craft.rect.centery+self.MOVE_MAPPING[key[K_UP]+key[K_DOWN]*2], 80), 640)
        self.burner.rect.center = self.craft.rect.centerx, self.craft.rect.centery+56

    def draw(self, screen: pygame.surface.Surface, tmr: int=0) -> None:
        if self.muteki%2 != 0: return
        self.group.draw(screen)

    def reset(self) -> None:
        self.craft.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.burner.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.hp = self.MAX_HP
        self.muteki = 0
    
    def shield_draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(source=self.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+self.hp*4, 680, (100-self.hp)*4, 12])

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = min(self.MAX_HP, max(0, value))
