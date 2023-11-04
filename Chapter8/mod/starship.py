import pygame
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite
from mod.shield import Shield

class StarShip():
    # 画像の読み込み
    IMG_SSHIP: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/starship.png"),
        pygame.image.load("image_gl/starship_l.png"),
        pygame.image.load("image_gl/starship_r.png"),
        pygame.image.load("image_gl/starship_burner.png")
    ]
    WIDTH: int = IMG_SSHIP[0].get_width()
    HEIGHT: int = IMG_SSHIP[0].get_height()
    BURNER_WIDTH: int = IMG_SSHIP[3].get_width()
    BURNER_HEIGTH: int = IMG_SSHIP[3].get_height()
    V = 20
    DEFAULT_X: int = 480
    DEFAULT_Y: int = 600
    MOVE_MAPPING = (0, -V, V, 0)
    ROLL_MAPPING = (0,  1, 2, 0)

    # hit_enemy = lambda: None
    # '''hit_ss_and_enemyを外部から注入する為の変数。
    
    # 空のラムダ関数が入っているので、そのままだとエラーを起こす。'''
    
    def __init__(self) -> None:
        self.group: Any = pygame.sprite.Group()
        self.craft: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[0], cx=self.DEFAULT_X, cy=self.DEFAULT_Y)
        self.burner: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[3], cx=self.DEFAULT_X, cy=self.DEFAULT_Y+56)
        self.shield: Shield = Shield()

    def move(self, key: pygame.key.ScancodeWrapper) -> None: # 自機の移動
        self.craft.image = self.IMG_SSHIP[self.ROLL_MAPPING[key[K_LEFT]+key[K_RIGHT]*2]]
        self.craft.rect.centerx = min(max(self.craft.rect.centerx+self.MOVE_MAPPING[key[K_LEFT]+key[K_RIGHT]*2], 40), 920)
        self.craft.rect.centery = min(max(self.craft.rect.centery+self.MOVE_MAPPING[key[K_UP]+key[K_DOWN]*2], 80), 640)
        self.burner.rect.center = self.craft.rect.centerx, self.craft.rect.centery+56

    def draw(self, screen: pygame.surface.Surface, tmr: int=0) -> None:
        if self.shield.muteki%2 != 0: return
        self.group.draw(screen)

    def reset(self) -> None:
        self.craft.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.burner.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.shield.reset()
    
    def recover(self, rec: int) -> None:
        self.shield.recover(rec=rec)

    def shield_draw(self, screen: pygame.surface.Surface) -> None:
        self.shield.draw(screen=screen)

    @property
    def hp(self) -> int:
        return self.shield.shield

    @hp.setter
    def hp(self, value: int) -> None:
        self.shield.shield = value

    def __iadd__(self, other: int) -> None:
        self.shield.shield += other