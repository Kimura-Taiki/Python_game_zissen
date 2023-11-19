import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable, Final
from mod.const import *


def process_input_events(move_forward: Callable[[], None]) -> None:
    '''キー入力に対応した処理を行います。実処理は関数として注入してもらいます。'''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()
    if key[K_UP]:
        move_forward()


def trapezoid_color(course_point: int) -> pygame.Color:
    '''道路ポリゴンの色を作ります。スタートからの絶対距離で色分けします。'''
    if course_point == O1ST_QUARTER: return RED
    elif course_point == O2ND_QUARTER: return GREEN
    elif course_point == O3RD_QUARTER: return BLUE
    elif course_point == O4TH_QUARTER: return BLACK
    elif course_point%12 == 0: return WHITE
    return GRAY


class Course():
    '''レースで使うコース情報を保持するクラスです。'''
    def __init__(self, img_bg: pygame.surface.Surface, cmax: int, curve: list[float], updown: list[float]) -> None:
        self.IMG_BG: Final = img_bg
        '''pygame.surface.Surface : コースの背景の複製元となる面です。'''
        self.CMAX: Final = cmax
        '''コースの全長、板の枚数で定義されています。１周するとまた最初から数えます。'''
        self.CURVE: Final = curve
        '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
        self.UPDOWN: Final = updown
        '''コースの該当地点での仰角です。実際に描画する際には視点位置からの仰角積分を使います。'''

    @classmethod
    def updown_course(cls) -> 'Course':
        '''list1003_1.pyで用いられているアップダウンのみのコースを返す関数です。'''
        return Course(img_bg=pygame.image.load(PNG_BG).convert(), cmax=480,
                      curve=[0.0 for _ in range(480)],
                      updown=[5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)])


class RacerGame():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Python Racer")
        self.screen = pygame.display.set_mode((WX, WY))
        '''pygame.surface.Surface : ゲーム画面となるウィンドウです。この面はゲーム内の描画に使用されます。'''
        self.clock = pygame.time.Clock()
        '''pygame.time.Clock : ゲームループのフレームレートを制御するためのClockインスタンスです。
        このクロックは主に `Clock.tick` メソッドを使用して一定のフレームレートを維持します。'''
        self.IMG_BG = pygame.image.load(PNG_BG).convert()
        '''pygame.surface.Surface : 背景の複製元となる面です。'''
        # self.CURVE = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]
        # '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
        self.CURVE = [0.0 for i in range(480)]
        '''コースの該当地点での曲率です。今回は直線コースなので、曲率は常時0です。'''
        self.UPDOWN = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]
        '''コースの該当地点での仰角です。実際に描画する際には視点位置からの仰角積分を使います。'''
        self.CMAX = len(self.CURVE)
        '''コースの全長、板の枚数で定義されている。１周するとまた最初から数える。'''
        self.car_y = 0
        '''コース上でのスタート地点からの距離を板の枚数で指定しています。'''
        self.vertical = 0.0
        '''背景の横方向の位置を管理する変数'''

    def _move_forward(self) -> None:
        '''_move_forward: 車を前進させ、背景の横方向の位置を更新します。'''
        self.car_y = (self.car_y+1) % self.CMAX
        self.vertical = (self.vertical-sum(self.CURVE[(self.car_y+i) % self.CMAX] for i in range(BOARD))/30+WX) % WX

    def mainloop(self) -> None:
        process_input_events(move_forward=self._move_forward)

        di1: float = 0.0
        board_lx: list[float] = [WX/2-BOARD_W[i]/2+(di1 := di1+self.CURVE[(self.car_y+i) % self.CMAX])/2 for i in range(BOARD)]
        di2: float = 0.0
        board_rx: list[float] = [WX/2+BOARD_W[i]/2+(di2 := di2+self.CURVE[(self.car_y+i) % self.CMAX])/2 for i in range(BOARD)]
        ud: float = 0.0
        board_ud: list[float] = [(ud := ud+self.UPDOWN[(self.car_y+i) % self.CMAX])/30 for i in range(BOARD)]
        horizon: int = Y_AT_0_DEGREES+int(sum(self.UPDOWN[(self.car_y+i) % self.CMAX] for i in range(BOARD))/3)
        sy: float = float(horizon)
        board_by: list[float] = [(sy := sy+BOARD_H[BOARD-1-i]*(WY-horizon)/200)-BOARD_UD[BOARD-1-i]*board_ud[BOARD-1-i] for i in range(BOARD)][::-1]

        self.screen.fill(color=SEA_BLUE)
        self.screen.blit(self.IMG_BG, [self.vertical-WX, horizon-Y_AT_0_DEGREES])
        self.screen.blit(self.IMG_BG, [self.vertical, horizon-Y_AT_0_DEGREES])

        # 描画用データをもとに道路を描く
        for i in range(BOARD-1, 0, -1):
            pygame.draw.polygon(surface=self.screen, color=trapezoid_color(course_point=self.car_y+i),
                                points=[[board_lx[i  ], board_by[i  ]], [board_rx[i  ], board_by[i  ]],
                                        [board_rx[i-1], board_by[i-1]], [board_lx[i-1], board_by[i-1]]])
                                # points=[[board_lx[i  ], BOARD_BY[i  ]], [board_rx[i  ], BOARD_BY[i  ]],
                                #         [board_rx[i-1], BOARD_BY[i-1]], [board_lx[i-1], BOARD_BY[i-1]]])

        pygame.display.update()
        self.clock.tick(60)
