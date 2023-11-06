from typing import NamedTuple
class Coord():
    x:int = 0
    '''hoihoi'''
    z:int = 99
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

c = Coord(100, 200)
print(c, id(c))
c.x = 44
print(c, id(c))
c = Coord(44, 200)
print(c, id(c))
