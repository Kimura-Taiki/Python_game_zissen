import pygame
from typing import Callable, Optional, NamedTuple

from mod.const import BOARD_W, BOARD_LEFT_OBJECT, BOARD_RIGHT_OBJECT, Y_AT_0_DEGREES, WX, SEA_BLIT_X_OFFSET, \
    IMG_OBJ, IMG_SEA, OBJECT_BIKINI_BILLBOARD, OBJECT_PALM_TREE, OBJECT_YACHT, OBJECT_SEA, \
    YELLOW, WHITE, SEA_BLUE, RED, GREEN, BLUE, BLACK, GRAY, O1ST_QUARTER, O2ND_QUARTER, O3RD_QUARTER, O4TH_QUARTER
from mod.car import Car

def trapezoid_color(course_point: int) -> pygame.Color:
    '''道路ポリゴンの色を作ります。スタートからの絶対距離で色分けします。'''
    if course_point == O1ST_QUARTER: return RED
    elif course_point == O2ND_QUARTER: return GREEN
    elif course_point == O3RD_QUARTER: return BLUE
    elif course_point == O4TH_QUARTER: return BLACK
    elif course_point%12 == 0: return WHITE
    return GRAY


def draw_obj(surface: pygame.surface.Surface, img: pygame.surface.Surface, x: int | float, y: int | float, scale: float) -> Optional[bool]:
    img_rz = pygame.transform.rotozoom(surface=img, angle=0, scale=scale)
    surface.blit(source=img_rz, dest=[x-img_rz.get_width()/2, y-img_rz.get_height()])
    return None


def draw_shadow(surface: pygame.surface.Surface, x: int | float, y: int | float, size: int | float) -> None:
    shadow = pygame.Surface([size, size/4])
    shadow.fill(RED)
    shadow.set_colorkey(RED) # Surfaceの透過色を設定
    shadow.set_alpha(128) # Surfaceの透明度を設定
    pygame.draw.ellipse(shadow, BLACK, [0, 0, size, size/4])
    surface.blit(shadow, [x-size/2, y-size/4])


class Draw():
    def __init__(self, screen: pygame.surface.Surface, lxf: Callable[[int], float], rxf: Callable[[int], float],
                 yf: Callable[[int], float]) -> None:
        self.screen = screen
        '''描画先です。'''
        self.lxf = lxf
        self.rxf = rxf
        self.yf = yf
        [self.idx002, self.idx098, self.idx024, self.idx026, self.idx049, self.idx051, self.idx074, self.idx076,
         self.idxm05, self.idxm50, self.idx130] = [
             self._internal_division(ratio=value) for value in [0.02, 0.98, 0.24, 0.26, 0.49, 0.51, 0.74, 0.76, -0.05, -0.50, 1.30]]
        self.yellow_tz = [self._TZ(YELLOW, self.lxf, self.idx002), self._TZ(YELLOW,  self.idx098, self.rxf)]
        self.white_tz = [self._TZ(WHITE, self.idx024, self.idx026), self._TZ(WHITE,  self.idx049, self.idx051),
                         self._TZ(WHITE, self.idx074, self.idx076)]

    def draw_background(self, img_bg: pygame.surface.Surface, vertical_x: int, sea_x: int, horizon_y: int) -> None:
        '''背景部分を描画する命令です。道路や設置物は連続的なので_draw_board_section命令の繰り返しで描画しています。'''
        self.screen.fill(color=SEA_BLUE)
        self.screen.blit(source=img_bg, dest=[vertical_x-WX, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(source=img_bg, dest=[vertical_x, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(source=IMG_SEA, dest=[sea_x, horizon_y])

    class _TZ(NamedTuple):
        '''下記のdraw_board_section命令中に_draw_trapezoid命令を走査する際にmypyでエラーを起こさない為のクラスです。'''
        color: pygame.Color; lxf: Callable[[int], float]; rxf: Callable[[int], float]

    def draw_board_section(self, i: int, car_y: int, cmax: int) -> None:
        '''板番号i,上辺の左X座標関数lxf,上辺の右座標関数rxf,上辺の幅関数wxf,上辺のY座標関数yfから板の存在する面全域を描画する命令です。
        描画対象には道路と設置物があります。'''
        self._draw_trapezoid(color=trapezoid_color(course_point=car_y+i), i=i, lf=self.lxf, rf=self.rxf, bf=self.yf)
        if int(car_y+i) % 10 <= 4:
            [self._draw_trapezoid(color=j.color, i=i, lf=j.lxf, rf=j.rxf, bf=self.yf) for j in self.yellow_tz]
        if int(car_y+i) % 20 <= 10:
            [self._draw_trapezoid(color=j.color, i=i, lf=j.lxf, rf=j.rxf, bf=self.yf) for j in self.white_tz]
        self._draw_object(i=i, car_y=car_y, cmax=cmax)

    def _draw_trapezoid(self, color: pygame.Color, i: int, lf: Callable[[int], float], rf: Callable[[int], float],
                        bf: Callable[[int], float]) -> Optional[bool]:
        '''色color,板番号i,上辺の左X座標関数lf,上辺の右座標関数rf,上辺のY座標関数bfから台形を描画する命令です。
        リスト内包表記で一括操作する際にmypyが戻り値要求をする為、Optionalな型ヒントを与えてあります。'''
        pygame.draw.polygon(surface=self.screen, color=color,
                            points=[[lf(i), bf(i)], [rf(i), bf(i)], [rf(i-1), bf(i-1)], [lf(i-1), bf(i-1)]])
        return None

    def _internal_division(self, ratio: float) -> Callable[[int], float]:
        '''ratioの比率でlxf-rxf間を内分する関数を返す関数です。ratio=0.0でlxf(左端)、ratio=1.0でrxf(右端)となります。'''
        return lambda i: self.lxf(i)*(1.0-ratio)+self.rxf(i)*ratio

    class _DO(NamedTuple):
        '''下記の_draw_object命令中にdraw_object命令を走査する際にmypyでエラーを起こさない為のクラスです。'''
        object: int; cond: int; x: float

    def _draw_object(self, i: int, car_y: int, cmax: int) -> None:
        '''設置物を描画します。'''
        scale = 1.5 * BOARD_W[i] / BOARD_W[0]
        mod_car_y = (car_y+i) % cmax
        obj_l = BOARD_LEFT_OBJECT[mod_car_y]
        obj_r = BOARD_RIGHT_OBJECT[mod_car_y]
        [draw_obj(surface=self.screen, img=IMG_OBJ[j.object], x=j.x, y=self.yf(i), scale=scale) for j in
         [self._DO(obj_r, OBJECT_BIKINI_BILLBOARD, self.idx130(i)), self._DO(obj_l, OBJECT_PALM_TREE, self.idxm05(i)),
          self._DO(obj_l, OBJECT_YACHT, self.idxm50(i))] if j.object == j.cond]
        if obj_l == OBJECT_SEA:
            self.screen.blit(source=IMG_SEA, dest=[self.idxm50(i) + SEA_BLIT_X_OFFSET, self.yf(i)])

    # def draw_player_car(self, car: Car):
    #     if i == car_y: # PLAYERカー
    #         pass
    #     tyome = self._internal_division(ratio=car.x/WX)(car.y)
    #     draw_shadow(surface=self.screen, x=self._internal_division(ratio=car.x/WX)(car.y),
    #                 y=self.yf(car.y), size=200*BOARD_W[i]/BOARD_W[0])
    #     draw_obj(surface=self.screen, img=img_car[3+car_lr[0]], x=ux+car_x[0]*BOARD_W[i]/800, y=self.yf(car.y), scale=0.05+BOARD_W[i]/BOARD_W[0])


