import pygame as pg
import utils
from assets.data import Map_01


class Maze:
    def __init__(self, width, height):
        self.bg_image = utils.get_sprite('maze', width, height)
        self.food_s = utils.get_sprite('food_s', 8, 8)
        self.food_l = utils.get_sprite('food_l', 12, 12)
        self.maze = [[c for c in Map_01[i]] for i in range(len(Map_01))]
        self.size = 16


    def draw(self, surf):
        surf.blit(self.bg_image, (0, 0))
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
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
        

