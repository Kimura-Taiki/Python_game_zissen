# 以下のpythonのコードでCoord.xの代入(=)と加減算(+=,-=)にmax(0, min(100, self._x))のバリデーションが正しく掛かっていますか？

class Coord:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        '''バリデーションです。xが0から100の間に収まるように、
        maxとmin関数を噛ませています。
        ついでにprint命令も噛ませて処理を命じさせています。'''
        self._x = max(0, min(100, value)); print("Xは{}だよ".format(self._x))

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

# クラスのインスタンスを作成
coord = Coord(50, 60)
# x属性に値を代入
coord.x = 80
coord.x = 120
coord.x = 0
coord.x += 55
coord.x += 40
coord.x -= 70
coord.x -= 9999