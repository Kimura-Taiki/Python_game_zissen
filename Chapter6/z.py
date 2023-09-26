def __z__():
    pass

class Coord():
    x = 1
    y = 2

    @classmethod
    def set(cls, x, y):
        cls.x, cls.y = x, y

    @classmethod
    def pri(cls):
        print(cls.x, cls.y)

def cpri(cls):
    print(cls, cls.x, cls.y)

Coord.pri()
cpri(Coord)

Coord.set(100, 200)
Coord.pri()
cpri(Coord)
