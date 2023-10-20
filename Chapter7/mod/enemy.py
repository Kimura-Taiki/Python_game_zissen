import pygame
pygame.init()
from math import cos, sin, radians
from typing import Any, Callable

class IntraSprite(pygame.sprite.Sprite):
    image: pygame.surface.Surface
    '''Group.drawを稼働させる為の画像情報です。'''
    nega: pygame.surface.Surface
    '''回転時に画像の原板となる画像情報です。'''
    rect: pygame.rect.Rect
    '''Group.drawを稼働させる為の矩形情報です。'''

    def __init__(self, group: Any, image: pygame.surface.Surface, cx: int, cy: int) -> None:
        super().__init__(group)
        self.image = image
        self.nega = image
        self.rect = pygame.rect.Rect(
            cx-int(self.image.get_width()/2), cy-int(self.image.get_height()/2),
            self.image.get_width(), self.image.get_height())


# class Enemy(pygame.sprite.Sprite):
class Enemy(IntraSprite):
    LINE_T: int = -80
    LINE_B: int = 800
    LINE_L: int = -80
    LINE_R: int = 1040

    DEFAULT_IMG: pygame.surface.Surface = pygame.image.load("image_gl/enemy1.png")

    @staticmethod
    def pass_func(enemy: Any=None) -> None:
        pass

    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.DEFAULT_IMG, cx=x, cy=y)
        self.x: int = x
        self.y: int = y
        self.hldgs: list[Enemy] = hldgs
        self.name: str = "----"
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.fire: Callable[[Enemy], None] = self.pass_func
    
    def roll_image(self) -> None:
        '''画像をangleに応じて回転'''
        x = self.rect.centerx
        y = self.rect.centery
        self.image = pygame.transform.rotozoom(surface=self.nega, angle=-90-self.angle, scale=1.0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
    
    def move(self) -> None: # 敵オブジェクトの移動
        self.x += int(self.speed*cos(radians(self.angle)))
        self.rect.centerx = self.x
        self.y += int(self.speed*sin(radians(self.angle)))
        self.rect.centery = self.y
        (self.fire)(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.hldgs.remove(self)

def enemies_move(enemies: list[Enemy]) -> None:
    for enemy in enemies[:]:
        enemy.move()

def enemies_draw(screen: pygame.surface.Surface, enemies: list[Enemy]) -> None:
    pygame.sprite.Group(enemies).draw(surface=screen)
