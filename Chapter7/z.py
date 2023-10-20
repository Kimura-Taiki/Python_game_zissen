import pygame
from functools import partial
from typing import Any, Iterable, Union, NamedTuple

from collections import namedtuple

# Car = namedtuple('Car', ['color', 'mileage'])
# my_car =Car(color="red", mileage=3812.4)
# print(my_car, my_car.color, my_car.mileage)

# print(Car._fields)
# ec = Car._fields+('charge', )

# print(ec, type(ec))

# ElectricCar = namedtuple('ElectricCar', Car._fields + ('charge', ))

class Car(NamedTuple):
    color: str
    mileage: float

def hoi() -> Car:
    """
    これはhoiという関数です。
    hoiはhoi以外の何者でもない。それ以上でもそれ以下でもない。
    """
    return Car(color="red", mileage=3812.4)

col, mil = hoi()
print(hoi(), col, mil)

# screen.blit(pygame.font.Font(None, size=40).render("", True, (255, 255, 255)), [0, 0])

# nametupleで美しいPythonを書く！
# https://qiita.com/Seny/items/add4d03876f505442136

# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj