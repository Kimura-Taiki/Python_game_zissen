import pygame

from mod.screen import screen, WIN_Y
from mod.solve_event import event_mapping, solve_event

# 画像の読み込み
img_galaxy = pygame.image.load("image_gl/galaxy.png")

bg_y = 0

def main(): # メインループ
    global bg_y, screen, event_mapping

    clock = pygame.time.Clock()

    while True:
        solve_event(event_mapping)
        
        # 背景のスクロール
        bg_y = (bg_y+16)%WIN_Y
        screen.blit(img_galaxy, [0, bg_y-WIN_Y])
        screen.blit(img_galaxy, [0, bg_y])

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()