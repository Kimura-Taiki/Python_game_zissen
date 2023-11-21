import pygame
from typing import Optional, Final
from math import sin, radians

from mod.const import WX, WY, BOARD, BOARD_H, BOARD_W, BOARD_UD, \
    BOARD_LEFT_OBJECT, BOARD_RIGHT_OBJECT, Y_AT_0_DEGREES, PNG_BG, CLEN, DATA_LR, DATA_UD, IMG_BG

class Course():
    '''レースで使うコース情報を保持するクラスです。'''
    def __init__(self, img_bg: pygame.surface.Surface, cmax: int, curve: list[float], updown: list[float],
                 object_left: Optional[list[int]]=None, object_right: Optional[list[int]]=None) -> None:
        self.IMG_BG: Final = img_bg
        '''pygame.surface.Surface : コースの背景の複製元となる面です。'''
        self.CMAX: Final = cmax
        '''コースの全長、板の枚数で定義されています。１周するとまた最初から数えます。'''
        self.CURVE: Final = curve
        '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
        self.UPDOWN: Final = updown
        '''コースの該当地点での仰角です。実際に描画する際には視点位置からの仰角積分を使います。'''
        self.object_left: Final = object_left if object_left else [0]*cmax
        '''コース左側に置いてある設置物番号です。インデックス値はスタート地点からの距離を示しています。'''
        self.object_right: Final = object_right if object_right else [0]*cmax
        '''コース右側に置いてある設置物番号です。インデックス値はスタート地点からの距離を示しています。'''

    def both_curve_lists(self, car_y: int) -> tuple[list[float], list[float]]:
        '''板の上辺の左右のX座標を入れたリストを返します。(左X座標リスト, 右X座標リスト)の順番で返します。'''
        _sum_curve = 0.0
        curvature_integral = [(_sum_curve := _sum_curve+self.CURVE[(car_y+i) % self.CMAX]/2) for i in range(BOARD)]
        lx_list: list[float] = [WX/2-BOARD_W[i]/2+curvature_integral[i] for i in range(BOARD)]
        rx_list: list[float] = [WX/2+BOARD_W[i]/2+curvature_integral[i] for i in range(BOARD)]
        return lx_list, rx_list
    
    def both_updown_lists(self, car_y: int) -> tuple[list[float], int]:
        '''板の上辺のY座標を入れたリストと板の描画を開始する地平線のY座標を返します。(Y座標リスト, 地平線)の順番で返します。'''
        ud: float = 0.0
        board_ud: list[float] = [(ud := ud+self.UPDOWN[(car_y+i) % self.CMAX])/30 for i in range(BOARD)]
        horizon: int = Y_AT_0_DEGREES+int(sum(self.UPDOWN[(car_y+i) % self.CMAX] for i in range(BOARD))/3)
        sy: float = float(horizon)
        board_by: list[float] = [(sy := sy+BOARD_H[BOARD-1-i]*(WY-horizon)/200)-BOARD_UD[BOARD-1-i]*board_ud[BOARD-1-i] for i in range(BOARD)][::-1]
        return board_by, horizon


    @classmethod
    def updown_course(cls) -> 'Course':
        '''list1003_1.pyで用いられているアップダウンのみのコースを返す関数です。'''
        return Course(img_bg=pygame.image.load(PNG_BG).convert(), cmax=480,
                      curve=[0.0 for _ in range(480)],
                      updown=[5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)])

    @classmethod
    def lr_list_course(cls) -> 'Course':
        '''list1006_1.pyで用いられているDATA_LRからコースを生成する関数です。
        DATA_LRで示される各値を曲率の極値として、隣接極値間では一次関数で補完します。
        各極値間はBOARD枚分の距離があります。'''
        return Course(img_bg=pygame.image.load(PNG_BG), cmax=BOARD*CLEN,
                      curve=[DATA_LR[i]*(BOARD-j)/BOARD+DATA_LR[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      updown=[0.0 for _ in range(BOARD*CLEN)])
    
    @classmethod
    def lrud_list_course(cls) -> 'Course':
        '''list1007_1.pyで用いられているDATA_LRとDATA_UDからコースを生成する関数です。
        DATA_LRを曲率の極値として、DATA_UDを仰角の極値として、隣接極値間では一次関数で補完します。
        各極値間はBOARD枚分の距離があります。'''
        return Course(img_bg=pygame.image.load(PNG_BG), cmax=BOARD*CLEN,
                      curve=[DATA_LR[i]*(BOARD-j)/BOARD+DATA_LR[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      updown=[DATA_UD[i]*(BOARD-j)/BOARD+DATA_UD[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)])
    
    @classmethod
    def obj_list_course(cls) -> 'Course':
        '''list1008_1.pyで用いられている設置物付きのコースを生成する関数です。
        設置物の配置は定数から取り出します。'''
        return Course(img_bg=IMG_BG, cmax=BOARD*CLEN,
                      curve=[DATA_LR[i]*(BOARD-j)/BOARD+DATA_LR[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      updown=[DATA_UD[i]*(BOARD-j)/BOARD+DATA_UD[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      object_left=BOARD_LEFT_OBJECT,
                      object_right=BOARD_RIGHT_OBJECT)


