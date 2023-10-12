def f(i: int | None):
    if i is not None:
        print("{}の二乗は{}です".format(i, i*i))
    else:
        print("な〜んにもない")

data: int | None = None
print(data, type(data))


f(3)
f(12)
f(None)
exit()


class Zakki():
    chr = "Z"

    def __init__(self):
        self.hatena = self.chr


class Hoge():
    def __init__(self, name) -> None:
        self.name = name

    def __del__(self) -> None:
        print("{}を削除したよ".format(self.name))

h1 = Hoge("Hoge1")
h2 = Hoge("ほげ２")
h3 = Hoge("保外三")
hsa = [h1, h2]
hsb = [h2, h3]
hsa.remove(h1)
del h1
# del h2
print("削除終わり")


# screen.blit(pygame.font.Font(None, size=40).render("", True, (255, 255, 255)), [0, 0])


# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj