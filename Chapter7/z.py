class Zakki():
    chr = "Z"

    def __init__(self):
        self.hatena = self.chr

class Factory():
    tpls = (('x', 12),
            ('y', True))
    
    def __init__(self, params={}) -> None:
        for tpl in self.tpls:
            if tpl[0] in params.keys():
                setattr(self, tpl[0], params[tpl[0]])
            else:
                setattr(self, tpl[0], tpl[1])

f = Factory({'x':38, 'z':"Get"})
print(f, f.x, f.y)



# screen.blit(pygame.font.Font(None, size=40).render("", True, (255, 255, 255)), [0, 0])


# 依存性の注入
# https://qiita.com/mkgask/items/d984f7f4d94cc39d8e3c

# Injector
# https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770cjj