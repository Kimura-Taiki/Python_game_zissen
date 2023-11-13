import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_z
from functools import partial
import sys
from typing import Any, Callable, Literal, ClassVar, Optional, Final
from math import cos, sin, radians
from random import randint, choice

pygame.init()

def quit_event() -> None:
    pygame.quit()
    sys.exit()

event_mapping: list[dict[str, Any]] = [{"type":pygame.QUIT,                            "func":quit_event}]

def solve_event(mapping: list[dict[str, Any]]) -> None:
    for event in pygame.event.get():
        for map in mapping:
            if event.type == map["type"] and (event.type != pygame.KEYDOWN or event.key == map["key"]):
                map["func"]()
                break

WIN_X: int = 960
WIN_Y: int = 720
WIN_SIZE: tuple[int, int] = (WIN_X, WIN_Y)

pygame.display.set_caption("Galaxy Lancer")
screen: pygame.surface.Surface = pygame.display.set_mode(WIN_SIZE)

def fullscreen_event(screen: pygame.surface.Surface, size: tuple[int, int]) -> None:
    screen = pygame.display.set_mode(size=size, flags=pygame.FULLSCREEN)

def windowed_event(screen: pygame.surface.Surface, size: tuple[int, int]) -> None:
    screen = pygame.display.set_mode(size=size)

event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F1,      "func":partial(fullscreen_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_F2,      "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})
event_mapping.append({"type":pygame.KEYDOWN, "key":pygame.K_ESCAPE,  "func":partial(windowed_event, screen=screen, size=WIN_SIZE)})

# 背景関連の処理をBackGroundクラスへ集約
class BackGround():
    bg_y: int = 0
    IMG_GALAXY: pygame.surface.Surface = pygame.image.load("image_gl/galaxy.png")
    
    @classmethod
    def scroll(cls, speed: int) -> None:
        BackGround.bg_y = (BackGround.bg_y+speed)%WIN_Y

    @classmethod
    def draw(cls, screen: pygame.surface.Surface) -> None:
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y-WIN_Y])
        screen.blit(BackGround.IMG_GALAXY, [0, BackGround.bg_y])

class Sprite(pygame.sprite.Sprite):
    image: pygame.surface.Surface
    '''Group.drawを稼働させる為の画像情報です。'''
    angle: int
    '''回転量を度数法で表します。
    0で右、90で下、以下360でまた右に戻ります。'''
    nega: pygame.surface.Surface
    '''回転時に画像の原板となる画像情報です。'''
    rect: pygame.rect.Rect
    '''Group.drawを稼働させる為の矩形情報です。'''

    def __init__(self, group: Any, image: pygame.surface.Surface, cx: int, cy: int) -> None:
        super().__init__(group)
        self.image = image
        self.nega = image
        self.rect = pygame.rect.Rect(
            cx-int(self.image.get_width()/2), cy-int(self.image.get_height()/2),
            self.image.get_width(), self.image.get_height())

    def roll_image(self, angle: int|None=None) -> None:
        '''画像をangleに応じて回転'''
        x, y = self.x, self.y
        self.image = pygame.transform.rotozoom(surface=self.nega, angle=-90-self.angle if angle is None else -90-angle, scale=1.0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    @property
    def x(self) -> Any:
        return self.rect.centerx

    @x.setter
    def x(self, value: int) -> None:
        self.rect.centerx = value

    @property
    def y(self) -> Any:
        return self.rect.centery

    @y.setter
    def y(self, value: int) -> None:
        self.rect.centery = value

class Effect(Sprite):
    IMG_EXPLODE: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/explosion1.png"),
        pygame.image.load("image_gl/explosion2.png"),
        pygame.image.load("image_gl/explosion3.png"),
        pygame.image.load("image_gl/explosion4.png"),
        pygame.image.load("image_gl/explosion5.png")
    ]
    
    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.IMG_EXPLODE[0], cx=x, cy=y)
        self.angle: int = 90
        self.hldgs: list[Effect] = hldgs
        self.duration: int = 0
    
    def elapse(self, t: int =1) -> Optional[bool]:
        '''時間経過をさせます。
        
        この命令はリスト内表記で繰り返し処理する際にmypyで弾かれぬべく、
        戻り値の型ヒントにOptional[bool]を与えてあります。'''
        self.duration += t
        if self.duration >= 5:
            self.hldgs.remove(self)
        else:
            self.image = self.IMG_EXPLODE[self.duration]
        return None

class StarShip():
    # 画像の読み込み
    IMG_SSHIP: list[pygame.surface.Surface] = [
        pygame.image.load("image_gl/starship.png"),
        pygame.image.load("image_gl/starship_l.png"),
        pygame.image.load("image_gl/starship_r.png"),
        pygame.image.load("image_gl/starship_burner.png")
    ]
    IMG_SHIELD: pygame.surface.Surface = pygame.image.load("image_gl/shield.png")
    DEFAULT_X: int = 480
    DEFAULT_Y: int = 600
    V = 20
    MOVE_MAPPING = (0, -V, V, 0)
    ROLL_MAPPING = (0,  1, 2, 0)
    MAX_HP = 100

    def __init__(self) -> None:
        self.group: Any = pygame.sprite.Group()
        self.craft: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[0], cx=self.DEFAULT_X, cy=self.DEFAULT_Y)
        self.burner: Sprite = Sprite(group=self.group, image=self.IMG_SSHIP[3], cx=self.DEFAULT_X, cy=self.DEFAULT_Y+56)
        self._hp: int = self.MAX_HP
        self.muteki: int = 0

    def move(self, key: pygame.key.ScancodeWrapper) -> None: # 自機の移動
        self.craft.image = self.IMG_SSHIP[self.ROLL_MAPPING[key[K_LEFT]+key[K_RIGHT]*2]]
        self.craft.rect.centerx = min(max(self.craft.rect.centerx+self.MOVE_MAPPING[key[K_LEFT]+key[K_RIGHT]*2], 40), 920)
        self.craft.rect.centery = min(max(self.craft.rect.centery+self.MOVE_MAPPING[key[K_UP]+key[K_DOWN]*2], 80), 640)
        self.burner.rect.center = self.craft.rect.centerx, self.craft.rect.centery+56

    def draw(self, screen: pygame.surface.Surface, tmr: int=0) -> None:
        if self.muteki%2 != 0: return
        self.group.draw(screen)

    def reset(self) -> None:
        self.craft.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.burner.rect.center = (self.DEFAULT_X, self.DEFAULT_Y)
        self.hp = self.MAX_HP
        self.muteki = 0
    
    def shield_draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(source=self.IMG_SHIELD, dest=(40, 680))
        pygame.draw.rect(surface=screen, color=(64,32,32), rect=[40+self.hp*4, 680, (100-self.hp)*4, 12])

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = min(self.MAX_HP, max(0, value))

class Bullet(Sprite):
    IMG_WEAPON = pygame.image.load("image_gl/bullet.png")
    SPEED = 36

    def __init__(self, x: int, y: int, angle: int=270, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.IMG_WEAPON, cx=x, cy=y)
        self.angle: int = angle
        self.roll_image()
        self.hldgs: list[Bullet] = hldgs

    def elapse(self) -> Literal[False]:
        '''Bulletをangleに従って直線運動させます。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        self.rect.centerx += int(self.SPEED*cos(radians(self.angle)))
        self.rect.centery += int(self.SPEED*sin(radians(self.angle)))
        if self.rect.centery < 0 or self.rect.centerx < 0 or self.rect.centerx > 960:
            self.hldgs.remove(self)
        return False

class Enemy(Sprite):
    LINE_T: int = -80
    LINE_B: int = 800
    LINE_L: int = -80
    LINE_R: int = 1040

    DEFAULT_IMG: pygame.surface.Surface = pygame.image.load("image_gl/enemy1.png")

    @staticmethod
    def pass_func(enemy: Any=None) -> None:
        pass

    def _not_implemented_shot_down(self) -> None: raise NotImplementedError("Enemy.shot_down_funcが未実装\n被撃墜時の命令が設定されていません")
    shot_down_func: ClassVar[Callable[['Enemy'], None]] = _not_implemented_shot_down

    def __init__(self, x: int, y: int, hldgs: Any=None) -> None:
        super().__init__(group=[], image=self.DEFAULT_IMG, cx=x, cy=y)
        self.hldgs: list[Enemy] = hldgs
        self.name: str = "----"
        self.speed: int = 6
        self.angle: int = 90
        self.breakable: bool = True
        self.is_boss: bool = False
        self.flash_duration: int = 0
        self.hp: int = 1
        self.timer: int = 0
        self.mode: int = 0
        self.elapse_func: Callable[[Enemy], None] = self.move_linearly
        self.fire: Callable[[Enemy], None] = self.pass_func

    def elapse(self) -> Literal[False]:
        '''Enemyをangleに従って直線運動させます。

        リスト内包表記で繰り返し処理する際に戻り値が無いとエラーを起こす為、
        戻り値にFalseを与えてあります。'''
        (self.elapse_func)(self)
        if self.flash_duration > 0:
            self.flash_duration -= 1
            if self.flash_duration == 0:
                self.image = self.nega
                self.roll_image(angle=90)
        (self.fire)(self)
        if self.x < self.LINE_L or self.LINE_R < self.x or self.y < self.LINE_T or self.LINE_B < self.y:
            self.hldgs.remove(self)
        return False

    def damaged(self, damage: int, effects: list[Effect]) -> None:
        '''Enemyの被弾時処理です。
        
        Conflict側で抱えてしまうと被弾時処理が嵩張りがち且つ敵個体毎に処理が変わる為、
        Enemyクラスに被弾時処理を委譲しています。'''
        effects.append(self.internal_explosion(effects=effects))
        SE_EXPLOSION.play()
        if self.is_boss:
            self.flash_duration = 3
            self.image = pygame.transform.rotozoom(surface=pygame.image.load("image_gl/enemy_boss_f.png"), angle=180, scale=1.0)
        self.hp -= damage
        if self.hp <= 0:
            self.shot_down_func()
            self.hldgs.remove(self)

    def internal_explosion(self, effects: list[Effect]) -> Effect:
        '''敵機のランダム位置で発生する爆風を返します。'''
        dx, dy = int(self.rect.w/2), int(self.rect.h/2)
        return Effect(x=self.x+randint(-dx, dx), y=self.y+randint(-dy, dy), hldgs=effects)

    @classmethod
    def move_linearly(cls, enemy: 'Enemy') -> None:
        '''デフォルトの敵機運動としてself.elapseへ代入されている命令です。
        単純な等速直線運動を行います。'''
        enemy.x += enemy.speed*cos(radians(enemy.angle))
        enemy.y += enemy.speed*sin(radians(enemy.angle))

BLACK = (  0,   0,   0)
SILVER= (192, 208, 224)
RED   = (255,   0,   0)
CYAN  = (  0, 224, 255)


class Title():
    @staticmethod
    def __nie_start_game() -> None: raise NotImplementedError("Title.start_gameが未実装\nスタート時の初期化命令が設定されていません")
    start_game: Callable[[], None] = __nie_start_game

    IMG_TITLE = [
        pygame.image.load("image_gl/nebula.png"),
        pygame.image.load("image_gl/logo.png")
    ]

    @classmethod
    def title(cls, screen :pygame.surface.Surface, key :pygame.key.ScancodeWrapper, tmr: int) -> None:
        img_rz = pygame.transform.rotozoom(cls.IMG_TITLE[0], -tmr%360, 1.0)
        screen.blit(img_rz, [480-img_rz.get_width()/2, 280-img_rz.get_height()/2])
        screen.blit(cls.IMG_TITLE[1], [70, 160])
        draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
        if key[K_SPACE] == True:
            cls.start_game()

def draw_text(screen: pygame.surface.Surface,
              text: str, x: int, y: int, size: int, col: tuple[int, int, int]) -> None:
    '''文字を表示する命令です。'''
    font = pygame.font.Font(None, size)
    cx, cy = int(x-font.render(text, True, col).get_width()/2), int(y-font.render(text, True, col).get_height()/2)
    screen.blit(source=font.render(text, True, [int(i/2) for i in col]), dest=[cx+1, cy+1])
    screen.blit(source=font.render(text, True, [i+128 if i < 128 else 255 for i in col]), dest=[cx-1, cy-1])
    screen.blit(source=font.render(text, True, col), dest=[cx, cy])

vol_bgm = 0.1
vol_se = 0.1

def adjusted_sound(file: str, volume: float = vol_se) -> pygame.mixer.Sound:
    sound = pygame.mixer.Sound(file=file)
    sound.set_volume(volume)
    return sound

def adjusted_bgm(file: str, loops:int = 0, volume: float = vol_bgm) -> None:
    pygame.mixer.music.load(filename=file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=loops)

SE_BARRAGE = adjusted_sound(file="sound_gl/barrage.ogg")
SE_DAMAGE = adjusted_sound(file="sound_gl/damage.ogg")
SE_EXPLOSION = adjusted_sound(file="sound_gl/explosion.ogg")
SE_SHOT = adjusted_sound(file="sound_gl/shot.ogg")

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

class EnemyFactory():
    def __init__(self, **kwargs: Any) -> None:
        self._DIFFS: Final[dict[str, Any]] = kwargs

    def make(self, x: int, y: int, hldgs: list[Enemy], **kwargs: Any) -> Enemy:
        enemy = Enemy(x=x, y=y, hldgs=hldgs)
        for key, value in self._DIFFS.items():
            setattr(enemy, key, value)
        for key, value in kwargs.items():
            setattr(enemy, key, value)
        enemy.roll_image()
        return enemy

    @classmethod
    def bring_enemy(cls, enemies: list[Enemy], tmr: int) -> None:
        match tmr:
            case _ if 0 < tmr and tmr < 25*30 and tmr % 15 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 30*30 < tmr and tmr < 55*30 and tmr % 10 == 0:
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 60*30 < tmr and tmr < 85*30 and tmr % 15 == 0:
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
            case _ if 90*30 < tmr and tmr < 115*30 and tmr % 20 == 0:
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 120*30 < tmr and tmr < 145*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
            case _ if 150*30 < tmr and tmr < 175*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_B, hldgs=enemies, angle=270))
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies, angle=randint(70, 110)))
            case _ if 180*30 < tmr and tmr < 205*30 and tmr % 20 == 0:
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if 210*30 < tmr and tmr < 235*30 and tmr % 20 == 0:
                enemies.append(RED_CRAFT.make(x=Enemy.LINE_L, y=randint(40, 680), hldgs=enemies, angle=0))
                enemies.append(BLUE_CRAFT.make(x=Enemy.LINE_R, y=randint(40, 680), hldgs=enemies, angle=180))
            case _ if 240*30 < tmr and tmr < 265*30 and tmr % 30 == 0:
                enemies.append(RED_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(BLUE_CRAFT.make(x=randint(20, 940), y=Enemy.LINE_T, hldgs=enemies))
                enemies.append(ABATIS.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies, angle=randint(60, 120)))
                enemies.append(PILLBOX.make(x=randint(100, 860), y=Enemy.LINE_T, hldgs=enemies))
            case _ if tmr == 270*30:
                enemies.append(BOSS.make(x=480, y=int(Enemy.LINE_T/2), hldgs=enemies))


def elapse_pillbox(enemy: Enemy) -> None:
    enemy.timer += 1
    if enemy.rect.centery > 240 and enemy.angle == 90:
        enemy.angle = choice([50, 70, 110, 130])
        enemy.hldgs.append(BULLET.make(x=enemy.rect.centerx, y=enemy.rect.centery, hldgs=enemy.hldgs))
    Enemy.move_linearly(enemy=enemy)
    enemy.roll_image(angle=90+enemy.timer*10)

def elapse_boss(enemy: Enemy) -> None:
    enemy.timer += 1
    Enemy.move_linearly(enemy=enemy)
    match enemy.mode:
        case 0:
            if enemy.y >= 200: enemy.mode, enemy.angle = 1, 180
        case 1:
            if enemy.x < 200:
                enemy.hldgs.extend(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=i*20) for i in range(0, 10))
                enemy.mode, enemy.angle = 2, 0
        case 2:
            if enemy.x > 760:
                enemy.hldgs.extend(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=i*20) for i in range(0, 10))
                enemy.mode, enemy.angle = 1, 180
    if enemy.hp < 100 and enemy.timer % 30 == 0: enemy.hldgs.append(BULLET.make(x=enemy.x, y=enemy.y+80, hldgs=enemy.hldgs, angle=randint(60, 120)))


BULLET = EnemyFactory(nega=pygame.image.load("image_gl/enemy0.png"), name="Bullet", speed=6, breakable=False)
RED_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy1.png"), name="RedCraft", speed=8)
BLUE_CRAFT = EnemyFactory(nega=pygame.image.load("image_gl/enemy2.png"), name="BlueCraft", speed=12)
ABATIS = EnemyFactory(nega=pygame.image.load("image_gl/enemy3.png"), name="Abatis", speed=6, hp=3)
PILLBOX = EnemyFactory(nega=pygame.image.load("image_gl/enemy4.png"), name="Pillbox", speed=12, hp=2, elapse_func=elapse_pillbox)
BOSS = EnemyFactory(nega=pygame.image.load("image_gl/enemy_boss.png"), name="Boss", speed=4, hp=200, elapse_func=elapse_boss, is_boss=True)

class Conflict():
    @classmethod
    def hit_bullet_and_enemy(cls, bullets: list[Bullet], enemies: list[Enemy], effects: list[Effect]) -> None:
        for enemy in [enemy for enemy in enemies if enemy.breakable == True][:]:
            hitten: list[Bullet] = pygame.sprite.spritecollide(sprite=enemy, group=pygame.sprite.Group(bullets), dokill=False)
            for bullet in hitten:
                bullet.hldgs.remove(bullet)
                enemy.damaged(damage=1, effects=effects)
                break

    @classmethod
    def hit_ss_and_enemy(cls, s_ship: StarShip, enemies: list[Enemy], effects: list[Effect]) -> None:
        if s_ship.muteki > 0:
            s_ship.muteki -= 1
            return
        hitten: list[Enemy] = pygame.sprite.spritecollide(sprite=s_ship.craft, group=pygame.sprite.Group(enemies), dokill=False)
        if hitten == []: return
        s_ship.muteki = 60 if s_ship.muteki == 0 else s_ship.muteki
        for enemy in hitten[:]:
            effects.append(Effect(x=enemy.x, y=enemy.y, hldgs=effects))
            SE_DAMAGE.play()
            s_ship.hp -= 10
            if not enemy.is_boss:
                enemy.hldgs.remove(enemy)

class ShootBullet():
    '''弾の生成と発射を担うクラスです。

    現時点では単発弾(Single)と拡散弾(Diffusion)が発射できます。このクラスは2つの主要なメソッド、
    single_shotとdiffusion_shotを提供し、それぞれ単発弾と拡散弾の発射を担当します。

    拡散弾の発射には外部からis_diffusion関数とconsume_diffusion関数を再定義する必要があります。
    これにより、拡散弾の発射条件と消費コストを外部からカスタマイズすることができます。

    ## 使用方法:
    1. is_diffusion関数とconsume_diffusion命令を外部で定義します。
    2. single_shotメソッドおよびdiffusion_shotメソッドを呼び出して弾を発射します。

    ## 拡張性:
    このクラスは単発弾と拡散弾の発射に焦点を当てていますが、将来的には新しい弾幕のパターンや
    タイプを追加するために拡張できる構造を提供しています。
    新しい弾幕の追加や既存の挙動の変更は新たなメソッドを追加する事で行ってください。
    '''

    @staticmethod
    def __not_implemented_is_diffusion() -> bool:
        raise NotImplementedError(
            "ShootBullet.is_diffusionが未実装\n拡散弾発射条件が設定されていません")
    is_diffusion: Callable[[], bool] = __not_implemented_is_diffusion
    '''拡散弾のコストを払い得るかを判断する為の関数です。
    is_diffusionは外部から定義、更新される事を想定しています。未更新時に常時エラーを吐くのは想定内です。

    この関数は、拡散弾を発射する前に呼び出され、拡散弾の発射条件が満たされているかを判定します。'''

    @staticmethod
    def __not_implemented_consume_diffusion() -> None:
        raise NotImplementedError(
            "ShootBullet.consume_diffusionが未実装\n拡散弾発射時の消費が設定されていません")
    consume_diffusion: Callable[[], None] = __not_implemented_consume_diffusion
    '''拡散弾を発射した際に、拡散弾のコストを実際に支払う処理を担う関数です。
    consume_diffusionは外部から定義、更新される事を想定しています。未更新時に常時エラーを吐くのは想定内です。

    この関数は、拡散弾を発射した直後に呼び出され、拡散弾の発射に関連するコストを支払います。'''

    _key_space_duration: int = 0
    '''Spaceキーが何フレームの間、押し続けられているかを示します。
    単射時の反応性を保持しつつ、押しっぱなし時の過剰な連射を抑える為に使われています。'''
    _key_z_duration: int = 0
    '''Zキーが何フレームの間、押し続けられているかを示します。
    単射時の反応性を保持しつつ、コストを費やす拡散弾の連射を防ぐ為に使われています。'''
    DIFFUSION_ANGLE_RANGE: range = range(160, 390, 10)

    @classmethod
    def single_shot(cls, pressed_keys: pygame.key.ScancodeWrapper,
                    bullets: list[Bullet], x: int, y: int) -> None:
        '''Spaceキーで単発弾を発射します。'''
        cls._key_space_duration = \
            (cls._key_space_duration+1)*pressed_keys[K_SPACE]
        if cls._key_space_duration % 5 == 1:
            bullets.append(Bullet(x=x, y=y-50, hldgs=bullets))
            SE_SHOT.play()

    @classmethod
    def diffusion_shot(cls, pressed_keys: pygame.key.ScancodeWrapper,
                       bullets: list[Bullet], x: int, y: int) -> None:
        '''Zキーで拡散弾を発射します。

        発射時の消費コストが存在します。消費コストは外部に依存させたいのでdiffusion系の変数に任せています。'''
        cls._key_z_duration = (cls._key_z_duration+1)*pressed_keys[K_z]
        if cls._key_z_duration == 1 and cls.is_diffusion():
            for angle in cls.DIFFUSION_ANGLE_RANGE:
                bullets.append(Bullet(x=x, y=y-50, angle=angle, hldgs=bullets))
            SE_BARRAGE.play()
            cls.consume_diffusion()

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

    def shot_down_enemy(enemy: Enemy) -> None:
        nonlocal score, effects
        s_ship.hp += 1
        score += 100
        if enemy.is_boss:
            effects.extend(enemy.internal_explosion(effects=effects) for i in range(10))
            SE_EXPLOSION.play()
            index_shift(new_idx=3)
    Enemy.shot_down_func = shot_down_enemy

    def start_game() -> None:
        nonlocal score
        index_shift(new_idx=1)
        # index_shift(new_idx=1, new_tmr=180*30) # ボスの確認用ね
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

        # 映像の書き換えと更新周期の設定
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()