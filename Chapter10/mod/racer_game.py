import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable, Final, Optional
from mod.const import *
from mod.course import Course


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


def draw_obj(surface: pygame.surface.Surface, img: pygame.surface.Surface, x: int | float, y: int | float, scale: float) -> None:
    img_rz = pygame.transform.rotozoom(surface=img, angle=0, scale=scale)
    surface.blit(source=img_rz, dest=[x-img_rz.get_width()/2, y-img_rz.get_height()])


class RacerGame():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Python Racer")
        self.screen = pygame.display.set_mode((WX, WY))
        '''pygame.surface.Surface : ゲーム画面となるウィンドウです。この面はゲーム内の描画に使用されます。'''
        self.clock = pygame.time.Clock()
        '''pygame.time.Clock : ゲームループのフレームレートを制御するためのClockインスタンスです。
        このクロックは主に `Clock.tick` メソッドを使用して一定のフレームレートを維持します。'''
        self.COURSE = Course.obj_list_course()
        '''現在走っているコースです。変更を想定していないので現時点では定数です。
        本来ならRacerGameインスタンス生成時に注入すべき値ですが、今回は面倒なので直埋めします。'''
        self.car_y = 0
        '''コース上でのスタート地点からの距離を板の枚数で指定しています。'''
        self.vertical = 0.0
        '''背景の横方向の位置を管理する変数'''

    def _move_forward(self) -> None:
        '''_move_forward: 車を前進させ、背景の横方向の位置を更新します。'''
        self.car_y = self._mod_car_y(dy=1)
        self.vertical = (self.vertical-sum(self.COURSE.CURVE[self._mod_car_y(dy=i)] for i in range(BOARD))/30+WX) % WX

    def mainloop(self) -> None:
        process_input_events(move_forward=self._move_forward)

        board_lx, board_rx = self.COURSE.both_curve_lists(car_y=self.car_y)
        board_by, horizon = self.COURSE.both_updown_lists(car_y=self.car_y)

        # 描画部分
        draw = Draw(screen=self.screen, lxf=lambda i: board_lx[i], rxf=lambda i: board_rx[i], yf=lambda i: board_by[i])
        draw.draw_background(img_bg=self.COURSE.IMG_BG, vertical_x=self.vertical,
                             sea_x=int(board_lx[BOARD-1]+SEA_BLIT_X_OFFSET), horizon_y=horizon)
        for i in range(BOARD-1, 0, -1):
            draw.draw_board_section(i=i, car_y=self.car_y, cmax=self.COURSE.CMAX)

        pygame.display.update()
        self.clock.tick(60)

    def _mod_car_y(self, dy: int) -> int:
        '''car_yをコース全長で循環させる処理をこの関数で統一して字数も減らします。'''
        return (self.car_y+dy) % self.COURSE.CMAX


class Draw():
    def __init__(self, screen: pygame.surface.Surface, lxf: Callable[[int], float], rxf: Callable[[int], float],
                 yf: Callable[[int], float]) -> None:
        self.screen = screen
        '''描画先です。'''
        self.lxf = lxf
        self.rxf = rxf
        self.yf = yf
        self.idx002 = self._internal_division(ratio=0.02)
        self.idx098 = self._internal_division(ratio=0.98)
        self.idx024 = self._internal_division(ratio=0.24)
        self.idx026 = self._internal_division(ratio=0.26)
        self.idx049 = self._internal_division(ratio=0.49)
        self.idx051 = self._internal_division(ratio=0.51)
        self.idx074 = self._internal_division(ratio=0.74)
        self.idx076 = self._internal_division(ratio=0.76)
        self.idxm05 = self._internal_division(ratio=-0.05)
        self.idxm50 = self._internal_division(ratio=-0.50)
        self.idx130 = self._internal_division(ratio=1.30)

    def draw_background(self, img_bg: pygame.surface.Surface, vertical_x: int, sea_x: int, horizon_y: int) -> None:
        '''背景部分を描画する命令です。道路や設置物は連続的なので_draw_board_section命令の繰り返しで描画しています。'''
        self.screen.fill(color=SEA_BLUE)
        self.screen.blit(img_bg, [vertical_x-WX, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(img_bg, [vertical_x, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(source=IMG_SEA, dest=[sea_x, horizon_y])

    def draw_board_section(self, i: int, car_y: int, cmax: int) -> None:
        '''板番号i,上辺の左X座標関数lxf,上辺の右座標関数rxf,上辺の幅関数wxf,上辺のY座標関数yfから板の存在する面全域を描画する命令です。
        描画対象には道路と設置物があります。'''
        self._draw_trapezoid(color=trapezoid_color(course_point=car_y+i), i=i, lf=self.lxf, rf=self.rxf, bf=self.yf)
        if int(car_y+i) % 10 <= 4:
            self._draw_yellow_line(i=i)
        if int(car_y+i) % 20 <= 10:
            self._draw_white_line(i=i)
        self._draw_object(i=i, car_y=car_y, cmax=cmax)

    def _draw_trapezoid(self, color: pygame.Color, i: int,
                        lf: Callable[[int], float], rf: Callable[[int], float], bf: Callable[[int], float]) -> None:
        '''色color,板番号i,上辺の左X座標関数lf,上辺の右座標関数rf,上辺のY座標関数bfから台形を描画する命令です。'''
        pygame.draw.polygon(surface=self.screen, color=color,
                            points=[[lf(i), bf(i)], [rf(i), bf(i)], [rf(i-1), bf(i-1)], [lf(i-1), bf(i-1)]])

    def _internal_division(self, ratio: float) -> Callable[[int], float]:
        return lambda i: self.lxf(i)*(1.0-ratio)+self.rxf(i)*ratio

    def _draw_yellow_line(self, i: int) -> None:
        '''道路脇の黄線を描画します。'''
        self._draw_trapezoid(color=YELLOW, i=i, lf=self.lxf, rf=self.idx002, bf=self.yf)
        self._draw_trapezoid(color=YELLOW, i=i, lf=self.idx098, rf=self.rxf, bf=self.yf)

    def _draw_white_line(self, i: int) -> None:
        '''道路の白線を描画します。'''
        self._draw_trapezoid(color=WHITE, i=i, lf=self.idx024, rf=self.idx026, bf=self.yf)
        self._draw_trapezoid(color=WHITE, i=i, lf=self.idx049, rf=self.idx051, bf=self.yf)
        self._draw_trapezoid(color=WHITE, i=i, lf=self.idx074, rf=self.idx076, bf=self.yf)

    def _draw_object(self, i: int, car_y: int, cmax: int) -> None:
        '''設置物を描画します。'''
        scale = 1.5 * BOARD_W[i] / BOARD_W[0]
        mod_car_y = (car_y+i) % cmax
        obj_l = BOARD_LEFT_OBJECT[mod_car_y]
        if obj_l == OBJECT_PALM_TREE:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_l], x=self.idxm05(i), y=self.yf(i), scale=scale)
        if obj_l == OBJECT_YACHT:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_l], x=self.idxm50(i), y=self.yf(i), scale=scale)
        if obj_l == OBJECT_SEA:
            self.screen.blit(source=IMG_SEA, dest=[self.idxm50(i) + SEA_BLIT_X_OFFSET, self.yf(i)])
        obj_r = BOARD_RIGHT_OBJECT[mod_car_y]
        if obj_r == OBJECT_BIKINI_BILLBOARD:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_r], x=self.idx130(i), y=self.yf(i), scale=scale)

