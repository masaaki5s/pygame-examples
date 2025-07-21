import sys
import pygame as pg

from sprites import Pacman, Ghost
from maze import Maze

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

maze = Maze()
pacman = Pacman('pacman', 0, 14, maze)
red_ghost = Ghost('red', 12, 14, maze)

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
    clock.tick(10)
