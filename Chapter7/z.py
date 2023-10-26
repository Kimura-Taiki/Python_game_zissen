from pygame.sprite import Group
from typing import List, Never, Set
import pygame

# TypedGroupという新しいクラスを作成する代わりに、pygame.sprite.Groupをそのまま使用
# my_group: List[Sprite] = Group()
pygame.sprite.Group()
class Sprite(pygame.sprite.Sprite):
    pass
my_group: Set[Sprite | Never] = Group()
my_sprite: Sprite = Sprite()  # Spriteはあくまで例です
my_group.add(my_sprite)
sprite: Sprite = my_group.sprites()[0]



# from pygame.sprite import Group, Sprite

# class TypedGroup(Group[Sprite]):
#     def __init__(self) -> None:
#         super().__init__(self)

# # 上記のように書くと、
# # Missing type parameters for generic type "Group"  [type-arg]
# # とmypyのエラーが出てしまいます。

# class MySprite(Sprite):
#     pass

# # TypedGroup を使用する
# my_group: TypedGroup = TypedGroup()

# # TypedGroup に要素を追加
# my_sprite: MySprite = MySprite()  # MySprite は自分のスプライトクラスの例
# my_group.add(my_sprite)

# # TypedGroup から要素を取得
# sprite: MySprite = my_group.sprites()[0]

# from typing import NamedTuple
# class Color(NamedTuple):
#     r: int; g: int; b: int

# r = Color(255, 0, 0)
# print(r, r.r, r.g, r.b)

# from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
# print(K_UP, K_DOWN, K_LEFT, K_RIGHT, type(K_UP))

# from pygame.sprite import Group
# g = Group()
# g.draw()


# nametupleで美しいPythonを書く！
# https://qiita.com/Seny/items/add4d03876f505442136

# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj