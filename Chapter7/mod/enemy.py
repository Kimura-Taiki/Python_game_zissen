import pygame
pygame.init()
import math
import random

class Enemy():

    IMG_ENEMY = (
        pygame.image.load("image_gl/enemy0.png"),
        pygame.image.load("image_gl/enemy1.png")
    )

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

    @classmethod
    def bring_enemy(cls, tmr): # 敵を出す
        if tmr%30 == 0:
            cls.set_enemy(random.randint(20, 940), cls.LINE_T, 90, 1, 6)

    @classmethod
    def set_enemy(cls, x, y, a, ty, sp): # 敵機をセットする
        while True:
            if cls.emy_f[cls.emy_no] == False:
                cls.emy_f[cls.emy_no] = True
                cls.emy_x[cls.emy_no] = x
                cls.emy_y[cls.emy_no] = y
                cls.emy_a[cls.emy_no] = a
                cls.emy_type[cls.emy_no] = ty
                cls.emy_speed[cls.emy_no] = sp
                break
            cls.emy_no = (cls.emy_no+1)%cls.ENEMY_MAX

    @classmethod
    def move_enemy(cls, screen): # 敵機の移動
        for i in range(cls.ENEMY_MAX):
            if cls.emy_f[i] == True:
                ang = -90-cls.emy_a[i]
                png = cls.emy_type[i]
                cls.emy_x[i] = cls.emy_x[i] + cls.emy_speed[i]*math.cos(math.radians(cls.emy_a[i]))
                cls.emy_y[i] = cls.emy_y[i] + cls.emy_speed[i]*math.sin(math.radians(cls.emy_a[i]))
                if cls.emy_type[i] == 1 and cls.emy_y[i] > 360:
                    cls.set_enemy(cls.emy_x[i], cls.emy_y[i], 90, 0, 8)
                    cls.emy_a[i] = -45
                    cls.emy_speed[i] = 16
                if cls.emy_x[i] < cls.LINE_L or cls.LINE_R < cls.emy_x[i] or cls.emy_y[i] < cls.LINE_T or cls.LINE_B < cls.emy_y[i]:
                    cls.emy_f[i] = False
                img_rz = pygame.transform.rotozoom(cls.IMG_ENEMY[png], ang, 1.0)
                screen.blit(img_rz, [cls.emy_x[i]-img_rz.get_width()/2, cls.emy_y[i]-img_rz.get_height()/2])
