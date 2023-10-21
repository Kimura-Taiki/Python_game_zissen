class Coord():
    x: int
    y: int

z = Coord()
z.x, z.y = 10, 20

# for i in range(0,5): print(i)
l= [i for i in range(0,10)]
for i in l:
    l.remove(i)

[print(i) for i in l]


# nametupleで美しいPythonを書く！
# https://qiita.com/Seny/items/add4d03876f505442136

# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj