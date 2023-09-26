import pygame
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

class StarShip():
    x = 480
    y = 360

    # 画像の読み込み
    IMG_SSHIP = pygame.image.load("image_gl/starship.png")
    V = 20
    KEY_MAPPING = ({"key":K_UP,     "dx": 0, "dy":-V},
                   {"key":K_DOWN,   "dx": 0, "dy": V},
                   {"key":K_LEFT,   "dx":-V, "dy": 0},
                   {"key":K_RIGHT,  "dx": V, "dy": 0})

    @classmethod
    def coord(cls):
        return cls.x, cls.y
    
    @classmethod
    def move(cls, key): # 自機の移動
        for map in cls.KEY_MAPPING:
            if key[map["key"]] != 1: continue
            cls.x += map["dx"]
            cls.y += map["dy"]
        cls.x = min(max(cls.x, 40), 920)
        cls.y = min(max(cls.y, 80), 640)

    @classmethod
    def draw(cls, screen):
        screen.blit(cls.IMG_SSHIP, [cls.x-37, cls.y-48])

