import pygame
from typing import Any

class Sprite(pygame.sprite.Sprite):
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
