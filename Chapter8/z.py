class MyClass:
    def __init__(self):
        self._val = 0

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        if value < 0:
            print("値は0以上である必要があります。")
        else:
            self._val = value

    def __iadd__(self, other):
        if self._val + other < 0:
            print("加算後の値は0以上である必要があります。")
        else:
            self._val += other

# クラスのインスタンスを作成
obj = MyClass()

# val 属性に対して += 演算子を使用
obj.val += 5  # 正常に実行

print(obj.val)  # 5

# 不正な値を加算しようとすると警告が表示
obj.val += -10  # "加算後の値は0以上である必要があります。" と表示
obj.val -= 10

exit()
from typing import NamedTuple, Optional

def five(i:int) -> Optional[int]:
    return None
    return i if i%5==0 else None

def nono(i:int) -> Optional[bool]:
    return None

class Color(NamedTuple):
    r: int
    g: int
    b: int

g1 = {Color(255, 0, 0), Color(255, 255, 0), Color(255, 0, 0)}

print(g1, type(g1))

print([five(i) for i in range(10)])
print([nono(i) for i in range(10)])
