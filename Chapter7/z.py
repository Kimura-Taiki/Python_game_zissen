class Zakki():
    chr = "Z"

    def __init__(self):
        self.hatena = self.chr


print("z.pyだよ。？は{}だよ".format(Zakki().hatena))

class Xxx(Zakki):
    chr = "X"
    pass

class Yyy(Zakki):
    chr = "Y"
    pass

print("Xの？は{}だよ".format(Xxx().hatena))
print("Yの？は{}だよ".format(Yyy().hatena))
print("Xの？は{}だよ".format(Xxx().hatena))


# screen.blit(pygame.font.Font(None, size=40).render("", True, (255, 255, 255)), [0, 0])


# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj