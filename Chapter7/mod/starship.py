import pygame
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from typing import Any

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

class StarShip(pygame.sprite.Sprite):
    # 画像の読み込み
    IMG_SSHIP: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/starship.png"),
        pygame.image.load("image_gl/starship_l.png"),
        pygame.image.load("image_gl/starship_r.png"),
        pygame.image.load("image_gl/starship_burner.png")
    ]
    WIDTH: int = IMG_SSHIP[0].get_width()
    HEIGHT: int = IMG_SSHIP[0].get_height()
    GROUP: pygame.sprite.Group = pygame.sprite.Group()
    print("GROUPは{}です".format(GROUP), type(GROUP))
    V = 20
    KEY_MAPPING = ({"key":K_UP,     "dx": 0, "dy":-V, "roll":0},
                   {"key":K_DOWN,   "dx": 0, "dy": V, "roll":0},
                   {"key":K_LEFT,   "dx":-V, "dy": 0, "roll":1},
                   {"key":K_RIGHT,  "dx": V, "dy": 0, "roll":2})

    def __init__(self) -> None:
        super().__init__(self.GROUP)
        self.x: int = 480
        self.y: int = 360
        self.roll: int = 0
        self.image: pygame.surface.Surface = self.IMG_SSHIP[0]
        self.rect: pygame.rect.Rect = pygame.rect.Rect(400-self.WIDTH/2, 360-self.HEIGHT/2, self.WIDTH, self.HEIGHT)
        print("StarShip.rectは [ {} ] です！".format(self.rect))

    def move(self, key: pygame.key.ScancodeWrapper) -> None: # 自機の移動
        self.roll = 0
        for map in self.KEY_MAPPING:
            if key[map["key"]] != 1: continue
            self.x += map["dx"]
            self.y += map["dy"]
            self.roll = map["roll"]
        self.x = min(max(self.x, 40), 920)
        self.y = min(max(self.y, 80), 640)
        self.rect.center = (self.x, self.y)

    def draw(self, screen: pygame.surface.Surface, tmr: int=0, muteki: int=0) -> None:
        if muteki%2 != 0: return
        screen.blit(self.IMG_SSHIP[3], (self.x-8, self.y+40+(tmr%3)*2))
        self.GROUP.draw(screen)
        # screen.blit(source=self.IMG_SSHIP[self.roll], dest=(self.x-37, self.y-48))
