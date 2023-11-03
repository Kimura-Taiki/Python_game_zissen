import pygame
from typing import Any, Literal, Optional

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.sprite import Sprite

class Effect(Sprite):
    IMG_EXPLODE: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/explosion1.png"),
        pygame.image.load("image_gl/explosion2.png"),
        pygame.image.load("image_gl/explosion3.png"),
        pygame.image.load("image_gl/explosion4.png"),
        pygame.image.load("image_gl/explosion5.png")
    ]
    
    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.IMG_EXPLODE[0], cx=x, cy=y)
        self.angle: int = 90
        self.hldgs: list[Effect] = hldgs
        self.duration: int = 0
    
    def elapse(self, t: int =1) -> Optional[bool]:
        '''時間経過をさせます。
        
        この命令はリスト内表記で繰り返し処理する際にmypyで弾かれぬべく、
        戻り値の型ヒントにOptional[bool]を与えてあります。'''
        self.duration += t
        if self.duration >= 5:
            self.hldgs.remove(self)
        else:
            self.image = self.IMG_EXPLODE[self.duration]
    
    def draw(self, screen: pygame.surface.Surface) -> Literal[False]:
        '''Effectを描画します。screen.blitを使用しています。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        screen.blit(source=self.IMG_EXPLODE[self.duration], dest=(self.x-48, self.y-48))
        return False

