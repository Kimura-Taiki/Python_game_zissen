import pygame
import sys
from math import sin, radians
from pygame.locals import K_UP, QUIT
from typing import Callable, Final, Optional
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


def draw_obj(surface: pygame.surface.Surface, img: pygame.surface.Surface, x: int | float, y: int | float, scale: float) -> None:
    img_rz = pygame.transform.rotozoom(surface=img, angle=0, scale=scale)
    surface.blit(source=img_rz, dest=[x-img_rz.get_width()/2, y-img_rz.get_height()])


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
        # return Course(img_bg=pygame.image.load(PNG_BG), cmax=BOARD*CLEN,
        return Course(img_bg=IMG_BG, cmax=BOARD*CLEN,
                      curve=[DATA_LR[i]*(BOARD-j)/BOARD+DATA_LR[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      updown=[DATA_UD[i]*(BOARD-j)/BOARD+DATA_UD[(i+1) % CLEN]*j/BOARD for i in range(CLEN) for j in range(BOARD)],
                      object_left=BOARD_LEFT_OBJECT,
                      object_right=BOARD_RIGHT_OBJECT)


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

        _sum_curve = 0.0
        curvature_integral = [(_sum_curve := _sum_curve+self.COURSE.CURVE[self._mod_car_y(dy=i)]/2) for i in range(BOARD)]
        board_lx = [WX/2-BOARD_W[i]/2+curvature_integral[i] for i in range(BOARD)]
        board_rx = [WX/2+BOARD_W[i]/2+curvature_integral[i] for i in range(BOARD)]
        ud: float = 0.0
        board_ud: list[float] = [(ud := ud+self.COURSE.UPDOWN[self._mod_car_y(dy=i)])/30 for i in range(BOARD)]
        horizon: int = Y_AT_0_DEGREES+int(sum(self.COURSE.UPDOWN[self._mod_car_y(dy=i)] for i in range(BOARD))/3)
        sy: float = float(horizon)
        board_by: list[float] = [(sy := sy+BOARD_H[BOARD-1-i]*(WY-horizon)/200)-BOARD_UD[BOARD-1-i]*board_ud[BOARD-1-i] for i in range(BOARD)][::-1]

        self._draw_background(sea_x=int(board_lx[BOARD-1]-780), horizon_y=horizon)

        # 描画用データをもとに道路を描く
        for i in range(BOARD-1, 0, -1):
            self._draw_board_section(i=i, lxf=lambda i: board_lx[i], rxf=lambda i: board_rx[i], wxf=lambda i: BOARD_W[i], yf=lambda i: board_by[i])

        pygame.display.update()
        self.clock.tick(60)

    def _mod_car_y(self, dy: int) -> int:
        '''car_yをコース全長で循環させる処理をこの関数で統一して字数も減らします。'''
        return (self.car_y+dy) % self.COURSE.CMAX

    def _draw_background(self, sea_x: int, horizon_y: int) -> None:
        '''背景部分を描画する命令です。道路や設置物は連続的なので_draw_board_section命令の繰り返しで描画しています。'''
        self.screen.fill(color=SEA_BLUE)
        self.screen.blit(self.COURSE.IMG_BG, [self.vertical-WX, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(self.COURSE.IMG_BG, [self.vertical, horizon_y-Y_AT_0_DEGREES])
        self.screen.blit(source=IMG_SEA, dest=[sea_x, horizon_y])

    def _draw_trapezoid(self, color: pygame.Color, i: int,
                        lf: Callable[[int], float], rf: Callable[[int], float], bf: Callable[[int], float]) -> None:
        '''色color,板番号i,上辺の左X座標関数lf,上辺の右座標関数rf,上辺のY座標関数bfから台形を描画する命令です。'''
        pygame.draw.polygon(surface=self.screen, color=color,
                            points=[[lf(i), bf(i)], [rf(i), bf(i)], [rf(i-1), bf(i-1)], [lf(i-1), bf(i-1)]])

    def _draw_board_section(self, i: int, lxf: Callable[[int], float], rxf: Callable[[int], float], wxf: Callable[[int], float], yf: Callable[[int], float]) -> None:
        '''板番号i,上辺の左X座標関数lxf,上辺の右座標関数rxf,上辺の幅関数wxf,上辺のY座標関数yfから板の存在する面全域を描画する命令です。
        描画対象には道路と設置物があります。'''
        self._draw_trapezoid(color=trapezoid_color(course_point=self.car_y+i), i=i, lf=lxf, rf=rxf, bf=yf)
        if int(self.car_y+i)%10 <= 4: # 左右の黄色線
            self._draw_trapezoid(color=YELLOW, i=i, lf=lxf, rf=lambda i: lxf(i)+wxf(i)*0.02, bf=yf)
            self._draw_trapezoid(color=YELLOW, i=i, lf=lambda i: rxf(i)-wxf(i)*0.02, rf=rxf, bf=yf)
        if int(self.car_y+i)%20 <= 10: # 白線
            self._draw_trapezoid(color=WHITE, i=i, lf=lambda i: lxf(i)+wxf(i)*0.24, rf=lambda i: lxf(i)+wxf(i)*0.26, bf=yf)
            self._draw_trapezoid(color=WHITE, i=i, lf=lambda i: lxf(i)+wxf(i)*0.49, rf=lambda i: rxf(i)-wxf(i)*0.49, bf=yf)
            self._draw_trapezoid(color=WHITE, i=i, lf=lambda i: rxf(i)-wxf(i)*0.26, rf=lambda i: rxf(i)-wxf(i)*0.24, bf=yf)
        scale = 1.5*BOARD_W[i]/BOARD_W[0]
        obj_l = BOARD_LEFT_OBJECT[self._mod_car_y(dy=i)]
        if obj_l == OBJECT_PALM_TREE:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_l], x=lxf(i)-wxf(i)*0.05, y=yf(i), scale=scale)
        if obj_l == OBJECT_YACHT:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_l], x=lxf(i)-wxf(i)*0.5, y=yf(i), scale=scale)
        if obj_l == OBJECT_SEA:
            self.screen.blit(source=IMG_SEA, dest=[lxf(i)-wxf(i)*0.5-780, yf(i)])
        obj_r = BOARD_RIGHT_OBJECT[self._mod_car_y(dy=i)]
        if obj_r == OBJECT_BIKINI_BILLBOARD:
            draw_obj(surface=self.screen, img=IMG_OBJ[obj_r], x=rxf(i)+wxf(i)*0.3, y=yf(i), scale=scale)
