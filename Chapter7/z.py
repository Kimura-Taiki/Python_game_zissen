from typing import NamedTuple
class Color(NamedTuple):
    r: int; g: int; b: int

r = Color(255, 0, 0)
print(r, r.r, r.g, r.b)

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
print(K_UP, K_DOWN, K_LEFT, K_RIGHT, type(K_UP))


# nametupleで美しいPythonを書く！
# https://qiita.com/Seny/items/add4d03876f505442136

# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj