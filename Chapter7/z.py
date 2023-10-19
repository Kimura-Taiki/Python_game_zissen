import pygame
from functools import partial
from typing import Any

class Aaa():
    def __init__(self, x: int=100, y: int=200) -> None:
        self.x: int = x
        self.y: int = y

class Bbb():
    def __init__(self, b: int=111) -> None:
        self.a0: Aaa = Aaa()
        self.a1: Aaa = Aaa(x=1, y=11)
        self.b: int = b

b = Bbb()
print(b, b.a0, b.a1, b.b, b.a0.x, b.a0.y, b.a1.x, b.a1.y)
exit()

def pita(x: int, y: int) -> float:
    return (x**2+y**2)**0.5

print(pita, type(pita),pita(3,4), type(pita(3,4)))
px = partial(pita, x=4, y=5)
print(px, type(px), px(), type(px()))
exit()


def f(i: int | None):
    if i is not None:
        print("{}の二乗は{}です".format(i, i*i))
    else:
        print("な〜んにもない")

data: int | None = None
print(data, type(data))
company_branches: dict[str, dict[str, dict[str, str | bool | int]]]
company_branches = {
    "東京": {
        "001": {
            "name": "佐藤",
            "is_leader": True,
            "leader_period": 3,
        },
        "005": {"name": "田中", "is_leader": False},
    },
    "福岡": {
        "003": {
            "name": "伊藤",
            "is_leader": True,
            "leader_period": 5,
        },
        "008": {"name": "山本", "is_leader": False},
        "011": {"name": "吉田", "is_leader": False},
    },
}
print(company_branches)

f(3)
f(12)
f(None)
exit()


class Zakki():
    chr = "Z"

    def __init__(self):
        self.hatena = self.chr


class Hoge():
    def __init__(self, name) -> None:
        self.name = name

    def __del__(self) -> None:
        print("{}を削除したよ".format(self.name))

h1 = Hoge("Hoge1")
h2 = Hoge("ほげ２")
h3 = Hoge("保外三")
hsa = [h1, h2]
hsb = [h2, h3]
hsa.remove(h1)
del h1
# del h2
print("削除終わり")


# screen.blit(pygame.font.Font(None, size=40).render("", True, (255, 255, 255)), [0, 0])


# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj