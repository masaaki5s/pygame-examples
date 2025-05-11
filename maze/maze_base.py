import sys
from random import sample
import pygame as pg


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
    maze[1][0] = 0                          # 入口
    maze[GRIDS-2][GRIDS-1] = 0              # 出口
    return maze, (0, 1), (GRIDS-1, GRIDS-2)

def get_move(x0, y0, maze):
    """ 完成させてください """
    pass


def display_maze(x, y, maze):
    screen.fill('darkgreen')
    for h in range(VIEW*2+1):
        for w in range(VIEW*2+1):
            xx, yy = x - VIEW + w, y - VIEW + h
            if 0 <= xx < GRIDS and 0 <= yy < GRIDS:
                color = 'white' if maze[yy][xx] == 0 else 'black'
                pg.draw.rect(screen, color, (w * SIZE, h * SIZE, SIZE, SIZE))
    pg.draw.rect(screen, 'red', (VIEW * SIZE, VIEW * SIZE, SIZE, SIZE))


VIEW = 10              # 現在地（中心）から見える距離
GRIDS = VIEW * 4 + 1   # 迷路のグリッド数（奇数になるようにすること）
SIZE = 20              # グリッドのピクセル数
W, H = SIZE * (VIEW * 2 + 1), SIZE * (VIEW * 2 + 1) # 画面サイズ

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

# 以下の処理を完成させてください
# 迷路を作成（create_mazeを呼ぶ）

# ゴール済み（ゲームオーバー）のフラグを初期化する

# PyGameのメインループをはじめる
    # イベントループを書く
        # e.typeがpg.QUITならばプログラムを終了する

    # もし「ゴール済み」じゃないなら
        # get_move関数を呼んで新しいグリッド位置を得る
        # もし，新しい位置がゴールなら
            # ゴール済みフラグをTrueにする
    
    # display_maze関数を呼んで迷路を描画する

    # もし「ゴール済み」なら
        # draw_text関数を使ってGOAL! のメッセージ出力

    # 画面の更新のための次の関数を忘れないように書く
    # pg.display.flip()
    # clock.tick(10)