import pygame
pygame.init()
from random import randint

from os.path import dirname
import sys
if __name__ == '__main__': sys.path.append(dirname(dirname(__file__)))
from mod.enemy import Enemy


class EnemyFactory():
    def no_func():
        pass

    DEFAULT_PARAMS = (('name', None), ('speed', 6), ('angle', 90), ('breakable', True), ('fire', no_func))

    def __init__(self, dict) -> None:
        self.img = pygame.image.load(dict['img'])
        for tuple in self.DEFAULT_PARAMS:
            if tuple[0] in dict.keys():
                setattr(self, tuple[0], dict[tuple[0]])
            else:
                setattr(self, tuple[0], tuple[1])
    
    def print(self):
        print(self.name, self.img, self.speed, self.angle, self.breakable, self.fire)

    def make(self, x, y, dict={}) -> Enemy:
        enemy = Enemy(x=x, y=y)
        enemy.img2 = self.img
        for tuple in self.DEFAULT_PARAMS:
            setattr(enemy, tuple[0], getattr(self, tuple[0]))
        for tuple in dict:
            setattr(enemy, tuple[0], tuple[1])
        return enemy
    
    @classmethod
    def bring_enemy(cls, enemies, tmr): # 敵を出す
        if tmr%30 == 0:
            enemies.append(torpedoer.make(x=randint(20, 940), y=Enemy.LINE_T))
    
def torpedo_run(enemy: Enemy): # 弾を発射する、母機の処理にのみ弾の発射機構を追加する
    if enemy.y > 360:
        enemy.enemies.append(torpedo.make(x=enemy.x, y=enemy.y))
        enemy.angle = -45
        enemy.speed = 16

torpedoer = EnemyFactory({'img':"image_gl/enemy1.png",    'name':"Torpedoer", 'fire':EnemyFactory.no_func})
# torpedoer = EnemyFactory({'img':"image_gl/enemy1.png",    'name':"Torpedoer", 'fire':torpedo_run})
torpedo = EnemyFactory({'img':"image_gl/enemy0.png",    'name':"Torpedo",   'speed':10, 'breakable':False})



tac = EnemyFactory({'img':"image_gl/enemy1.png",    'name':"Torpedoer", 'fire':torpedo_run})
tpd = EnemyFactory({'img':"image_gl/enemy0.png",    'name':"Torpedo",   'speed':10, 'breakable':False})
print(tac, tpd)
tac.print()
tpd.print()
i = tac.make(x=30, y=40)
print(i, type(i))
print(i.name, i.img2, i.x, i.y, i.speed, i.angle, i.breakable, i.fire)