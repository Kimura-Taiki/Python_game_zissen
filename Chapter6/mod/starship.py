import pygame
pygame.init()
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

class StarShip():
    x = 480
    y = 360
    ss_d = 0
    tmr = 0

    # 画像の読み込み
    IMG_SSHIP = (
        pygame.image.load("image_gl/starship.png"),
        pygame.image.load("image_gl/starship_l.png"),
        pygame.image.load("image_gl/starship_r.png"),
        pygame.image.load("image_gl/starship_burner.png")
    )
    V = 20
    KEY_MAPPING = ({"key":K_UP,     "dx": 0, "dy":-V, "roll":0},
                   {"key":K_DOWN,   "dx": 0, "dy": V, "roll":0},
                   {"key":K_LEFT,   "dx":-V, "dy": 0, "roll":1},
                   {"key":K_RIGHT,  "dx": V, "dy": 0, "roll":2})

    @classmethod
    def coord(cls):
        return cls.x, cls.y
    
    @classmethod
    def move(cls, key): # 自機の移動
        cls.ss_d = 0
        for map in cls.KEY_MAPPING:
            if key[map["key"]] != 1: continue
            cls.x += map["dx"]
            cls.y += map["dy"]
            cls.ss_d = map["roll"]
        cls.x = min(max(cls.x, 40), 920)
        cls.y = min(max(cls.y, 80), 640)

    @classmethod
    def draw(cls, screen):
        screen.blit(cls.IMG_SSHIP[3], [cls.x-8, cls.y+40+(cls.tmr%3)*2])
        screen.blit(cls.IMG_SSHIP[cls.ss_d], [cls.x-37, cls.y-48])

