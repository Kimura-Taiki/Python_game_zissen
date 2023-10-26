import pygame
from typing import Any, Literal

class Effect():
    IMG_EXPLODE: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/explosion1.png"),
        pygame.image.load("image_gl/explosion2.png"),
        pygame.image.load("image_gl/explosion3.png"),
        pygame.image.load("image_gl/explosion4.png"),
        pygame.image.load("image_gl/explosion5.png")
    ]
    
    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        self.x: int = x
        self.y: int = y
        self.hldgs: list[Effect] = hldgs
        self.duration: int = 0
    
    def elapse(self, t: int) -> Literal[False]:
        '''Effectの持続時間を経過させます。規定時間を過ぎると消滅します。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        self.duration += t
        if self.duration >= 5:
            self.hldgs.remove(self)
        return False
    
    def draw(self, screen: pygame.surface.Surface) -> Literal[False]:
        '''Effectを描画します。screen.blitを使用しています。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        screen.blit(source=self.IMG_EXPLODE[self.duration], dest=(self.x-48, self.y-48))
        return False

