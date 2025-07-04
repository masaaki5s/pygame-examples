import pygame as pg
import utils


class Sprite:
    def __init__(self, sprite_id, x, y, speed=3):
        self.x = x                     # X座標
        self.y = y                     # Y座標
        self.dir = (1, 0)              # 進行方向
        self.sprite_idx = 0            # 表示画像のインデックス
        self.speed = speed             # 移動速度
        self.sprite = utils.get_sprite(sprite_id, 32, 32)

    def update(self):
        self.sprite_idx = (self.sprite_idx + 1) % len(self.sprite[(0,1)])

    def draw(self, surf):
        surf.blit(self.sprite[self.dir][self.sprite_idx], (self.x, self.y))


class Pacman(Sprite):
    def __init__(self, sprite_id, x, y, speed=3):
        super().__init__(sprite_id, x, y, speed)

    def update(self):
        dirs = {pg.K_LEFT:(-1, 0), pg.K_RIGHT:(1, 0), pg.K_UP:(0, -1), pg.K_DOWN:(0, 1)}
        keys = pg.key.get_pressed()
        for k in dirs:                             # 矢印キーに応じて方向を変える
            if keys[k]:
                self.dir = dirs[k]

        self.x += self.dir[0] * self.speed         # パックマンの中心位置を移動
        self.y += self.dir[1] * self.speed
        self.sprite_idx = (self.sprite_idx + 1) % 3