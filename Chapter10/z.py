import pygame
from typing import Optional

# ドクストリングを各変数に与える為に宣言だけしてあります
IMG_BG: pygame.surface.Surface
'''Surface化済みの背景画像の原板です。'''
IMG_SEA: pygame.surface.Surface
'''Surface化済みの海岸画像の原板です。'''
IMG_OBJ: list[Optional[pygame.surface.Surface]]
'''Surface化済みのオブジェクト画像の原板です。'''

# 遅延定義用の命令
def img_init() -> None:
    global IMG_BG, IMG_SEA, IMG_OBJ
    IMG_BG = pygame.image.load("image_pr/bg.png").convert()
    IMG_SEA = pygame.image.load("image_pr/sea.png").convert_alpha()
    IMG_OBJ = [
        None,
        pygame.image.load("image_pr/board.png").convert_alpha(),
        pygame.image.load("image_pr/yashi.png").convert_alpha(),
        pygame.image.load("image_pr/yacht.png").convert_alpha()]

# 遅延定義用の命令はset_mode後に使う
pygame.init()
screen = pygame.display.set_mode((640, 480))
img_init()
print(IMG_SEA)
