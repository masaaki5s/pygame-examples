import random
import pygame as pg
import utils


class Sprite:
    def __init__(self, sprite_id, x, y, maze):
        self.maze = maze
        self.x = x                     # 迷路のマスの位置（横）
        self.y = y                     # 　　　　　　　　（縦）
        self.dir = (1, 0)              # 進行方向
        self.sprite_idx = 0            # 表示画像のインデックス
        self.sprite = utils.get_sprite(sprite_id, 32, 32)

    def update(self):
        if self.maze.is_walkable(self.x, self.y, self.dir):
            self.x += self.dir[0]     # スプライトの中心位置を移動
            self.y += self.dir[1]        
        self.sprite_idx = (self.sprite_idx + 1) % len(self.sprite[(0,1)])

    def draw(self, surf):
        s = self.sprite[self.dir][self.sprite_idx]
        rect = s.get_rect()
        rect.centerx = self.x * self.maze.size + self.maze.size//2
        rect.centery = self.y * self.maze.size + self.maze.size//2
        surf.blit(s, (rect.left, rect.top))


class Pacman(Sprite):
    def __init__(self, sprite_id, x, y, maze):
        super().__init__(sprite_id, x, y, maze)

    def update(self):
        dirs = {pg.K_LEFT:(-1, 0), pg.K_RIGHT:(1, 0), pg.K_UP:(0, -1), pg.K_DOWN:(0, 1)}
        keys = pg.key.get_pressed()
        for k in dirs:
            if keys[k]:
                self.dir = dirs[k]
        super().update()        
