import pygame
pygame.init()
import math
import random

img_enemy = [
    pygame.image.load("image_gl/enemy0.png"),
    pygame.image.load("image_gl/enemy1.png")
]

ENEMY_MAX = 100
emy_no = 0
emy_f = [False]*ENEMY_MAX
emy_x = [0]*ENEMY_MAX
emy_y = [0]*ENEMY_MAX
emy_a = [0]*ENEMY_MAX
emy_type = [0]*ENEMY_MAX
emy_speed = [0]*ENEMY_MAX

LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040


def bring_enemy(tmr): # 敵を出す
    if tmr%30 == 0:
        set_enemy(random.randint(20, 940), LINE_T, 90, 1, 6)

def set_enemy(x, y, a, ty, sp): # 敵機をセットする
    global emy_no
    while True:
        if emy_f[emy_no] == False:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            break
        emy_no = (emy_no+1)%ENEMY_MAX

def move_enemy(scrn): # 敵機の移動
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90-emy_a[i]
            png = emy_type[i]
            emy_x[i] = emy_x[i] + emy_speed[i]*math.cos(math.radians(emy_a[i]))
            emy_y[i] = emy_y[i] + emy_speed[i]*math.sin(math.radians(emy_a[i]))
            if emy_type[i] == 1 and emy_y[i] > 360:
                set_enemy(emy_x[i], emy_y[i], 90, 0, 8)
                emy_a[i] = -45
                emy_speed[i] = 16
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                emy_f[i] = False
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(img_rz, [emy_x[i]-img_rz.get_width()/2, emy_y[i]-img_rz.get_height()/2])
