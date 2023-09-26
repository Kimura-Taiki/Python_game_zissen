import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供

img_weapon = pygame.image.load("image_gl/bullet.png")

msl_f = False
msl_x = 0
msl_y = 0


def set_missile(mother): # 自機の発射する弾をセットする
    global msl_f, msl_x, msl_y
    if msl_f == False:
        msl_f = True
        msl_x = mother.x
        msl_y = mother.y-50


def move_missile(screen): # 弾の移動
    global msl_f, msl_y
    if msl_f == True:
        msl_y = msl_y - 36
        screen.blit(img_weapon, [msl_x-10, msl_y-32])
        if msl_y < 0:
            msl_f = False


def main(): # メインループ
    global screen, event_mapping

    clock = pygame.time.Clock()

    while True:
        StarShip.elapse()
        # pygameのイベントを解決
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        # 自機の移動
        StarShip.move(key=pygame.key.get_pressed())
        StarShip.draw(screen=screen)

        # 弾の発射
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            set_missile(StarShip)
        move_missile(screen=screen)

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()