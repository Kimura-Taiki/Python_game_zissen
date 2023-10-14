import pygame

class Effect():
    IMG_EXPLODE_dayo: list[None | pygame.surface.Surface] = [
        None,
        pygame.image.load("image_gl/explosion1.png"),
        pygame.image.load("image_gl/explosion2.png"),
        pygame.image.load("image_gl/explosion3.png"),
        pygame.image.load("image_gl/explosion4.png"),
        pygame.image.load("image_gl/explosion5.png")
    ]
    pass


img_explode: list[pygame.surface.Surface] = [
    # None,
    pygame.image.load("image_gl/explosion1.png"), # 番兵として設置
    pygame.image.load("image_gl/explosion1.png"),
    pygame.image.load("image_gl/explosion2.png"),
    pygame.image.load("image_gl/explosion3.png"),
    pygame.image.load("image_gl/explosion4.png"),
    pygame.image.load("image_gl/explosion5.png")
]

EFFECT_MAX = 100
eff_no = 0
eff_p = [0]*EFFECT_MAX
eff_x = [0]*EFFECT_MAX
eff_y = [0]*EFFECT_MAX

def set_effect(x: int, y: int) -> None: # 爆発をセットする
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no+1)%EFFECT_MAX

def draw_effect(screen: pygame.surface.Surface) -> None: # 爆発の演出
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            screen.blit(img_explode[eff_p[i]], [eff_x[i]-48, eff_y[i]-48])
            eff_p[i] = eff_p[i] + 1
            if eff_p[i] == 6:
                eff_p[i] = 0
