import pygame
from pygame.locals import K_SPACE, K_z
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__':
    sys.path.append(dirname(dirname(__file__)))
from mod.bullet import Bullet
from mod.sound import SE_SHOT, SE_BARRAGE

pygame.init()


class ShootBullet():
    '''弾の生成と発射を担うクラスです。

    現時点では単発弾(Single)と拡散弾(Diffusion)が発射できます。このクラスは2つの主要なメソッド、
    single_shotとdiffusion_shotを提供し、それぞれ単発弾と拡散弾の発射を担当します。

    拡散弾の発射には外部からis_diffusion関数とconsume_diffusion関数を再定義する必要があります。
    これにより、拡散弾の発射条件と消費コストを外部からカスタマイズすることができます。

    ## 使用方法:
    1. is_diffusion関数とconsume_diffusion命令を外部で定義します。
    2. single_shotメソッドおよびdiffusion_shotメソッドを呼び出して弾を発射します。

    ## 拡張性:
    このクラスは単発弾と拡散弾の発射に焦点を当てていますが、将来的には新しい弾幕のパターンや
    タイプを追加するために拡張できる構造を提供しています。
    新しい弾幕の追加や既存の挙動の変更は新たなメソッドを追加する事で行ってください。
    '''

    @staticmethod
    def __not_implemented_is_diffusion() -> bool:
        raise NotImplementedError(
            "ShootBullet.is_diffusionが未実装\n拡散弾発射条件が設定されていません")
    is_diffusion: Callable[[], bool] = __not_implemented_is_diffusion
    '''拡散弾のコストを払い得るかを判断する為の関数です。
    is_diffusionは外部から定義、更新される事を想定しています。未更新時に常時エラーを吐くのは想定内です。

    この関数は、拡散弾を発射する前に呼び出され、拡散弾の発射条件が満たされているかを判定します。'''

    @staticmethod
    def __not_implemented_consume_diffusion() -> None:
        raise NotImplementedError(
            "ShootBullet.consume_diffusionが未実装\n拡散弾発射時の消費が設定されていません")
    consume_diffusion: Callable[[], None] = __not_implemented_consume_diffusion
    '''拡散弾を発射した際に、拡散弾のコストを実際に支払う処理を担う関数です。
    consume_diffusionは外部から定義、更新される事を想定しています。未更新時に常時エラーを吐くのは想定内です。

    この関数は、拡散弾を発射した直後に呼び出され、拡散弾の発射に関連するコストを支払います。'''

    _key_space_duration: int = 0
    '''Spaceキーが何フレームの間、押し続けられているかを示します。
    単射時の反応性を保持しつつ、押しっぱなし時の過剰な連射を抑える為に使われています。'''
    _key_z_duration: int = 0
    '''Zキーが何フレームの間、押し続けられているかを示します。
    単射時の反応性を保持しつつ、コストを費やす拡散弾の連射を防ぐ為に使われています。'''
    DIFFUSION_ANGLE_RANGE: range = range(160, 390, 10)

    @classmethod
    def single_shot(cls, pressed_keys: pygame.key.ScancodeWrapper,
                    bullets: list[Bullet], x: int, y: int) -> None:
        '''Spaceキーで単発弾を発射します。'''
        cls._key_space_duration = \
            (cls._key_space_duration+1)*pressed_keys[K_SPACE]
        if cls._key_space_duration % 5 == 1:
            bullets.append(Bullet(x=x, y=y-50, hldgs=bullets))
            SE_SHOT.play()

    @classmethod
    def diffusion_shot(cls, pressed_keys: pygame.key.ScancodeWrapper,
                       bullets: list[Bullet], x: int, y: int) -> None:
        '''Zキーで拡散弾を発射します。

        発射時の消費コストが存在します。消費コストは外部に依存させたいのでdiffusion系の変数に任せています。'''
        cls._key_z_duration = (cls._key_z_duration+1)*pressed_keys[K_z]
        if cls._key_z_duration == 1 and cls.is_diffusion():
            for angle in cls.DIFFUSION_ANGLE_RANGE:
                bullets.append(Bullet(x=x, y=y-50, angle=angle, hldgs=bullets))
            SE_BARRAGE.play()
            cls.consume_diffusion()
