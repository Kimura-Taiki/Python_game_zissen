# from typing import Callable, Any

# class MyClass:
#     def __init__(self, value: int):
#         self.value = value

# # クラスの外部で定義した関数
# def my_function(self: MyClass, new_value: int) -> None:
#     self.value = new_value

# # クラスにバインドした関数を持つクラスを作成
# class BoundMethods:
#     my_method: Callable[..., Any] = my_function

# # BoundMethodsクラスのインスタンスを作成
# bound_obj = BoundMethods()

# # インスタンスを作成してメソッドを呼び出す
# obj = MyClass(42)
# print(obj.value)  # 42
# bound_obj.my_method(obj, 99)  # インスタンスメソッドを呼び出す
# print(obj.value)  # 99


from typing import Callable, Any

class MyClass:
    def __init__(self, value: int):
        self.value = value
    
    def _raise_nie(self, value: int) -> None: raise NotImplementedError()

    my_method: Callable[[Any, int], None] = _raise_nie

# クラスの外部で定義した関数
def my_function(self: MyClass, new_value: int) -> None:
    self.value = new_value

# 関数をインスタンスメソッドとしてクラスにバインド
# MyClass.my_method: Callable[[MyClass, int], None] = my_function
MyClass.my_method: Callable[[MyClass, int], None] = my_function

# インスタンスを作成してメソッドを呼び出す
obj = MyClass(42)
print(obj.value)  # 42
obj.my_method(99)  # インスタンスメソッドを呼び出す
print(obj.value)  # 99

# 以上のpythonコードをmypyへ通すと
# z.py:14: error: Type cannot be declared in assignment to non-self attribute  [misc]
# z.py:14: error: Cannot assign to a method  [method-assign]
# z.py:14: error: Incompatible types in assignment (expression has type "Callable[[Arg(MyClass, 'self'), Arg(int, 'new_value')], None]", variable has type "Callable[[Arg(MyClass, 'self'), Arg(int, 'value')], None]")  [assignment]
# Found 3 errors in 1 file (checked 1 source file)
# とエラーが返ってきます。