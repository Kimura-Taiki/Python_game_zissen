from mod.course import Course
from mod.const import PLCAR_Y, WX

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
