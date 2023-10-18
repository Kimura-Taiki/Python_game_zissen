import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))


class Shield():
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")

    ss_shield: int = 100
    ss_muteki: int = 0