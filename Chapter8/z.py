def compare_number(num):
    match num:
        case n if isinstance(n, int) and n > 0:
            print(f"numは正の整数 ({n}) です")
        case n if isinstance(n, int) and n < 0:
            print(f"numは負の整数 ({n}) です")
        case _:
            print("numは整数ではありません")

compare_number(10)
compare_number(-5)
compare_number(0)
compare_number("文字列")  # ここはパターンにマッチしないため、最後のケースが実行される
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