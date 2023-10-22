import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite


BLACK = (  0,   0,   0)
SILVER= (192, 208, 224)
RED   = (255,   0,   0)
CYAN  = (  0, 224, 255)

img_title = [
    pygame.image.load("image_gl/nebula.png"),
    pygame.image.load("image_gl/logo.png")
]

idx = 0
score = 0

def draw_text(screen: pygame.surface.Surface,
              text: str, x: int, y: int, size: int, col: tuple[int, int, int]) -> None:
    '''文字を表示する命令です。'''
    sur = pygame.font.Font(name=None, size=size).render(text=text, antialias=True, color=col)
    screen.blit(source=sur, dest=[x-sur.get_width()/2, y-sur.get_height()/2])

