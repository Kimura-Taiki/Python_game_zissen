import pygame
from typing import Callable

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.starship import StarShip
from mod.effect import Effect
from mod.sound import SE_DAMAGE, adjusted_bgm
from mod.title import draw_text, RED, SILVER

def game_over(screen: pygame.surface.Surface, effects: list[Effect], s_ship: StarShip, tmr: int, call: Callable[[], None]) -> None:
    match tmr:
        case 1:
            pygame.mixer.music.stop()
        case n if n <= 90 and n%5 == 0:
            SE_DAMAGE.play()
            effects.append(Effect(x=s_ship.craft.rect.centerx, y=s_ship.craft.rect.centery, hldgs=effects))
        case n if n < 90:
            s_ship.draw(screen=screen, tmr=tmr)
        case 120:
            adjusted_bgm(file="sound_gl/gameover.ogg", loops=0)
        case n if 120 < n and n < 300:
            draw_text(screen, "GAME OVER", 480, 300, 80, RED)
        case 300:
            call()

def game_clear(screen: pygame.surface.Surface, key: pygame.key.ScancodeWrapper, s_ship: StarShip, tmr: int, call: Callable[[], None]) -> None:
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
            call()

