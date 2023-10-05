# from os.path import dirname
# import sys
# if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy # 敵関連のクラスを提供
from mod.conflict import Conflict # 接触時判定の命令を提供

# Enemy.bring_enemy(0)
# print(Enemy.enemies[0])
# print(type(Enemy.enemies[0]))
# exit()

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

        # 敵機と自弾の衝突判定
        Conflict.hit_bullet_and_enemy(bullets=Bullet.bullets, enemies=Enemy.enemies)

        # screen.blit(pygame.font.Font(None, size=40).render(str(Enemy.l), True, (255, 255, 255)), [0, 0])

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()