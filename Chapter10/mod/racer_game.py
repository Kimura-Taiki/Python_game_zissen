import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable, Final, Optional, NamedTuple
from mod.const import *
from mod.course import Course
from mod.draw import Draw


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


def draw_shadow(bg, x, y, siz):
    shadow = pygame.Surface([siz, siz/4])
    shadow.fill(RED)
    shadow.set_colorkey(RED) # Surfaceの透過色を設定
    shadow.set_alpha(128) # Surfaceの透明度を設定
    pygame.draw.ellipse(shadow, BLACK, [0,0,siz,siz/4])
    bg.blit(shadow, [x-siz/2, y-siz/4])


def drive_car(key): # プレイヤーの車の操作、制御
    if key[K_LEFT] == 1:
        if car_lr[0] > -3:
            car_lr[0] -= 1
        car_x[0] = car_x[0] + (car_lr[0]-3)*car_spd[0]/100 - 5
    elif key[K_RIGHT] == 1:
        if car_lr[0] < 3:
            car_lr[0] += 1
        car_x[0] = car_x[0] + (car_lr[0]+3)*car_spd[0]/100 + 5
    else:
        car_lr[0] = int(car_lr[0]*0.9)

    if key[K_a] == 1: # アクセル
        car_spd[0] += 3
    elif key[K_z] == 1: # ブレーキ
        car_spd[0] -= 10
    else:
        car_spd[0] -= 0.25

    if car_spd[0] < 0:
        car_spd[0] = 0
    if car_spd[0] > 320:
        car_spd[0] = 320

    car_x[0] -= car_spd[0]*curve[int(car_y[0]+PLCAR_Y)%CMAX]/50
    if car_x[0] < 0:
        car_x[0] = 0
        car_spd[0] *= 0.9
    if car_x[0] > 800:
        car_x[0] = 800
        car_spd[0] *= 0.9

    car_y[0] = car_y[0] + car_spd[0]/100
    if car_y[0] > CMAX-1:
        car_y[0] -= CMAX


class Car():
    def __init__(self, x: float=0.0, y: int=0, yaw: int=0, speed: float=0.0) -> None:
        self.x = x
        '''float型:コース上のX位置です。大体0で左端、WXで右端です。'''
        self.y = y
        '''int型:コース上でのスタート地点からの距離を板の枚数で指定しています。'''
        self.yaw = yaw
        self._speed = speed

    def handle(self, handle: int) -> None:
        if handle < 0:
            if self.yaw > -3:
                self.yaw -= 1
            self.x += (self.yaw-3)*self.speed/100-5
        elif handle > 0:
            if self.yaw < 3:
                self.yaw += 1
            self.x += (self.yaw+3)*self.speed/100+5
        else:
            self.yaw = int(self.yaw*0.9)

    def accele(self, accele: int) -> None:
        if accele > 0:
            self.speed += 3
        elif accele < 0:
            self.speed -= 10
        else:
            self.speed -= 0.25

    def elapse(self, course: Course) -> None:
        self.x -= self.speed*course.CURVE[int(self.y+PLCAR_Y) % course.CMAX]/50
        if self.x < 0:
            self.x = 0
            self.speed *= 0.9
        if self.x > WX:
            self.y = WX
            self.speed *= 0.9
        self.y = (self.y+int(self.speed/100)) % course.CMAX

    @property
    def speed(self)  -> float:
        return self._speed

    @speed.setter
    def speed(self, value: int|float) -> float:
        return 0 if value < 0 else (value if value < 320 else 320)

print(Car().speed)