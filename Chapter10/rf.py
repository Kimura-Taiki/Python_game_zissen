import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable
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
        self.CURVE = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]
        '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
        self.CMAX = len(self.CURVE)
        '''コースの全長、板の枚数で定義されている。１周するとまた最初から数える。'''
        self.car_y = 0
        '''コース上でのスタート地点からの距離を板の枚数で指定しています。'''

    def _move_forward(self) -> None:
        self.car_y = (self.car_y+1) % self.CMAX

    def mainloop(self) -> None:
        process_input_events(move_forward=self._move_forward)

        di1: float = 0.0
        board_lx: list[float] = [WX/2-BOARD_W[i]/2+(di1 := di1+self.CURVE[(self.car_y+i) % self.CMAX])/2 for i in range(BOARD)]
        di2: float = 0.0
        board_rx: list[float] = [WX/2+BOARD_W[i]/2+(di2 := di2+self.CURVE[(self.car_y+i) % self.CMAX])/2 for i in range(BOARD)]

        self.screen.blit(self.IMG_BG, [0, 0])

        # 描画用データをもとに道路を描く
        for i in range(BOARD-1, 0, -1):
            pygame.draw.polygon(surface=self.screen, color=trapezoid_color(course_point=self.car_y+i),
                                points=[[board_lx[i  ], BOARD_BY[i  ]], [board_rx[i  ], BOARD_BY[i  ]],
                                        [board_rx[i-1], BOARD_BY[i-1]], [board_lx[i-1], BOARD_BY[i-1]]])

        pygame.display.update()
        self.clock.tick(60)

def main() -> None:
    '''メイン処理'''
    game = RacerGame()
    while True:
        game.mainloop()


if __name__ == '__main__':
    main()
