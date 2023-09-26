import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供

# 画像の読み込み
img_sship = pygame.image.load("image_gl/starship.png")

def move_starship(scrn, key): # 自機の移動
    if key[pygame.K_UP] == 1:
        StarShip.y = StarShip.y - 20
        if StarShip.y < 80:
            StarShip.y = 80
    if key[pygame.K_DOWN] == 1:
        StarShip.y = StarShip.y + 20
        if StarShip.y > 640:
            StarShip.y = 640
    if key[pygame.K_LEFT] == 1:
        StarShip.x = StarShip.x - 20
        if StarShip.x < 40:
            StarShip.x = 40
    if key[pygame.K_RIGHT] == 1:
        StarShip.x = StarShip.x + 20
        if StarShip.x > 920:
            StarShip.x = 920
    scrn.blit(img_sship, [StarShip.x-37, StarShip.y-48])


def main(): # メインループ
    global screen, event_mapping

    clock = pygame.time.Clock()

    while True:
        # pygameのイベントを解決
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        key = pygame.key.get_pressed()
        move_starship(screen, key)

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()