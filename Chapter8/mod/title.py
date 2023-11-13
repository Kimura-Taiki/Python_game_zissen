import pygame
from pygame.locals import K_SPACE
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

BLACK = (  0,   0,   0)
SILVER= (192, 208, 224)
RED   = (255,   0,   0)
CYAN  = (  0, 224, 255)


class Title():
    @staticmethod
    def __nie_start_game() -> None: raise NotImplementedError("Title.start_gameが未実装\nスタート時の初期化命令が設定されていません")
    start_game: Callable[[], None] = __nie_start_game

    IMG_TITLE = [
        pygame.image.load("image_gl/nebula.png"),
        pygame.image.load("image_gl/logo.png")
    ]

    @classmethod
    def title(cls, screen :pygame.surface.Surface, key :pygame.key.ScancodeWrapper, tmr: int) -> None:
        img_rz = pygame.transform.rotozoom(cls.IMG_TITLE[0], -tmr%360, 1.0)
        screen.blit(img_rz, [480-img_rz.get_width()/2, 280-img_rz.get_height()/2])
        screen.blit(cls.IMG_TITLE[1], [70, 160])
        draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
        if key[K_SPACE] == True:
            cls.start_game()

def draw_text(screen: pygame.surface.Surface,
              text: str, x: int, y: int, size: int, col: tuple[int, int, int]) -> None:
    '''文字を表示する命令です。'''
    font = pygame.font.Font(None, size)
    cx, cy = int(x-font.render(text, True, col).get_width()/2), int(y-font.render(text, True, col).get_height()/2)
    screen.blit(source=font.render(text, True, [int(i/2) for i in col]), dest=[cx+1, cy+1])
    screen.blit(source=font.render(text, True, [i+128 if i < 128 else 255 for i in col]), dest=[cx-1, cy-1])
    screen.blit(source=font.render(text, True, col), dest=[cx, cy])
