import pygame
# from pygame.sprite import _Group
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

class IntraSprite(pygame.sprite.Sprite):
    def __init__(self, group: Any, image: pygame.surface.Surface, cx: int, cy: int) -> None:
        super().__init__(group)
        self.image = image
        self.rect = pygame.rect.Rect(
            cx-int(self.image.get_width()/2), cy-int(self.image.get_height()/2),
            self.image.get_width(), self.image.get_height())


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
    DEFAULT_Y: int = 360
    KEY_MAPPING = ({"key":K_UP,     "dx": 0, "dy":-V, "roll":0},
                   {"key":K_DOWN,   "dx": 0, "dy": V, "roll":0},
                   {"key":K_LEFT,   "dx":-V, "dy": 0, "roll":1},
                   {"key":K_RIGHT,  "dx": V, "dy": 0, "roll":2})
    
    def __init__(self) -> None:
        self.x: int = self.DEFAULT_X
        self.y: int = self.DEFAULT_Y
        self.group: Any = pygame.sprite.Group()
        self.craft: IntraSprite = IntraSprite(group=self.group, image=self.IMG_SSHIP[0], cx=self.DEFAULT_X, cy=self.DEFAULT_Y)
        self.burner: IntraSprite = IntraSprite(group=self.group, image=self.IMG_SSHIP[3], cx=self.DEFAULT_X, cy=self.DEFAULT_Y+56)

    def move(self, key: pygame.key.ScancodeWrapper) -> None: # 自機の移動
        roll = 0
        for map in self.KEY_MAPPING:
            if key[map["key"]] != 1: continue
            self.x += map["dx"]
            self.y += map["dy"]
            roll = map["roll"]
        self.x = min(max(self.x, 40), 920)
        self.y = min(max(self.y, 80), 640)
        self.craft.image = self.IMG_SSHIP[roll]
        self.craft.rect.center = (self.x, self.y)
        self.burner.rect.center = (self.x, self.y+56)

    def draw(self, screen: pygame.surface.Surface, tmr: int=0, muteki: int=0) -> None:
        if muteki%2 != 0: return
        self.group.draw(screen)
