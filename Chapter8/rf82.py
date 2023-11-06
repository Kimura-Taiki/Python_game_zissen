# from os.path import dirname
# import sys
# if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))

import pygame
pygame.init()
from pygame.locals import K_SPACE
from functools import partial
from typing import Callable

from mod.solve_event import event_mapping, solve_event # 解決すべきpygameイベントを定義
from mod.screen import screen # ウィンドウを作成
from mod.background import BackGround # 背景を流して描画する命令を提供
from mod.starship import StarShip # 自機関連のクラスを提供
from mod.bullet import Bullet # 自機ビーム弾関連のクラスを提供
from mod.enemy import Enemy # 敵関連のクラスを提供
from mod.conflict import Conflict # 接触時判定の命令を提供
from mod.enemy_factory import EnemyFactory # 敵の生成クラスを提供
from mod.effect import Effect # 爆風のエフェクトを提供
from mod.title import Title, draw_text, SILVER # タイトル画面他ゲームの外枠を提供
from mod.sound import adjusted_bgm
from mod.index import SceneIndex
from mod.shoot_bullet import ShootBullet # 自弾を発射する機能を提供

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
    SceneIndex.return_title = index_shift
    SceneIndex.lose_game = partial(index_shift, new_idx=2)
    SceneIndex.clear_game = partial(index_shift, new_idx=3)

    def shot_down_enemy() -> None:
        nonlocal score
        s_ship.hp += 1
        score += 100
    Conflict.shoot_down_func = shot_down_enemy

    def start_game() -> None:
        nonlocal score
        index_shift(new_idx=1)
        score = 0
        s_ship.reset()
        bullets.clear()
        enemies.clear()
        effects.clear()
        adjusted_bgm(file="sound_gl/bgm.ogg", loops=-1)
    Title.start_game = start_game

    ShootBullet.is_diffusion = lambda: s_ship.hp > 10
    ShootBullet.consume_diffusion = lambda: setattr(s_ship, 'hp', s_ship.hp - 10)

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
                Title.title(screen=screen, key=key, tmr=tmr)
            case 1: # ゲームプレイ中
                SceneIndex.during_game(screen=screen, key=key, s_ship=s_ship, bullets=bullets, enemies=enemies, effects=effects, tmr=tmr)
            case 2: # ゲームオーバー
                SceneIndex.game_over(screen=screen, effects=effects, s_ship=s_ship, tmr=tmr)
            case 3: # ゲームクリア
                SceneIndex.game_clear(screen=screen, key=key, s_ship=s_ship, tmr=tmr)
        
        # 弾・敵機・爆風の経過と描画
        [sprite.elapse() for sprite in bullets+enemies+effects]
        pygame.sprite.Group(bullets,enemies,effects).draw(surface=screen)

        draw_text(screen, "Score "+str(score), 200, 30, 50, SILVER)
        draw_text(screen, "Timer "+str(tmr), 200, 30+40, 50, SILVER)
        draw_text(screen, "is_Diffusion "+str(ShootBullet.is_diffusion()), 200, 30+40*2, 50, SILVER)
        # シールドの描画
        if idx != 0:
            s_ship.shield_draw(screen=screen)

        # screen.blit(pygame.font.Font(None, size=40).render(str(Enemy.l), True, (255, 255, 255)), [0, 0])

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()