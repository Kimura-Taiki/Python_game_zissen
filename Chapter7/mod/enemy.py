import pygame
pygame.init()
from math import cos, sin, radians

class Enemy():

    # enemies = []

    LINE_T: int = -80
    LINE_B: int = 800
    LINE_L: int = -80
    LINE_R: int = 1040

    DEFAULT_IMG: pygame.surface.Surface = pygame.image.load("image_gl/enemy1.png")

    @staticmethod
    def pass_func(arg=None):
        pass

    def __init__(self, x: int, y: int, hldgs=None) -> None:
        self.x: int = x
        self.y: int = y
        self.hldgs: list[Enemy] = hldgs
        self.name: str = "----"
        self.img: pygame.surface.Surface = self.DEFAULT_IMG
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.fire: function = self.pass_func
    
    def move(self): # 敵オブジェクトの移動
        self.x += self.speed*cos(radians(self.angle))
        self.y += self.speed*sin(radians(self.angle))
        self.fire(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.hldgs.remove(self)

    def draw(self, screen: pygame.surface.Surface): #的オブジェクトの描画
        img_rz:pygame.surface.Surface = pygame.transform.rotozoom(surface=self.img, angle=-90-self.angle, scale=1.0)
        screen.blit(img_rz, [self.x-img_rz.get_width()/2, self.y-img_rz.get_height()/2])

enemies: list[Enemy] = []

def enemies_move(enemies: list[Enemy]):
    for enemy in enemies[:]:
        enemy.move()

def enemies_draw(screen: pygame.surface.Surface, enemies: list[Enemy]):
    Enemy.l = 0
    for enemy in enemies[:]:
        enemy.draw(screen=screen)
        Enemy.l += 1