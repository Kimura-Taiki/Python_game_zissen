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


# class RacerGame():
#     pygame.init()
#     pygame.display.set_caption("Python Racer")
#     screen = pygame.display.set_mode((WX, WY))
#     '''pygame.surface.Surface : ゲーム画面となるウィンドウです。'''
#     clock = pygame.time.Clock()
#     '''pygame.time.Clock : Clock.tick命令用に抱えているClockインスタンスです。'''
#     IMG_BG = pygame.image.load(PNG_BG).convert()

#     CURVE = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]
#     '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
#     CMAX = len(CURVE)
#     '''コースの全長、板の枚数で定義されている。１周するとまた最初から数える。'''
#     car_y = 0
#     '''コース上でのスタート地点からの距離を板の枚数で指定しています。'''




def main() -> None: # メイン処理
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen = pygame.display.set_mode((WX, WY))
    clock = pygame.time.Clock()
    IMG_BG = pygame.image.load(PNG_BG).convert()
    curve = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]
    '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
    CMAX = len(curve)
    '''コースの全長、板の枚数で定義されている。１周するとまた最初から数える。'''
    car_y = 0
    '''コース上でのスタート地点からの距離を板の枚数で指定しています。'''

    while True:
        def move_forward() -> None:
            nonlocal car_y, CMAX
            car_y = (car_y+1) % CMAX
        process_input_events(move_forward=move_forward)

        di: float = 0.0
        board_lx: list[float] = [WX/2-BOARD_W[i]/2+(di := di+curve[(car_y+i) % CMAX])/2 for i in range(BOARD)]
        di: float = 0.0
        board_rx: list[float] = [WX/2+BOARD_W[i]/2+(di := di+curve[(car_y+i) % CMAX])/2 for i in range(BOARD)]

        screen.blit(IMG_BG, [0, 0])

        # 描画用データをもとに道路を描く
        for i in range(BOARD-1, 0, -1):
            pygame.draw.polygon(surface=screen, color=trapezoid_color(course_point=car_y+i),
                                points=[[board_lx[i  ], BOARD_BY[i  ]], [board_rx[i  ], BOARD_BY[i  ]],
                                        [board_rx[i-1], BOARD_BY[i-1]], [board_lx[i-1], BOARD_BY[i-1]]])

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
