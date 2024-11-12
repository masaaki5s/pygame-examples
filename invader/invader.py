"""
インベーダーゲーム
"""
import sys
import pygame as pg
from random import random

W, H = 800, 600
pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
pg.mixer.init()
hit = pg.mixer.Sound('sounds/Hit.wav')
oops = pg.mixer.Sound('sounds/boom.wav')
fire = pg.mixer.Sound('sounds/Pew1.wav')

def draw_text(x, y, text, size=80):
    font = pg.font.SysFont(None, size)
    img = font.render(text, True, 'white')
    screen.blit(img, (x, y))

ROWS, COLS = 5, 11
POINTS = [30, 20, 20, 10, 10]
ALIEN_TYPE = ['tako', 'tako', 'kani', 'kani', 'ika']
ALIEN_W, ALIEN_H = 30, 20
ALIEN_VX, ALIEN_VY = 2, 5
X0, Y0 = 150, 40 
DX, DY = 15, 15
ALIEN_BEAM_VY = 5

images = {}
for alien_type in ['ika', 'kani', 'tako']:
    images[alien_type] = []
    for i in [1, 2]:
        img = pg.image.load(f'images/{alien_type}{i}.png')
        img = pg.transform.scale(img, (ALIEN_W, ALIEN_H))
        images[alien_type].append(img)

aliens = []
for r in range(ROWS):
    for c in range(COLS):
        x = X0 + c * (ALIEN_W + DX)
        y = Y0 + r * (ALIEN_H + DY)
        rect = pg.Rect(x, y, ALIEN_W, ALIEN_H)
        aliens.append(rect)
is_alive = [True] * len(aliens)
alien_beams = []

im = pg.image.load(f'images/ship.png').convert_alpha()
images['fighter'] = pg.transform.scale(im, (40, 25))
fighter = images['fighter'].get_rect(center=(W // 2, H - 50))

my_beam = 0
beam_vy = -10
DEF_LINE = H - 50    # 防衛ライン

ALIEN_FLIP = pg.USEREVENT
pg.time.set_timer(ALIEN_FLIP, 500)

score = 0
num_fighters = 3
game_over = False
direction = 1
alien_gain = 1
img_idx = 0
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if e.type == ALIEN_FLIP:
            img_idx = (img_idx + 1) % 2

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        fighter.move_ip(-3, 0)
    if keys[pg.K_RIGHT]:
        fighter.move_ip(3, 0)
    
    if keys[pg.K_SPACE]:
        if num_fighters > 0 and my_beam == 0:
            my_beam = pg.Rect(fighter.centerx, fighter.top, 3, 10)
            fire.play()

    if my_beam != 0:
        my_beam.move_ip(0, beam_vy)
        if my_beam.top <= 0:
            my_beam = 0

    left, right = W, 0
    for i in range(len(aliens)):
        if is_alive[i]:
            left = min(left, aliens[i].left)
            right = max(right, aliens[i].right)
    if (direction > 0 and right >= W) or (direction < 0 and left <= 0):
        alien_vy = ALIEN_VY
        direction *= -1
        alien_gain += 1
        if alien_gain % 10 == 0:
            ALIEN_VX += 1
    else:
        alien_vy = 0
        
    for i in range(len(aliens)):
        alien = aliens[i]
        alien.move_ip(ALIEN_VX * direction, alien_vy)
        if is_alive[i] and alien.bottom >= DEF_LINE:
            game_over = True
            is_alive[i] = False
        if is_alive[i] and my_beam != 0 and my_beam.colliderect(alien):
            is_alive[i] = False
            score += POINTS[i//COLS]
            my_beam = 0
            hit.play()
        if is_alive[i] and random() < 0.002:
            beam = pg.Rect(alien.centerx, alien.bottom, 3, 10)
            alien_beams.append(beam)
    temp = []
    for beam in alien_beams:
        if game_over:
            break
        beam.move_ip(0, ALIEN_BEAM_VY)
        if beam.bottom < H:
            temp.append(beam)
        if num_fighters > 0 and beam.colliderect(fighter):
            oops.play()
            pg.time.wait(1000)
            my_beam = 0
            num_fighters -= 1
            if num_fighters == 0:
                ALIEN_VX *= 10
                ALIEN_VY *= 5
            temp = []
            break
    alien_beams = temp

    screen.fill('black')

    if num_fighters > 0:
        screen.blit(images['fighter'], fighter)

    if my_beam != 0:
        pg.draw.rect(screen, 'yellow', my_beam)

    for beam in alien_beams:
        pg.draw.rect(screen, 'red', beam)

    for i in range(len(aliens)):
        alien = aliens[i]
        if is_alive[i]:
            costume = ALIEN_TYPE[i//COLS]
            img = images[costume][img_idx]
            screen.blit(img, alien)

    draw_text(140, 5, f'SCORE: {score:04}', 55)
    draw_text(500, 5, f'SHIPS: {num_fighters:02}', 55)
    if not game_over and sum(is_alive) == 0:
        draw_text(150, 300, 'CLEARED !', 120)
    if num_fighters == 0 or game_over:
        draw_text(150, 300, 'GAME OVER', 120)

    pg.display.update()
    clock.tick(60)