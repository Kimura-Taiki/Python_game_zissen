class Outer():
    __ggg = 0

class Inner(Outer):
    __ggg = 1

print(Outer._Outer__ggg)
print(Inner._Outer__ggg)
print(Inner._Inner__ggg)