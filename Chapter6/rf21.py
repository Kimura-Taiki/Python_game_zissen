import pygame
import sys
from functools import partial

# 画像の読み込み
img_galaxy = pygame.image.load("image_gl/galaxy.png")

bg_y = 0
WIN_X = 960
WIN_Y = 720
WIN_SIZE = (WIN_X, WIN_Y)


screen = pygame.display.set_mode(WIN_SIZE)

def quit_event():
    pygame.quit()
    sys.exit()

def fullscreen_event(screen, size):
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen, size):
    screen = pygame.display.set_mode(size=size)

event_mapping = [
    {"type":pygame.QUIT,                            "func":quit_event},
    {"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)},
    {"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)}]

def solve_event(mapping):
    for event in pygame.event.get():
        for map in mapping:
            if event.type == map["type"] and (event.type != pygame.KEYDOWN or event.key == map["key"]):
                map["func"]()
                break

def main(): # メインループ
    global bg_y, screen, event_mapping

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    clock = pygame.time.Clock()

    while True:
        solve_event(event_mapping)
        
        # 背景のスクロール
        bg_y = (bg_y+16)%720
        screen.blit(img_galaxy, [0, bg_y-720])
        screen.blit(img_galaxy, [0, bg_y])

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()