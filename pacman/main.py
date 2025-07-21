import sys
import pygame as pg

from sprites import Pacman, Ghost
from maze import Maze

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

pacman = Pacman('pacman', 100, 200, 2)
red_ghost = Ghost('red', 300, 300, 3)
maze = Maze(224*2, 248*2)    # TODO: ドットサイズをMazeに隠蔽すること

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pacman.update()
    red_ghost.update()

    screen.fill('black')
    maze.draw(screen)
    pacman.draw(screen)
    red_ghost.draw(screen)
    pg.display.flip()
    clock.tick(15)
