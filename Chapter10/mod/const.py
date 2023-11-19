from typing import Final
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

Y_AT_0_DEGREES: Final = 400

# di: float
# di = 400.0
# BOARD_BY: Final[
#   list[float]] = [(di := di + 3.4 * i / BOARD) for i in range(BOARD)][::-1]
# '''板の描画Y座標です。0が手前、BOARD-1が最遠です。'''

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

PNG_BG: Final[str] = "image_pr/bg.png"
'''ゲーム背景の画像アドレス'''
