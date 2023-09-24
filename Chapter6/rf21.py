import pygame

from mod.screen import screen, WIN_Y
from mod.solve_event import event_mapping, solve_event

# 背景関連の処理をBackGroundクラスへ集約
class BackGround():
    bg_y = 0
    IMG_GALAXY = pygame.image.load("image_gl/galaxy.png")
    
    @classmethod
    def scroll(cls, speed):
        BackGround.bg_y = (BackGround.bg_y+speed)%WIN_Y

    @classmethod
    def draw(cls, screen):
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y-WIN_Y])
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y])

def main(): # メインループ
    global screen, event_mapping

    clock = pygame.time.Clock()

    while True:
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()