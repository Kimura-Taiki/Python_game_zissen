import functools

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, z):
        return self.x + self.y + z

# インスタンスを作成
obj = MyClass(10, 20)

# addメソッドを部分適用してz引数を固定
add_30 = functools.partial(obj.add, z=30)

# 部分適用されたメソッドを呼び出す
result = add_30()
print(result)  # 出力: 60
