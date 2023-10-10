import pygame
pygame.init()
from math import cos, sin, radians

class Enemy():

    enemies = []

    LINE_T = -80
    LINE_B = 800
    LINE_L = -80
    LINE_R = 1040

    # DEFAULT_PARAMS = (('name', None), ('img', None), ('speed', 6), ('angle', 90), ('breakable', True), ('fire', no_func))
        # for tuple in self.DEFAULT_PARAMS:
        #     setattr(enemy, tuple[0], getattr(self, tuple[0]))
    DEFAULT_IMG = pygame.image.load("image_gl/enemy1.png")

    @staticmethod
    def pass_func(arg=None):
        pass

    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y
        self.name: str = "----"
        self.img: pygame.surface.Surface = self.DEFAULT_IMG
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.fire: function = self.pass_func

    @classmethod
    def move(cls): # 敵オブジェクトの移動
        for enemy in cls.enemies[:]:
            enemy.x += enemy.speed*cos(radians(enemy.angle))
            enemy.y += enemy.speed*sin(radians(enemy.angle))
            enemy.fire(enemy)
            if enemy.x < cls.LINE_L or cls.LINE_R < enemy.x or enemy.y < cls.LINE_T or cls.LINE_B < enemy.y:
                cls.enemies.remove(enemy)

    @classmethod
    def draw(cls, screen): # 敵オブジェクトの描画
        for enemy in cls.enemies:
            img_rz = pygame.transform.rotozoom(surface=enemy.img, angle=-90-enemy.angle, scale=1.0)
            screen.blit(img_rz, [enemy.x-img_rz.get_width()/2, enemy.y-img_rz.get_height()/2])
