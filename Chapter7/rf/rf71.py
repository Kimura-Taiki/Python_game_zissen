from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy # 敵関連のクラスを提供

def main(): # メインループ
    global screen, event_mapping

    tmr = 0
    clock = pygame.time.Clock()

    while True:
        StarShip.elapse()
        tmr += 1
        # pygameのイベントを解決
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        # 入力諸元を更新
        key = pygame.key.get_pressed()

        # 自機の移動
        StarShip.move(key=key)
        StarShip.draw(screen=screen)

        # 弾の発射
        Bullet.set(key=key, mother=StarShip)
        Bullet.move()
        Bullet.draw(screen=screen)

        # 敵の表示と移動
        Enemy.bring_enemy(tmr=tmr)
        Enemy.move()
        Enemy.draw(screen=screen)

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()