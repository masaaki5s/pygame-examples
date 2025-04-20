"""
対戦型ピンポンゲームのベースとなるコードです
次の機能を追加してください
[1] ボールを打ち返すときに音をならす
[2] ボールが外に出たときに音をならす
[3] 相手（comp）のパドルがボールを打ち返せるように動く
[4] スコアをつける
[5] どちらかのスコアが11点になったらゲームオーバーにする
[6] サーブの方向をじゅんばんに変える
[7] コンピューターといい勝負ができるように調整する
[8] 打ち合いを続けるとボールが少しずつ速くなるようにする
[9] スマッシュ機能をつける（左矢印キーでボールを加速するとか）

"""
import sys
import pygame as pg

W, H = 800, 600

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
font_name = pg.font.match_font('consolas')
font = pg.font.Font(font_name, 60)
sound_hit = pg.mixer.Sound('sounds/pong.wav')
sound_miss = pg.mixer.Sound('sounds/fault.mp3')


def draw_screen(ball, comp, player, score, gameover):
    ''' ゲーム画面をひょうじする '''
    screen.fill('#1f3134')
    pg.draw.line(screen, 'white', (W//2, 0), (W//2, H))
    pg.draw.rect(screen, 'yellow', player)
    pg.draw.rect(screen, 'skyblue', comp)
    if gameover:
        text = font.render('GAME OVER', True, 'white')
        screen.blit(text, (250, 270))
        text = font.render('SPACE to Restart', True, 'white')
        screen.blit(text, (150, 330))
    else:
        pg.draw.ellipse(screen, 'orange', ball)
    score_ = font.render(f'{score[0]:02d}  {score[1]:02d}', True, 'white')
    screen.blit(score_, (W//2 - 110, 30))
    pg.display.update()

def new_ball():
    ''' あたらしいボールをつくる '''
    ball = pg.Rect(W//2-15, H//2-15, 20, 20)
    return ball, 6, 6                      # 6, 6 はボールのx, y方向のはやさ


player = pg.Rect(W-40, H//2-60, 10, 120)   # プレーヤーのパドル
comp = pg.Rect(30, H//2-60, 10, 120)       # 相手(コンピューター)のパドル
paddle_move = 8                            # パドルがうごく速さ
score = [0, 0]                             # [相手のスコア, じぶんのスコア]
ball, vx, vy = new_ball()                  # ボールのばしょと速さを初期化

gameover = False
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        player.y -= paddle_move
    if keys[pg.K_DOWN]:
        player.y += paddle_move

    if gameover and keys[pg.K_SPACE]:
        gameover = False
        score = [0, 0]
        ball, vx, vy = new_ball()

    if not gameover:
        ball.x += vx                           # ボールを移動（xざひょう)
        ball.y += vy                           #  yざひょう

        if ball.top <= 0 or ball.bottom >= H:  # うえ/した のカベで跳ね返る
            vy *= -1

        if ball.right <= 0 or ball.left >= W:  # ボールが外に出たとき
            ball, vx, vy = new_ball()
            pg.time.wait(1500)

        # ボールがパドルにあたったので打ち返す
        if (vx < 0 and ball.colliderect(comp)) or (vx > 0  and ball.colliderect(player)):
            vx *= -1

    draw_screen(ball, comp, player, score, gameover)   # 画面をびょうがする

    clock.tick(60)