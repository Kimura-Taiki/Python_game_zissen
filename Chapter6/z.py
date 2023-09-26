def __z__():
    pass

g = +5
print(g)
exit()

# 自機関連の処理と変数
class StarShip():
    x = 460
    y = 380

    V = 20
    IMG_SSHIP = pygame.image.load("image_gl/starship.png")
    KEY_MAPPING = ({"key":pygame.K_UP,      "dx": 0, "dy":-V},
                   {"key":pygame.K_DOWN,    "dx": 0, "dy": V},
                   {"key":pygame.K_LEFT,    "dx":-V, "dy": 0},
                   {"key":pygame.K_RIGHT,   "dx": V, "dy": 0})

    @classmethod
    def coord():
        return StarShip.x, StarShip.y
    
    @classmethod
    def move(scrn, key):
        for map in StarShip.KEY_MAPPING:
            if key[map["key"]] == 1:
                StarShip.x = max(min(StarShip.x+map["dx"], 920), 20)
                StarShip.y = max(min(StarShip.y+map["dy"], 640), 40)
        scrn.blit(StarShip.IMG_SSHIP, [StarShip.x-37, StarShip.y-48])
