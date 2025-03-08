""" テトリスゲーム """
import sys
from random import randint
import pygame as pg

block_size = 30
x_cells, y_cells = 12, 21     # 横幅は カベ + 10 + カベ
ticks_to_fall = 10

block_type = (
    ((0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0), (0, 1, 0, 0)), # I
    ((2, 2), (2, 2)),                  # O
    ((0, 3, 3), (3, 3, 0), (0, 0, 0)), # S
    ((4, 4, 0), (0, 4, 4), (0, 0, 0)), # Z
    ((5, 0, 0), (5, 5, 5), (0, 0, 0)), # L
    ((0, 0, 6), (6, 6, 6), (0, 0, 0)), # J
    ((0, 7, 0), (7, 7, 7), (0, 0, 0)), # T
    )
color_map = ['black', 'skyblue', 'yellow', 'green', 
        'red', 'blue', 'orange', 'purple', 'darkgray']

def draw_text(x, y, txt, size=60, color='white'):
    font = pg.font.SysFont(None, size)
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))

def generate_block():
    block = block_type[randint(0, 6)]
    return block, x_cells//2, 0

def can_move(b, x, y):
    for i in range(len(b)):
        for j in range(len(b)):
            if b[i][j] != 0 and grid[y+i][x+j]:
                return False
    return True        

def draw_grid():
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            col = color_map[grid[i][j]]
            pg.draw.rect(screen, col, (j*block_size, i*block_size, 
                                       block_size-1, block_size-1))

def draw_block(b, x, y):
    for i in range(len(b)):
        for j in range(len(b)):
            if b[i][j] and grid[y+i][x+j] == 0:
                sx, sy = (x + j) * block_size, (y + i) * block_size
                pg.draw.rect(screen, color_map[b[i][j]], 
                             (sx, sy, block_size-1, block_size-1))

def rotate(b, x, y):
    ret = [[0]*len(b) for _ in range(len(b))]
    for i in range(len(b)):
        for j in range(len(b)):
            ret[i][j] = b[j][len(b) - 1 - i]
    if can_move(ret, x, y):
        return ret
    return b

def initial_grid():
    grid = []
    for _ in range(y_cells-1):
        grid.append([8] + [0]*(x_cells-2) + [8])
    grid.append([8] * x_cells)
    return grid

pg.init()
screen = pg.display.set_mode((block_size * x_cells, block_size * y_cells))
clock = pg.time.Clock()
pg.key.set_repeat(200, 300)

grid = initial_grid() 
block, x, y = generate_block()
ticks = 0
gameover = False
score = 0
while True:
    dx = 0
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_RIGHT:
                dx = 1
            elif e.key == pg.K_LEFT:
                dx = -1
            elif e.key == pg.K_SPACE:
                block = rotate(block, x, y)

    if can_move(block, x+dx, y):            #  ブロックの横移動
        x += dx
    
    if not gameover and ticks % ticks_to_fall == 0:   # ブロックの落下
        if can_move(block, x, y+1):
            y += 1
        else:
            for i in range(len(block)):     # ブロックが落下停止
                for j in range(len(block)):
                    if block[i][j]:
                        grid[y + i][x + j] = block[i][j]

            block, x, y = generate_block()
            if not can_move(block, x, y):   # ゲームオーバー
                gameover = True

    grid_copy = initial_grid()              # グリッドの圧縮
    target = y_cells-2                     
    for i in range(y_cells-2, -1, -1):      # 一番下の行から順番に
        if 0 in grid[i][1:x_cells-1]:       # 0(空白)がある行だけコピー
            grid_copy[target] = grid[i]
            target -= 1
        else:
            score += 10
    grid = grid_copy

    draw_grid()
    draw_text(50, 10, f'SCORE: {score}', size=20)
    if not gameover:
        draw_block(block, x, y)
    else:
        draw_text(50, 300, 'GAME OVER')

    pg.display.flip()
    clock.tick(30)
    ticks += 1