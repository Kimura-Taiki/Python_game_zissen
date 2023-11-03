import pygame
from pygame.locals import *

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

BLACK = (  0,   0,   0)
SILVER= (192, 208, 224)
RED   = (255,   0,   0)
CYAN  = (  0, 224, 255)

class Title():
    IMG_TITLE = [
        pygame.image.load("image_gl/nebula.png"),
        pygame.image.load("image_gl/logo.png")
    ]

    @classmethod
    def draw(cls, screen :pygame.surface.Surface, key :pygame.key.ScancodeWrapper, tmr: int) -> None:
        img_rz = pygame.transform.rotozoom(cls.IMG_TITLE[0], -tmr%360, 1.0)
        screen.blit(img_rz, [480-img_rz.get_width()/2, 280-img_rz.get_height()/2])
        screen.blit(cls.IMG_TITLE[1], [70, 160])
        draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)

def draw_text(screen: pygame.surface.Surface,
              text: str, x: int, y: int, size: int, col: tuple[int, int, int]) -> None:
    '''文字を表示する命令です。'''
    sur = pygame.font.Font(None, size=size).render(text, True, col)
    screen.blit(source=sur, dest=[x-sur.get_width()/2, y-sur.get_height()/2])

