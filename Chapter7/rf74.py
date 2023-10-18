# from os.path import dirname
# import sys
# if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet, bullet_set, bullets_move, bullets_draw # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy, enemies_move, enemies_draw # 敵関連のクラスを提供
from mod.conflict import Conflict # 接触時判定の命令を提供
from mod.enemy_factory import EnemyFactory # 敵の生成クラスを提供
from mod.effect import Effect, effects_elapse, effects_draw # 爆風のエフェクトを提供
from mod.shield import Shield # シールド制を提供

def main() -> None: # メインループ
    global screen, event_mapping

    tmr = 0
    clock = pygame.time.Clock()
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    effects: list[Effect] = []
    s_ship = StarShip()

    while True:
        tmr += 1
        # pygameのイベントを解決
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        # 入力諸元を更新
        key = pygame.key.get_pressed()

        # 自機の移動
        s_ship.move(key=key)
        s_ship.draw(screen=screen, tmr=tmr, muteki=Shield.muteki)

        # 弾の発射
        bullet_set(key=key, bullets=bullets, x=s_ship.x, y=s_ship.y)
        bullets_move(bullets=bullets)
        bullets_draw(screen=screen, bullets=bullets)

        # 敵の表示と移動
        EnemyFactory.bring_enemy(enemies=enemies, tmr=tmr)
        enemies_move(enemies=enemies)
        enemies_draw(screen=screen, enemies=enemies)

        # 敵機と自弾の衝突判定
        effects_elapse(effects=effects, add_time=1)
        shots_down = Conflict.hit_bullet_and_enemy(bullets=bullets, enemies=enemies, effects=effects)
        Shield.recover(rec=shots_down)
        effects_draw(screen=screen, effects=effects)

        # 敵機と時期の衝突判定
        Shield.hit_ss_and_enemy(enemies=enemies, s_ship=s_ship, effects=effects)

        # シールドの描画
        Shield.draw(screen=screen)

        # screen.blit(pygame.font.Font(None, size=40).render(str(Enemy.l), True, (255, 255, 255)), [0, 0])

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()