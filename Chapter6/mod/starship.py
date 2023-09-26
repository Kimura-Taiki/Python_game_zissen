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
    def coord():
        return StarShip.x, StarShip.y
    
    def move(key): # 自機の移動
        for map in StarShip.KEY_MAPPING:
            if key[map["key"]] != 1: continue
            StarShip.x += map["dx"]
            StarShip.y += map["dy"]
        StarShip.x = min(max(StarShip.x, 40), 920)
        StarShip.y = min(max(StarShip.y, 80), 640)

    def draw(screen):
        screen.blit(StarShip.IMG_SSHIP, [StarShip.x-37, StarShip.y-48])

