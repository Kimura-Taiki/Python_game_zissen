import pygame
import sys
from math import sin, radians
from pygame.locals import *

BOARD = 120
'''描画する板の枚数'''


def make_course() -> list[float]:
    '''コースの曲率を作る関数。'''
    return [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]

def main(): # メイン処理
    pygame.init()
    pygame.display.set_caption("Python Racer")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    img_bg = pygame.image.load("image_pr/bg.png").convert()

    # 道路の板の基本形状を計算
    BOARD_W = [10+(BOARD-i)**2/12 for i in range(BOARD)]
    '''板の横幅です。0が手前、BOARD-1が最遠です。'''
    BOARD_H = [3.4*(BOARD-i)/BOARD for i in range(BOARD)]
    '''板の縦幅です。0が手前、BOARD-1が最遠です。'''

    curve = make_course()
    '''コースの該当地点での曲率です。実際に描画する際には視点位置からの曲率積分を使います。'''
    CMAX = len(curve)
    '''コースの全長、板の枚数で定義されている。１周するとまた最初から数える。'''


    car_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[K_UP]:
            car_y = (car_y+1)%CMAX

        # 描画用の道路のX座標を計算
        di: float = 0.0
        '''視点位置からの曲率積分です。'''
        board_x: list[float] = [400-BOARD_W[i]/2+(di := di+curve[(car_y+1) % CMAX])/2 for i in range(BOARD)]
        '''板の左下X座標です。左上X座標はboard_x[i-1]で求めます。'''
        

        sy = 400 # 道路を描き始める位置

        screen.blit(img_bg, [0, 0])

        # 描画用データをもとに道路を描く
        for i in range(BOARD-1, 0, -1):
            ux = board_x[i]
            uy = sy
            uw = BOARD_W[i]
            sy = sy + BOARD_H[i]
            bx = board_x[i-1]
            by = sy
            bw = BOARD_W[i-1]
            col = (160,160,160)
            if (car_y+i)%12 == 0:
                col = (255,255,255)
            match car_y+i:
                case 480: col = (0, 0, 0)
                case 120: col = (255, 0, 0)
                case 240: col = (0, 128, 0)
                case 360: col = (0, 0, 255)
            pygame.draw.polygon(surface=screen, color=col, points=[[ux, uy], [ux+uw, uy], [bx+bw, by], [bx, by]])

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
