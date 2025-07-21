import pygame as pg
import utils
from assets.data import Map_01


class Maze:
    def __init__(self):
        self.maze = [[c for c in row] for row in Map_01]
        self.cols = len(self.maze[0])        # 迷路のマス数（横）
        self.rows = len(self.maze)           #           （縦）
        self.size = 16                       # マスのサイズ（画素数）
        self.width = self.size * self.cols   # 迷路画像の横幅
        self.height = self.size * self.rows  # 迷路画像の高さ
        self.bg_image = utils.get_sprite('maze', self.width, self.height)
        self.food_s = utils.get_sprite('food_s', 8, 8)    # エサ(小)
        self.food_l = utils.get_sprite('food_l', 12, 12)  # エサ(大)


    def draw(self, surf):
        surf.blit(self.bg_image, (0, 0))
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == '1':
                    self._centering(surf, self.food_s, c, r)
                if self.maze[r][c] == '2':
                    self._centering(surf, self.food_l, c, r)


    def _centering(self, surf, s, c, r):
        """ セルの中心になるように画像を貼り付ける """
        rect = s.get_rect()
        rect.centerx = c * self.size + self.size//2
        rect.centery = r * self.size + self.size//2
        surf.blit(s, (rect.left, rect.top))


    def is_walkable(self, x, y, dir):
        """ 通路以外は移動できないようにチェックする """
        xx, yy = x+dir[0], y+dir[1]
        if (0 <= xx < self.cols and 0 <= yy < self.rows):
            if self.maze[yy][xx] != '#':
                return True
        return False
