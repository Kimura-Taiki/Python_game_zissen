import pygame
pygame.init()
from pygame.locals import K_SPACE, K_z
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.sound import SE_SHOT, SE_BARRAGE

def nie_is_diffusion() -> bool: raise NotImplementedError("拡散弾発射条件が設定されていません")
def nie_consume_diffusion() -> None: raise NotImplementedError("拡散弾発射時の消費が設定されていません")

class ShootBullet():
    '''弾の生成と発射を担うクラスです。
    現時点では単発弾(Single)と拡散弾(Diffusion)が発射できます。
    
    拡散弾には消費コストが必要なので事前に発射条件とコストを指定してください。'''
    is_diffusion: Callable[[], bool]= nie_is_diffusion
    consume_diffusion: Callable[[], None]= nie_consume_diffusion
    key_space: int= 0
    key_z: int = 0

    @classmethod
    def single_shot(cls, key: pygame.key.ScancodeWrapper, bullets: list[Bullet], x: int, y: int) -> None:
        '''Spaceキーで単発弾を発射します。'''
        cls.key_space = (cls.key_space+1)*key[K_SPACE]
        if cls.key_space%5 ==1:
            bullets.append(Bullet(x=x, y=y-50, hldgs=bullets))
            SE_SHOT.play()

    @classmethod
    def diffusion_shot(cls, key: pygame.key.ScancodeWrapper, bullets: list[Bullet], x: int, y: int) -> None:
        '''Zキーで拡散弾を発射します。
        
        発射時の消費コストが存在します。消費コストは外部に依存させたいのでdiffusion系の変数に任せています。'''
        cls.key_z = (cls.key_z+1)*key[K_z]
        if cls.key_z == 1 and cls.is_diffusion() == True:
            for a in range(160, 390, 10):
                bullets.append(Bullet(x=x, y=y-50, angle=a, hldgs=bullets))
            SE_BARRAGE.play()
            cls.consume_diffusion()
