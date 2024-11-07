"""
Simple Pong game
"""
import sys
import pygame as pg

W, H = 400, 300

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

pg.mixer.init()
sound = pg.mixer.Sound('sounds/pong.wav')

def new_ball():
    ball = pg.Rect(W - 50, H // 2, 6, 6)
    vx, vy = 5, 3
    return ball, vx, vy

paddle = pg.Rect(10, H // 2, 5, 40)
ball, ball_vx, ball_vy = new_ball()

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        paddle.move_ip(0, -10)
    if keys[pg.K_DOWN]:
        paddle.move_ip(0, 10)
    
    if ball.right >= W:
        ball_vx = -ball_vx
    if ball.top <= 0 or ball.bottom >= H:
        ball_vy = -ball_vy
    ball.move_ip(ball_vx, ball_vy)

    if ball_vx < 0 and ball.colliderect(paddle):
        ball_vx = -ball_vx
        sound.play()

    if ball.left < 0:
        pg.time.wait(1000)
        ball, ball_vx, ball_vy = new_ball()

    screen.fill('darkgreen')
    pg.draw.rect(screen, 'skyblue', paddle)
    pg.draw.rect(screen, 'white', ball)
    pg.display.update()
    clock.tick(30)