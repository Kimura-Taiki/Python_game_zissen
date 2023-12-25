import pygame
from typing import Final, Optional
from pygame import Color
from math import sin, radians

BOARD: Final = 120
'''描画する板の枚数'''

WX: Final = 800
'''ウィンドウのX幅'''
WY: Final = 600
'''ウィンドウのY幅'''

# 道路の板の基本形状を計算
BOARD_W: Final = [10 + (BOARD - i) ** 2 / 12 for i in range(BOARD)]
'''板の横幅です。0が手前、BOARD-1が最遠です。'''

BOARD_H: Final = [3.4 * (BOARD - i) / BOARD for i in range(BOARD)]
'''板の縦幅です。0が手前、BOARD-1が最遠です。'''

BOARD_UD: Final = [2*sin(radians(i*1.5)) for i in range(BOARD)]
'''板の起伏です。0が手前、BOARD-1が最遠です。正弦曲線の半周期×2に相当します。'''

# DATA_LR: Final = [0, 0, 0, 0, 0, 0, 0, 0, 0]
DATA_LR: Final = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0,-2,-2,-4,-4,-2,-1, 0, 0, 0, 0, 0, 0, 0]
'''コースのBOARD枚毎の極値曲率です。曲率は各極値から次の極値へ一次関数的に遷移します。'''

# DATA_UD: Final = [0,-2,-4,-6,-4,-2, 2, 4, 2]
DATA_UD: Final = [0, 0, 1, 2, 3, 2, 1, 0,-2,-4,-2, 0, 0, 0, 0, 0,-1,-2,-3,-4,-3,-2,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-3, 3, 0,-6, 6, 0]
'''コースのBOARD枚毎の極値仰角です。仰角は各極値から次の極値へ一次関数的に遷移します。'''

CLEN: Final = len(DATA_LR)
'''len(DATA_LR)です。'''

NO_OBJECT: Final = 0
'''オブジェクトが無い事を示すオブジェクト番号です。'''
OBJECT_BIKINI_BILLBOARD: Final = 1
'''ビキニ広告看板のオブジェクト番号です。'''
OBJECT_PALM_TREE: Final = 2
'''椰子の木のオブジェクト番号です。'''
OBJECT_YACHT: Final = 3
'''ヨットのオブジェクト番号です。'''
OBJECT_SEA: Final = 9
'''海岸のオブジェクト番号です。'''

BOARD_LEFT_OBJECT: Final = [OBJECT_SEA if j % 12 == 6 else
                            OBJECT_YACHT if (j % 20 == 0) and (i % 8 < 7) else
                            OBJECT_PALM_TREE if (j % 12 == 0) and(i % 8 < 7) else
                            NO_OBJECT for i in range(CLEN) for j in range(BOARD)]
# BOARD_LEFT_OBJECT: Final = [OBJECT_SEA if i % 12 == 6 else
#                             OBJECT_YACHT if (i % 20 == 0) else
#                             OBJECT_PALM_TREE if i % 12 == 0 else
#                             NO_OBJECT for i in range(CLEN*BOARD)]

'''コース左側の設置物設定です。インデックス値はスタート地点からの距離を示しています。'''
BOARD_RIGHT_OBJECT: Final = [OBJECT_BIKINI_BILLBOARD if j == 60 else NO_OBJECT for i in range(CLEN) for j in range(BOARD)]
'''コース右側の設置物設定です。インデックス値はスタート地点からの距離を示しています。'''

Y_AT_0_DEGREES: Final = 400
'''コースの仰角積分が0度の時の地平線のY座標です。'''
SEA_BLIT_X_OFFSET: Final = -780
'''海岸線画像を描画する際のオフセット値です。'''

FRAMES_PER_SECOND: Final = 60
'''秒間更新回数です。'''

O1ST_QUARTER: Final = 120
'''コースの第１四半距離です。'''
O2ND_QUARTER: Final = 240
'''コースの第２四半距離です。'''
O3RD_QUARTER: Final = 360
'''コースの第３四半距離です。'''
O4TH_QUARTER: Final = 480
'''コースの第４四半距離です。'''

RED: Final[Color] = Color(255, 0, 0)
'''#FF0000'''
GREEN: Final[Color] = Color(0, 128, 0)
'''#008000'''
BLUE: Final[Color] = Color(0, 0, 255)
'''#0000FF'''
BLACK: Final[Color] = Color(0, 0, 0)
'''#000000'''
WHITE: Final[Color] = Color(255, 255, 255)
'''#FFFFFF'''
GRAY: Final[Color] = Color(160, 160, 160)
'''#A0A0A0'''
SEA_BLUE: Final[Color] = Color(0, 56, 255)
'''#0038FF'''
YELLOW: Final[Color] = Color(255, 224, 0)
'''#FFE000'''

pygame.init()
pygame.display.set_caption("")
_scr = pygame.display.set_mode((WX, WY))

PNG_BG: Final[str] = "image_pr/bg.png"
'''ゲーム背景の画像アドレス'''
IMG_BG: Final = pygame.image.load("image_pr/bg.png").convert()
'''Surface化済みの背景画像の原板です。'''
IMG_SEA: Final = pygame.image.load("image_pr/sea.png").convert_alpha()
'''Surface化済みの海岸画像の原板です。'''
IMG_OBJ: Final[list[pygame.surface.Surface]] = [
    pygame.image.load("image_pr/car03.png").convert_alpha(),
    pygame.image.load("image_pr/board.png").convert_alpha(),
    pygame.image.load("image_pr/yashi.png").convert_alpha(),
    pygame.image.load("image_pr/yacht.png").convert_alpha()]
'''Surface化済みのオブジェクト画像の原板です。'''
IMG_CAR = [
    pygame.image.load("image_pr/car00.png").convert_alpha(),
    pygame.image.load("image_pr/car01.png").convert_alpha(),
    pygame.image.load("image_pr/car02.png").convert_alpha(),
    pygame.image.load("image_pr/car03.png").convert_alpha(),
    pygame.image.load("image_pr/car04.png").convert_alpha(),
    pygame.image.load("image_pr/car05.png").convert_alpha(),
    pygame.image.load("image_pr/car06.png").convert_alpha(),
]
'''Surface化済みの車画像の原板です。'''

CAR: Final = 30
'''レースに参加する車の最大数です。'''
PLCAR_Y: Final = 10
'''プレイヤーの車を表示する位置を修正する値です。
スタート地点から現在地までの板の枚数(Car.y)に加算しています。
つまり、Car.yより奥の地点で車を描画する様にしています。'''
