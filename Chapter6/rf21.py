import pygame
import sys

# 画像の読み込み
img_galaxy = pygame.image.load("image_gl/galaxy.png")

bg_y = 0

def quit_event():
    pygame.quit()
    sys.exit()

def fullscreen_event(screen, x, y):
    screen = pygame.display.set_mode((x ,y), pygame.FULLSCREEN)

def windowed_event(screen, x, y):
    screen = pygame.display.set_mode((x ,y))

def main(): # メインループ
    global bg_y

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    fullscreen_event(screen=screen, x=960, y=720)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    windowed_event(screen=screen, x=960, y=720)
        
        # 背景のスクロール
        bg_y = (bg_y+16)%720
        screen.blit(img_galaxy, [0, bg_y-720])
        screen.blit(img_galaxy, [0, bg_y])

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()