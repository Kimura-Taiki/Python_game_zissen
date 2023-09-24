import pygame

from mod.screen import screen, WIN_Y
from mod.solve_event import event_mapping, solve_event
from mod.background import BackGround

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