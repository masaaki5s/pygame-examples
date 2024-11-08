"""
シンプルなFlappy Bird
"""
import sys
import random
import pygame as pg

W, H = 600, 800
pg.init()
screen = pg.display.set_mode((W, H)) 
clock = pg.time.Clock()

pg.mixer.init()
flap_sound = pg.mixer.Sound("sounds/wing.wav")
hit_sound = pg.mixer.Sound("sounds/hit.wav")
score_sound = pg.mixer.Sound("sounds/point.wav")

def draw_text(x, y, txt, size=80, color='white'):
    font = pg.font.SysFont(None, size)
    img = font.render(txt, True, color)
    screen.blit(img, (x, y))

img = pg.image.load('images/background.png')
background = pg.transform.scale(img, (W, H))
bg_x = 0

bird_img = []
for name in ['bird_wing_up.png', 'bird_wing_down.png']:
    img = pg.image.load('images/'+name).convert_alpha() 
    img = pg.transform.scale2x(img)
    bird_img.append(img)
bird = bird_img[0].get_rect(center=(100, H//2))
bird_img_idx = 0
bird_vy, gravity = 0, 0.2

img = pg.image.load('images/pipe-green.png').convert_alpha()
pipe_img = pg.transform.scale(img, (80, 500))
pipe_img_flip = pg.transform.flip(pipe_img, False, True)
pipes = []

BIRD_FLAP = pg.USEREVENT
pg.time.set_timer(BIRD_FLAP, 100)
NEW_PIPE = pg.USEREVENT + 1
pg.time.set_timer(NEW_PIPE, 1800)

gameover = False
score , score_timer, high_score = 0, 0, 0
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if e.type == BIRD_FLAP:
            bird_img_idx = (bird_img_idx + 1) % len(bird_img)

        if e.type == NEW_PIPE:
            h = random.choice((350, 500, 650))
            pipes.append(pipe_img.get_rect(midtop = (W, h)))
            pipes.append(pipe_img.get_rect(midbottom = (W, h - 300)))
        
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE and not gameover:
                bird_vy = -5
                flap_sound.play()
            if e.key == pg.K_SPACE and gameover:
                bird_vy = 0
                bird.bottom = H//2
                pipes = []
                score, score_timer = 0, 0
                gameover = False           

    screen.blit(background, (bg_x, 0))
    screen.blit(background, (bg_x - W, 0))
    bg_x = (bg_x - 1) % W
    
    if not gameover:
        bird_vy += gravity
        bird.bottom = min(H, bird.bottom + bird_vy)

        for pipe in pipes:
            pipe.move_ip(-3, 0)
            if bird.colliderect(pipe):
                gameover = True 
                hit_sound.play()
                pg.time.wait(1000)
                pg.event.clear()
            if H <= pipe.bottom:
                screen.blit(pipe_img, pipe)
            else:
                screen.blit(pipe_img_flip, pipe)
        score_timer += 1
        if score_timer > 250:
            score += 1
            score_timer = 0
            score_sound.play()
        high_score = max(high_score, score)

        screen.blit(bird_img[bird_img_idx], bird)
        draw_text(220, 80, f'Score: {int(score)}', 50)
    else:
        draw_text(100, 300, 'Press SPACE to Restart', 50)
        draw_text(160, 600, f'High Score: {int(high_score)}', 50)

    pg.display.flip()
    clock.tick(60)