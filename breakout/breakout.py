"""
Breakout(ブロック崩し)
"""
import sys
from random import randint
from math import sin, cos
import pygame as pg

W, H = 600, 800
ROWS, COLS = 6, 10             # number of blocks
POINTS = [10, 9, 7, 5, 3, 1]   # points for each ROWS
COLORS = ['red', 'orange', 'yellow', 'green', 'purple', 'blue']
BALL_SPEED = 8

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

pg.mixer.init()
sound = pg.mixer.Sound("sounds/pa.mp3")

def draw_text(x, y, txt, size=80, color='white'):
    font = pg.font.SysFont(None, size)
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))

def new_ball():
    r = randint(45, 135) * 3.14 / 180
    vx, vy = BALL_SPEED * cos(r), BALL_SPEED * sin(r)
    rect = pg.Rect(W//2, 300, 6, 6)
    return rect, vx, vy

_wid, _hi = W // COLS, 150 // ROWS
blocks = []
for r in range(ROWS):
    for c in range(COLS):
        blocks.append(pg.Rect(c * _wid, 60 + r * _hi, _wid - 1, _hi - 1))
is_alive = [True] * len(blocks)

paddle = pg.Rect(W // 2, H - 20, 60, 7)
ball, ball_vx, ball_vy = new_ball()

score = 0
num_balls = 3
game_over = False
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    move = 0
    if keys[pg.K_LEFT]:
        move = -7
    elif keys[pg.K_RIGHT]:
        move = 7
    if 0 <= paddle.left + move and paddle.right + move <= W:
        paddle.move_ip(move, 0)

    ball.move_ip(ball_vx, ball_vy)
    if ball.left <= 0 or W <= ball.right:
        ball_vx = -ball_vx
    if ball.top <= 0:
        ball_vy = -ball_vy
    if not game_over and ball.bottom >= H:
        num_balls -= 1
        if num_balls == 0:
            game_over = True
        else:
            pg.time.wait(1000)
            ball, ball_vx, ball_vy = new_ball()

    if ball_vy > 0 and ball.colliderect(paddle):
        offset = (ball.centerx - paddle.centerx) / (paddle.width / 2)
        angle = offset * 3.14 / 2 * 0.7
        ball_vx, ball_vy = BALL_SPEED * sin(angle), -BALL_SPEED * cos(angle)
        sound.play()

    for i, block in enumerate(blocks):
        if is_alive[i] and ball.colliderect(block):
            is_alive[i] = False
            score += POINTS[i//COLS]
            ball_vy = -ball_vy
            sound.play()
            if sum(is_alive) == 0:
                game_over = True
            break

    screen.fill('black')
    for i, block in enumerate(blocks):
        if is_alive[i]:
            pg.draw.rect(screen, COLORS[i // COLS], block)
    draw_text(150, 7, f'{score:03}', 70, 'silver')
    draw_text(450, 7, f'{num_balls}', 70, 'silver')
    pg.draw.rect(screen, 'yellow', paddle)
    pg.draw.rect(screen, 'white', ball)

    if game_over:
        if sum(is_alive) == 0:
            draw_text(100, H//2, 'GOOD JOB!', 95)
        else:
            draw_text(100, H//2, 'GAME OVER', 95)

    pg.display.update()
    clock.tick(50)