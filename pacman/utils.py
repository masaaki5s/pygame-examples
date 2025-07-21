import pygame as pg

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))


def get_image(x0, y0, w, h, c, r, sizex, sizey):
    sheet = pg.image.load("assets/sprites.png").convert_alpha()
    s = pg.Surface((w, h), pg.SRCALPHA)
    s.blit(sheet, (0, 0), pg.Rect(x0+c*w, y0+r*h, w, h))
    s = pg.transform.scale(s, (sizex, sizey))
    return s    


def get_sprite(sprite_key, sizex, sizey):
    """ スプライトシート上の座標，サイズ，縦横の個数 """
    Z = {'maze':(0, 0, 228, 248, 1, 1),
        'pacman':(228, 0, 16, 16, 3, 4),
        'red':(228, 64, 16, 16, 8, 1),
        'pink':(228, 80, 16, 16, 8, 1),
        'blue':(228, 96, 16, 16, 8, 1),
        'orange':(228, 112, 16, 16, 8, 1),
        'food_s':(228, 242, 4, 4, 1, 1),
        'food_l':(233, 240, 8, 8, 1, 1)
        }
    
    DIR = ((1,0), (-1,0), (0,-1), (0,1))
    x0, y0, w, h, cols, rows = Z[sprite_key]
    if sprite_key in ('maze', 'food_s', 'food_l'):
        s = get_image(x0, y0, w, h, 0, 0, sizex, sizey)
        return s
    
    if sprite_key == 'pacman':
        ret = {}
        for r in range(rows):
            rr = []
            for c in range(cols):
                s = get_image(x0, y0, w, h, c, r, sizex, sizey)
                rr.append(s)
            ret[DIR[r]] = rr
        return ret
    
    else:   # 今回のバージョンではelseはゴースト（今後拡張）
        ret = {}
        for c in range(cols):
            if c%2 == 0:
                rr = []
            s = get_image(x0, y0, w, h, c, 0, sizex, sizey)    
            rr.append(s)
            if c%2==1:
                ret[DIR[c//2]] = rr 
        return ret           

