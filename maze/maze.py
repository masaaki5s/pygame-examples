import sys
from random import sample
import pygame as pg

VIEW = 10              # 現在地（中心）から見える距離
GRIDS = VIEW * 4 + 1   # 迷路のグリッド数（奇数になるようにすること）
SIZE = 20              # グリッドのピクセル数

def draw_text(x, y, txt, size=80, color='white'):
    font = pg.font.SysFont(None, size)
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))


def create_maze(w, h):
    maze = [[1]*w for _ in range(h)]
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    def dig(x, y):
        maze[y][x] = 0
        random_directions = sample(directions, 4)
        for dx, dy in random_directions:
            xx, yy = x + dx * 2, y + dy * 2
            if (0 <= xx < w) and (0 <= yy < h) and (maze[yy][xx] == 1):
                maze[y + dy][x + dx] = 0
                dig(xx, yy)
    dig(1, 1)
    maze[1][0] = 0                  # 入口
    maze[h-2][w-1] = 0              # 出口
    return maze, (0, 1), (w-1, h-2)


def get_move(x0, y0, maze):
    MOVE = {pg.K_LEFT:(-1, 0), pg.K_RIGHT:(1, 0), pg.K_UP:(0,-1), pg.K_DOWN:(0,1)}
    keys = pg.key.get_pressed()
    for k in MOVE:
        if keys[k]:
            dx, dy = MOVE[k]
            x, y = x0 + dx, y0 + dy
            if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
                if maze[y][x] == 0:
                    return x, y
    return x0, y0


def display_maze(x, y, maze):
    screen.fill('darkgreen')
    for h in range(VIEW*2+1):
        for w in range(VIEW*2+1):
            xx, yy = x - VIEW + w, y - VIEW + h
            if 0 <= xx < GRIDS and 0 <= yy < GRIDS:
                color = 'white' if maze[yy][xx] == 0 else 'black'
                pg.draw.rect(screen, color, (w * SIZE, h * SIZE, SIZE, SIZE))
    pg.draw.rect(screen, 'red', (VIEW * SIZE, VIEW * SIZE, SIZE, SIZE))

pg.init()
W, H = SIZE * (VIEW * 2 + 1), SIZE * (VIEW * 2 + 1)
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

maze, (x, y), (goal_x, goal_y) = create_maze(GRIDS, GRIDS)
goal = False
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if not goal:
        x, y = get_move(x, y, maze)
        if (x, y) == (goal_x, goal_y):
            goal = True
    display_maze(x, y, maze)
    if goal:
        draw_text(30, 100, 'GOAL!', 160, 'orange')

    pg.display.flip()
    clock.tick(10)