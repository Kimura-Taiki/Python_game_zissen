from typing import Optional

def x() -> Optional[bool]:
    pass

print([x() for i in range(10)])

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
