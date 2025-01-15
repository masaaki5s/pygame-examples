""" Mine Sweeper """
import sys
import pygame as pg
from random import randint

W, H, PXL = 9, 9, 45        # マスの数WxH, マスの大きさPXL
NUM_MINES = 10              # 地雷の数（ゲームをクリアするごとに+1
HEADER = int(PXL * 1.5)     # タイトル部分の高さ
UNK, MINE = -1, -2          # UNK:未知, MINE:地雷
RESET = (-1, -1)            # リセットボタンが押された
AROUND = [(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,1),(-1,0),(-1,-1)]
COLOR_MAP = ['blue', 'green', 'red', 'red', 'red', 'red', 'red', 'red']

def initialize_game():
    global NUM_MINES
    if game_status == 'gj':
        NUM_MINES += 1
    mine_pos = set()
    while len(mine_pos) < NUM_MINES:
        mine_pos.add((randint(0, W-1), randint(0, H-1)))
    field_map = [[UNK] * W for _ in range(H)]
    return 'smile', field_map, mine_pos


def get_mouse_click():
    click = pg.mouse.get_pressed()
    if click[0]:
        (x, y) = pg.mouse.get_pos()
        if reset_button.collidepoint((x, y)):
            return RESET
        w, h = x // PXL, (y - HEADER) // PXL
        if game_status == 'smile':
            if field_map[h][w] == UNK:
                return (w, h)


def draw_text(x, y, txt, fontsize=40, color='white', margine=8):
    font = pg.font.SysFont(None, fontsize)
    img = font.render(txt, True, color)
    screen.blit(img, (x + margine, y + margine))


def draw_screen(field_map):
    pg.draw.rect(screen, 'snow', header_rect, 6)
    screen.blit(images[game_status], reset_button)
    draw_text(W * PXL * 0.2, PXL * 0.2, f'{NUM_MINES:03d}', 55, 'darkred')
    to_clear = H * W if cleared_cells == 0 else H * W - NUM_MINES - cleared_cells
    draw_text(W * PXL * 0.7, PXL * 0.2, f'{to_clear:03d}', 55, 'darkred')

    for h in range(H):
        for w in range(W):
            rect = pg.Rect(w * PXL, HEADER + h * PXL, PXL-2, PXL-2)
            pg.draw.rect(screen, 'gray', rect)
            s = field_map[h][w]
            if s == UNK:
                screen.blit(images['square'], rect)
            if s == MINE:
                screen.blit(images['mine'], rect)
            if s >= 1:
                draw_text(w * PXL, HEADER + h * PXL, str(s), 45, COLOR_MAP[s-1])


def count_neighbor_mines(pos):
    cnt = 0
    for dw, dh in AROUND:
        if (pos[0] + dw, pos[1] + dh) in mine_pos:
            cnt += 1
    return cnt


def sweep_mines(pos):
    global cleared_cells
    count = count_neighbor_mines(pos)
    field_map[pos[1]][pos[0]] = count
    cleared_cells += 1
    if count != 0:
        return
    for dw, dh in AROUND:
        ww, hh = pos[0] + dw, pos[1] + dh
        if 0 <= ww < W and 0 <= hh < H and field_map[hh][ww] == UNK:
            sweep_mines((ww, hh))


pg.init()
screen = pg.display.set_mode((W * PXL, HEADER + H * PXL))
clock = pg.time.Clock()
pg.mixer.init()
sound_doomed = pg.mixer.Sound("sounds/boom.wav")

files = {'mine':'bomb', 'square':'square', 'smile':'smile', 'doomed':'doomed', 'gj':'gj'}
images = {}
for key, name in files.items():
    img = pg.image.load(f'images/{name}.png').convert_alpha()
    img = pg.transform.scale(img, (PXL, PXL))
    images[key] = img

header_rect = pg.Rect(0, 0, W * PXL, HEADER)
reset_button = images['smile'].get_rect(center=header_rect.center)

game_status = None
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pos = get_mouse_click()
    if game_status is None or pos == RESET:
        game_status, field_map, mine_pos = initialize_game()
        cleared_cells = 0
    elif pos is not None:
        if pos in mine_pos:
            for col, row in mine_pos:
                field_map[row][col] = MINE
            game_status = 'doomed'
            sound_doomed.play()
        else:
            sweep_mines(pos)

    if cleared_cells >= H * W - NUM_MINES:
        game_status = 'gj'

    screen.fill('darkgrey')
    draw_screen(field_map)
    pg.display.flip()
    clock.tick(10)