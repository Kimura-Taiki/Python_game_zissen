from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet, bullet_set # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy # 敵関連のクラスを提供
from mod.conflict import Conflict # 接触時判定の命令を提供
from mod.enemy_factory import EnemyFactory # 敵の生成クラスを提供
from mod.effect import Effect # 爆風のエフェクトを提供
from mod.shield import Shield # シールド制を提供

def main() -> None: # メインループ
    global screen, event_mapping

    tmr = 0
    clock = pygame.time.Clock()
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    effects: list[Effect] = []
    s_ship = StarShip()
    shield = Shield()
    print(s_ship)

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
        s_ship.draw(screen=screen, tmr=tmr, muteki=shield.muteki)

        # 弾の発射
        do_z = bullet_set(key=key, bullets=bullets, x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery, may_z=shield.shield>10)
        shield.shield -= do_z*10
        [bullet.move() for bullet in bullets]
        pygame.sprite.Group(bullets).draw(surface=screen)

        # 敵の表示と移動
        EnemyFactory.bring_enemy(enemies=enemies, tmr=tmr)
        [enemy.move() for enemy in enemies]
        pygame.sprite.Group(enemies).draw(surface=screen)

        # 敵機と自弾の衝突判定
        [effect.elapse(t=1) for effect in effects]
        shots_down = Conflict.hit_bullet_and_enemy(bullets=bullets, enemies=enemies, effects=effects)
        shield.recover(rec=shots_down)
        [effect.draw(screen=screen) for effect in effects]

        # 敵機と時期の衝突判定
        shield.hit_ss_and_enemy(enemies=enemies, craft=s_ship.craft, effects=effects)

        # シールドの描画
        shield.draw(screen=screen)

        # screen.blit(pygame.font.Font(None, size=40).render(str(Enemy.l), True, (255, 255, 255)), [0, 0])

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()