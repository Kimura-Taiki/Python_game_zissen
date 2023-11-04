class MyClass():
    my_function = lambda: None

    def do_something(self):
        self.my_function()

def my_dependent_function(self):
    return "依存関数が実行されました"

my_instance = MyClass()

print(MyClass.my_function)
MyClass.my_function = my_dependent_function
print(MyClass.my_function)
my_instance.do_something()

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
