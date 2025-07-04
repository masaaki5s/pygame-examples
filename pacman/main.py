import sys
import pygame as pg

from sprites import Pacman

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

pacman = Pacman('pacman', 100, 200, 2)

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pacman.update()

    screen.fill('black')
    pacman.draw(screen)
    pg.display.flip()
    clock.tick(15)
