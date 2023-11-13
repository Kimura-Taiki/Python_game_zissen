import pygame
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.starship import StarShip
from mod.bullet import Bullet
from mod.enemy import Enemy
from mod.effect import Effect
from mod.sound import SE_DAMAGE, adjusted_bgm
from mod.title import draw_text, RED, SILVER
from mod.enemy_factory import EnemyFactory
from mod.shoot_bullet import ShootBullet
from mod.conflict import Conflict



class SceneIndex():
    '''ゲームシーン毎の処理を担うクラスです。
    ゲーム中、ゲームオーバー、ゲームクリアの３種類を備えています。'''
    @staticmethod
    def __nie_return_title() -> None: raise NotImplementedError("SceneIndex.return_titleが未実装\nタイトル復帰用の命令が設定されていません")
    return_title: Callable[[], None] = __nie_return_title
    @staticmethod
    def __nie_clear_game() -> None: raise NotImplementedError("SceneIndex.clear_gameが未実装\nゲームクリア用の命令が設定されていません")
    clear_game: Callable[[], None] = __nie_clear_game
    @staticmethod
    def __nie_lose_game() -> None: raise NotImplementedError("SceneIndex.lose_gameが未実装\nゲームオーバー用の命令が設定されていません")
    lose_game: Callable[[], None] = __nie_lose_game

    @classmethod
    def during_game(cls, screen: pygame.surface.Surface, key: pygame.key.ScancodeWrapper, s_ship: StarShip, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect], tmr: int) -> None:
        # 自機の移動と描画
        s_ship.move(key=key)
        s_ship.draw(screen=screen, tmr=tmr)

        # 弾の生成
        ShootBullet.single_shot(pressed_keys=key, bullets=bullets, x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery)
        ShootBullet.diffusion_shot(pressed_keys=key, bullets=bullets, x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery)

        # 敵の生成
        EnemyFactory.bring_enemy(enemies=enemies, tmr=tmr)

        # 敵機と自弾の衝突判定
        Conflict.hit_bullet_and_enemy(bullets=bullets, enemies=enemies, effects=effects)

        # 敵機と自期の衝突判定
        Conflict.hit_ss_and_enemy(s_ship=s_ship, enemies=enemies, effects=effects)
        if s_ship.hp <= 0:
            cls.lose_game()

    @classmethod
    def game_over(cls, screen: pygame.surface.Surface, effects: list[Effect], s_ship: StarShip, tmr: int) -> None:
        match tmr:
            case 1:
                pygame.mixer.music.stop()
            case n if n < 90:
                if tmr%8 == 0: SE_DAMAGE.play()
                if tmr%5 == 0: effects.append(Effect(x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery, hldgs=effects))
                s_ship.draw(screen=screen, tmr=tmr)
            case 120:
                adjusted_bgm(file="sound_gl/gameover.ogg", loops=0)
            case n if n < 300:
                draw_text(screen, "GAME OVER", 480, 300, 80, RED)
            case 300:
                cls.return_title()
                
    @classmethod
    def game_clear(cls, screen: pygame.surface.Surface, key: pygame.key.ScancodeWrapper, s_ship: StarShip, tmr: int) -> None:
        '''mainのwhileループが肥大化していたのでgame_clearの特有処理部分を切り出し。
        
        クリア描画が終わった際にidxとtmrを書き換える為にcall関数を受け取る。'''
        # 自機の移動と描画
        s_ship.move(key=key)
        s_ship.draw(screen=screen, tmr=tmr)
        match tmr:
            case 1:
                pygame.mixer.music.stop()
            case 2:
                adjusted_bgm(file="sound_gl/gameclear.ogg", loops=0)
            case n if 20 < n and n < 300:
                draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER)
            case 300:
                cls.return_title()

