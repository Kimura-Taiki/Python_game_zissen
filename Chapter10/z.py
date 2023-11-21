x: list[int] = [0]*5
print("x", x, id(x))
y = x
print("y", y, id(y))
x = [i for i in range(5)]
print("x", x, id(x))
print("y", y, id(y))

