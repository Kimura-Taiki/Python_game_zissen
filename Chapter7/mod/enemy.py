import pygame
pygame.init()
from math import cos, sin, radians
from typing import Any, Callable

class IntraSprite(pygame.sprite.Sprite):
    image: pygame.surface.Surface
    '''Group.drawを稼働させる為の画像情報です。'''
    rect: pygame.rect.Rect
    '''Group.drawを稼働させる為の矩形情報です。'''

    def __init__(self, group: Any, image: pygame.surface.Surface, cx: int, cy: int) -> None:
        super().__init__(group)
        self.image = image
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
        self.img: pygame.surface.Surface = self.DEFAULT_IMG
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.fire: Callable[[Enemy], None] = self.pass_func
        # self.image: pygame.surface.Surface = self.DEFAULT_IMG
        # self.rect: pygame.rect.Rect = pygame.rect.Rect(x-self.image.get_width()/2, y-self.image.get_height()/2, x+self.image.get_width()/2, y+self.image.get_height()/2)
    
    def move(self) -> None: # 敵オブジェクトの移動
        self.x += int(self.speed*cos(radians(self.angle)))
        self.rect.centerx = self.x
        self.y += int(self.speed*sin(radians(self.angle)))
        self.rect.centery = self.y
        (self.fire)(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.hldgs.remove(self)

    def draw(self, screen: pygame.surface.Surface) -> None: #的オブジェクトの描画
        img_rz:pygame.surface.Surface = pygame.transform.rotozoom(surface=self.img, angle=-90-self.angle, scale=1.0)
        screen.blit(img_rz, [self.x-img_rz.get_width()/2, self.y-img_rz.get_height()/2])

def enemies_move(enemies: list[Enemy]) -> None:
    for enemy in enemies[:]:
        enemy.move()

def enemies_draw(screen: pygame.surface.Surface, enemies: list[Enemy]) -> None:
    pygame.sprite.Group(enemies).draw(surface=screen)
    # for enemy in enemies[:]:
    #     enemy.draw(screen=screen)

# from inspect import getmembers
e = Enemy(x=100, y=200)
# print(getmembers(e))
# exit()

# pass
# pygame 2.5.2 (SDL 2.28.3, Python 3.12.0)
# Hello from the pygame community. https://www.pygame.org/contribute.html
# [('DEFAULT_IMG', <Surface(58x52x8 SW)>), 
#  ('LINE_B', 800),
#  ('LINE_L', -80), 
#  ('LINE_R', 1040), 
#  ('LINE_T', -80), 
#  ('_Sprite__g', set()), 
#  ('__annotations__', {'LINE_T': <class 'int'>, 
#                       'LINE_B': <class 'int'>, 
#                       'LINE_L': <class 'int'>, 
#                       'LINE_R': <class 'int'>, 
#                       'DEFAULT_IMG': <class 'pygame.surface.Surface'>}), 
#  ('__class__', <class 'mod.enemy.Enemy'>), 
#  ('__delattr__', <method-wrapper '__delattr__' of Enemy object at 0x104445f10>), 
#  ('__dict__', {'_Sprite__g': set(), 
#                'image': <Surface(58x52x8 SW)>, 
#                'rect': <rect(71, 174, 58, 52)>, 
#                'x': 100, 
#                'y': 200, 
#                'hldgs': None, 
#                'name': '----', 
#                'img': <Surface(58x52x8 SW)>, 
#                'speed': 6, 
#                'angle': 90, 
#                'breakable': True, 
#                'fire': <function Enemy.pass_func at 0x10444e200>}), 
#  ('__dir__', <built-in method __dir__ of Enemy object at 0x104445f10>), 
#  ('__doc__', None), 
#  ('__eq__', <method-wrapper '__eq__' of Enemy object at 0x104445f10>), 
#  ('__format__', <built-in method __format__ of Enemy object at 0x104445f10>), 
#  ('__ge__', <method-wrapper '__ge__' of Enemy object at 0x104445f10>), 
#  ('__getattribute__', <method-wrapper '__getattribute__' of Enemy object at 0x104445f10>), 
#  ('__getstate__', <built-in method __getstate__ of Enemy object at 0x104445f10>), 
#  ('__gt__', <method-wrapper '__gt__' of Enemy object at 0x104445f10>), 
#  ('__hash__', <method-wrapper '__hash__' of Enemy object at 0x104445f10>), 
#  ('__init__', <bound method Enemy.__init__ of <Enemy Sprite(in 0 groups)>>), 
#  ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x14f7e9d20>), 
#  ('__le__', <method-wrapper '__le__' of Enemy object at 0x104445f10>), 
#  ('__lt__', <method-wrapper '__lt__' of Enemy object at 0x104445f10>), 
#  ('__module__', 'mod.enemy'), 
#  ('__ne__', <method-wrapper '__ne__' of Enemy object at 0x104445f10>), 
#  ('__new__', <built-in method __new__ of type object at 0x103155178>), 
#  ('__reduce__', <built-in method __reduce__ of Enemy object at 0x104445f10>), 
#  ('__reduce_ex__', <built-in method __reduce_ex__ of Enemy object at 0x104445f10>), 
#  ('__repr__', <bound method Sprite.__repr__ of <Enemy Sprite(in 0 groups)>>), 
#  ('__setattr__', <method-wrapper '__setattr__' of Enemy object at 0x104445f10>), 
#  ('__sizeof__', <built-in method __sizeof__ of Enemy object at 0x104445f10>), 
#  ('__str__', <method-wrapper '__str__' of Enemy object at 0x104445f10>), 
#  ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x14f7e9d20>), 
#  ('__weakref__', None), 
#  ('add', <bound method Sprite.add of <Enemy Sprite(in 0 groups)>>), 
#  ('add_internal', <bound method Sprite.add_internal of <Enemy Sprite(in 0 groups)>>), 
#  ('alive', <bound method Sprite.alive of <Enemy Sprite(in 0 groups)>>), 
#  ('angle', 90), 
#  ('breakable', True), 
#  ('draw', <bound method Enemy.draw of <Enemy Sprite(in 0 groups)>>), 
#  ('fire', <function Enemy.pass_func at 0x10444e200>), 
#  ('groups', <bound method Sprite.groups of <Enemy Sprite(in 0 groups)>>), 
#  ('hldgs', None), 
#  ('image', <Surface(58x52x8 SW)>), 
#  ('img', <Surface(58x52x8 SW)>), 
#  ('kill', <bound method Sprite.kill of <Enemy Sprite(in 0 groups)>>), 
#  ('move', <bound method Enemy.move of <Enemy Sprite(in 0 groups)>>), 
#  ('name', '----'), 
#  ('pass_func', <function Enemy.pass_func at 0x10444e200>), 
#  ('rect', <rect(71, 174, 58, 52)>), 
#  ('remove', <bound method Sprite.remove of <Enemy Sprite(in 0 groups)>>), 
#  ('remove_internal', <bound method Sprite.remove_internal of <Enemy Sprite(in 0 groups)>>), 
#  ('speed', 6), 
#  ('update', <bound method Sprite.update of <Enemy Sprite(in 0 groups)>>), 
#  ('x', 100), 
#  ('y', 200)]