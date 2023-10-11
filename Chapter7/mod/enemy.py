import pygame
pygame.init()
from math import cos, sin, radians

class Enemy():

    enemies = []

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
    
    def mono_move(self): # 単体敵の移動
        self.x += self.speed*cos(radians(self.angle))
        self.y += self.speed*sin(radians(self.angle))
        self.fire(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.enemies.remove(self)

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies[:]:
            enemy.mono_move()
            # enemy.x += enemy.speed*cos(radians(enemy.angle))
            # enemy.y += enemy.speed*sin(radians(enemy.angle))
            # enemy.fire(enemy)
            # if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
            #     cls.enemies.remove(enemy)

    @classmethod
    def draw(cls, screen: pygame.surface.Surface): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz:pygame.surface.Surface = pygame.transform.rotozoom(surface=enemy.img, angle=-90-enemy.angle, scale=1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])

# enemies: list[Enemy] = []