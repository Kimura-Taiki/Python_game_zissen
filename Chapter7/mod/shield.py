import pygame

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))


class Shield():
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")

    shield: int = 100
    muteki: int = 0

    @classmethod
    def draw(cls, screen: pygame.surface.Surface) -> None:
        screen.blit(source=cls.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+cls.shield*4, 680, (100-cls.shield)*4, 12])
    
    @classmethod
    def hit_ss_and_enemy(cls) -> None:
        if cls.muteki > 0:
            cls.muteki -= 1
            return
