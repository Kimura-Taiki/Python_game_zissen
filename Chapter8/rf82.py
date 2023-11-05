# from os.path import dirname
# import sys
# if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()
from pygame.locals import K_SPACE

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet, bullet_set # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy # 敵関連のクラスを提供
from mod.conflict import Conflict # 接触時判定の命令を提供
from mod.enemy_factory import EnemyFactory # 敵の生成クラスを提供
from mod.effect import Effect # 爆風のエフェクトを提供
from mod.title import Title, draw_text, SILVER # タイトル画面他ゲームの外枠を提供
from mod.sound import adjusted_bgm
from mod.index import game_over, game_clear

def main_elapse(screen: pygame.surface.Surface, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect]) -> None:
    '''メイン画面で操作に関係無く時間経過で動いていく処理。
    主にスプライトの移動と描画、消滅を担う。'''
    [sprite.elapse() for sprite in bullets+enemies+effects]
    pygame.sprite.Group(bullets,enemies,effects).draw(surface=screen)


def main() -> None: # メインループ
    global screen, event_mapping

    idx = 0
    tmr = 0
    score = 0
    clock = pygame.time.Clock()
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    effects: list[Effect] = []
    s_ship = StarShip()

    def index_shift(new_idx :int=0, new_tmr :int=0) -> None:
        '''idxとtmrを動かす際に引数や依存性を減らす為の命令です。'''
        nonlocal idx, tmr
        idx, tmr = new_idx, new_tmr

    while True:
        tmr += 1
        # pygameのイベントを解決
        solve_event(event_mapping)
        
        # 背景のスクロール
        BackGround.scroll(speed=16)
        BackGround.draw(screen=screen)

        # 入力諸元を更新
        key = pygame.key.get_pressed()
        match idx:
            case 0: # タイトル
                Title.draw(screen=screen, key=key, tmr=tmr)
                if key[K_SPACE] == 1:
                    idx = 1
                    tmr = 0
                    score = 0
                    s_ship.reset()
                    bullets.clear()
                    enemies.clear()
                    effects.clear()
                    adjusted_bgm(file="sound_gl/bgm.ogg", loops=-1)
            case 1: # ゲームプレイ中
                # 自機の移動と描画
                s_ship.move(key=key)
                s_ship.draw(screen=screen, tmr=tmr)

                # 弾の生成
                do_z = bullet_set(key=key, bullets=bullets, x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery, may_z=s_ship.hp>10)
                s_ship.hp -= do_z*10

                # 敵の生成
                EnemyFactory.bring_enemy(enemies=enemies, tmr=tmr)

                if tmr == 30*15:
                    idx = 3
                    tmr = 0
            case 2: # ゲームオーバー
                game_over(screen=screen, effects=effects, s_ship=s_ship, tmr=tmr, call=index_shift)
            case 3: # ゲームクリア
                game_clear(screen=screen, key=key, s_ship=s_ship, tmr=tmr, call=index_shift)
        
        main_elapse(screen=screen, bullets=bullets, enemies=enemies, effects=effects)

        # 敵機と自弾の衝突判定
        shots_down = Conflict.hit_bullet_and_enemy(bullets=bullets, enemies=enemies, effects=effects)
        s_ship.hp += shots_down
        score += shots_down*100

        # 敵機と自期の衝突判定
        Conflict.hit_ss_and_enemy(s_ship=s_ship, enemies=enemies, effects=effects)
        if s_ship.hp <= 0 and idx == 1:
            idx = 2
            tmr = 0

        draw_text(screen, "Score "+str(score), 200, 30, 50, SILVER)
        draw_text(screen, "Timer "+str(tmr), 200, 30+40, 50, SILVER)
        # シールドの描画
        if idx != 0:
            s_ship.shield_draw(screen=screen)

        # screen.blit(pygame.font.Font(None, size=40).render(str(Enemy.l), True, (255, 255, 255)), [0, 0])

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()