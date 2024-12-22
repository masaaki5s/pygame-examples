"""
PyGameを使った三目並べのGUI
"""
import sys
import pygame as pg
from tictactoe import X, O, EMPTY, TIE, initial_board, computer_move, check_winner
from time import sleep

SIZE = 150                 # マスのサイズ
X0 = Y0 = SIZE // 2        # 画面のマージン
W = H = SIZE * 4           # 画面サイズ

pg.init()
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()

def draw_text(text, x , y, font_color='white', bg_color=None, size=40):
    font = pg.font.SysFont(None, size)
    img = font.render(text, True, font_color)
    rect = img.get_rect()
    rect.center = (x, y)
    if bg_color is not None:
        pg.draw.rect(screen, bg_color, rect)
    screen.blit(img, rect)
    return rect

def draw_symbol(pos, symbol):
    x, y = pos
    if symbol == X:
        pg.draw.line(screen, 'blue', (x - 40, y - 40), (x + 40, y + 40), 10)
        pg.draw.line(screen, 'blue', (x - 40, y + 40), (x + 40, y - 40), 10)
    else:
        pg.draw.circle(screen, 'red', (x, y), 44, 10)

def select_symbol(x, y):
    draw_text("Select O or X",  W//2, 50)
    maru = pg.Rect(SIZE*0.5, SIZE*1.5, SIZE, SIZE)
    batu = pg.Rect(SIZE*2.5, SIZE*1.5, SIZE, SIZE)
    pg.draw.rect(screen, 'white', maru)
    pg.draw.rect(screen, 'white', batu)
    draw_symbol(maru.center, O)
    draw_symbol(batu.center, X)
    if x is not None:
        for symbol, rect in {O:maru, X:batu}.items():
            if rect.collidepoint(x, y):
                return symbol

def draw_board(board):
    for i in range(1, 3):
        pg.draw.line(screen, 'silver', (X0, Y0 + i * SIZE), (X0 + SIZE*3, Y0 + i * SIZE), 5)
        pg.draw.line(screen, 'silver', (X0 + i * SIZE, Y0), (X0 + i * SIZE, Y0 + SIZE *3), 5)
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                draw_symbol((X0 + j * SIZE + SIZE // 2, Y0 + i * SIZE + SIZE // 2), board[i][j])

def draw_result(board, x, y):
    draw_board(board)
    if winner == TIE:
        draw_text("Draw !",  W//2, 30)
    elif winner == human:
        draw_text("You won !",  W//2, 30)
    else:
        draw_text("Computer won !",  W//2, 30)
    rect = draw_text('Play again', W // 2, H - 30, font_color='black', bg_color='white')
    if x is not None and rect.collidepoint(x, y):
        return True

def human_move(board, x, y):
    if x is not None:
        row, col = (y - Y0) // SIZE, (x - X0) // SIZE 
        if board[row][col] == EMPTY:
            return (row, col)

board = initial_board()
human = None
game_over = False
while True:
    x, y = None, None
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos

    screen.fill('darkgreen')
    if human is None:
        human = select_symbol(x, y)
        player = O               # Oを先攻にする
    elif not game_over:
        if player == human:
            move = human_move(board, x, y)
        else:
            move = computer_move(board, player)
            sleep(0.3)          # 考えているフリをする
        if move is not None:
            board[move[0]][move[1]] = player
            player = -player
        winner = check_winner(board)
        if winner != 0:
            game_over = True
        draw_board(board)
    else:
        if draw_result(board, x, y):
            board = initial_board()
            human = None
            game_over = False
    
    pg.display.flip()
    clock.tick(30)