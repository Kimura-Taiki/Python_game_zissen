import pygame
pygame.init()

class StarShip():
    x = 480
    y = 360

    # 画像の読み込み
    IMG_SSHIP = pygame.image.load("image_gl/starship.png")

    @classmethod
    def coord():
        return StarShip.x, StarShip.y
    
    def move(key): # 自機の移動
        if key[pygame.K_UP] == 1:
            StarShip.y = StarShip.y - 20
            if StarShip.y < 80:
                StarShip.y = 80
        if key[pygame.K_DOWN] == 1:
            StarShip.y = StarShip.y + 20
            if StarShip.y > 640:
                StarShip.y = 640
        if key[pygame.K_LEFT] == 1:
            StarShip.x = StarShip.x - 20
            if StarShip.x < 40:
                StarShip.x = 40
        if key[pygame.K_RIGHT] == 1:
            StarShip.x = StarShip.x + 20
            if StarShip.x > 920:
                StarShip.x = 920

    def draw(screen):
        screen.blit(StarShip.IMG_SSHIP, [StarShip.x-37, StarShip.y-48])

