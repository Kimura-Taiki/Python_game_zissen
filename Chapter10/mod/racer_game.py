import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable, Final, Optional, NamedTuple
from mod.const import *
from mod.course import Course
from mod.draw import Draw
from mod.car import Car


def process_input_events(move_forward: Callable[[], None]) -> None:
    '''キー入力に対応した処理を行います。実処理は関数として注入してもらいます。'''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    key = pygame.key.get_pressed()
    if key[K_UP]:
        move_forward()


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

    def _mod_car_y(self, dy: int) -> int:
        '''car_yをコース全長で循環させる処理をこの関数で統一して字数も減らします。'''
        return (self.car_y+dy) % self.COURSE.CMAX

    def _move_forward(self) -> None:
        '''車を前進させ、背景の横方向の位置を更新します。'''
        self.car_y = self._mod_car_y(dy=1)
        self.vertical = (self.vertical - sum(self.COURSE.CURVE[self._mod_car_y(dy=i)] for i in range(BOARD)) / 30 + WX) % WX

    def _update_board_lists(self) -> tuple[list[float], list[float], list[float], int]:
        '''コースの左右の板のリストと水平線の位置を更新します。'''
        board_lx, board_rx = self.COURSE.both_curve_lists(car_y=self.car_y)
        board_by, horizon = self.COURSE.both_updown_lists(car_y=self.car_y)
        return board_lx, board_rx, board_by, horizon

    def _draw_game_screen(self, board_lx: list[float], board_rx: list[float], board_by: list[float], horizon: int) -> None:
        '''ゲーム画面を描画します。'''
        draw = Draw(screen=self.screen, lxf=lambda i: board_lx[i], rxf=lambda i: board_rx[i], yf=lambda i: board_by[i])
        draw.draw_background(img_bg=self.COURSE.IMG_BG, vertical_x=int(self.vertical),
                             sea_x=int(board_lx[BOARD-1] + SEA_BLIT_X_OFFSET), horizon_y=horizon)
        for i in range(BOARD-1, 0, -1):
            draw.draw_board_section(i=i, car_y=self.car_y, cmax=self.COURSE.CMAX)

    def mainloop(self) -> None:
        process_input_events(move_forward=self._move_forward)
        board_lx, board_rx, board_by, horizon = self._update_board_lists()
        self._draw_game_screen(board_lx, board_rx, board_by, horizon)
        pygame.display.update()
        self.clock.tick(FRAMES_PER_SECOND)


def draw_shadow(bg: pygame.surface.Surface, x: int, y: int, size: int):
    shadow = pygame.Surface([size, size/4])
    shadow.fill(RED)
    shadow.set_colorkey(RED) # Surfaceの透過色を設定
    shadow.set_alpha(128) # Surfaceの透明度を設定
    pygame.draw.ellipse(shadow, BLACK, [0, 0, size, size/4])
    bg.blit(shadow, [x-size/2, y-size/4])


def draw_obj(bg: pygame.surface.Surface, img: pygame.surface.Surface, x: int, y: int, scale: float):
    img_rz = pygame.transform.rotozoom(img, 0, scale)
    w = img_rz.get_width()
    h = img_rz.get_height()
    bg.blit(img_rz, [x-w/2, y-h])


