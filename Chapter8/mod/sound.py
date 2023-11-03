import pygame

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
