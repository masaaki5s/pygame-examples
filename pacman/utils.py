import pygame as pg

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))

def get_sprite(sprite_key, sizex, sizey):
    sheet = pg.image.load("assets/sprites.png").convert_alpha()
    Z = {'maze':(0, 0, 228, 248, 1, 1),
        'pacman':(229, 0, 16, 16, 3, 4),
        'red':(229, 64, 16, 16, 8, 1),
        'pink':(229, 80, 16, 16, 8, 1),
        'blue':(229, 96, 16, 16, 8, 1),
        'orange':(229, 112, 16, 16, 8, 1),
        }
    
    DIR = ((1,0), (-1,0), (0,-1), (0,1))
    x0, y0, w, h, cols, rows = Z[sprite_key]
    if sprite_key == 'maze':
        s = pg.Surface((w, h), pg.SRCALPHA)
        s.blit(sheet, (0, 0), pg.Rect(x0+c*w, y0+r*h, w, h)) 
        s = pg.transform.scale(s, (sizex, sizey))
        return s
    
    if sprite_key == 'pacman':
        ret = {}
        for r in range(rows):
            rr = []
            for c in range(cols):
                s = pg.Surface((w, h), pg.SRCALPHA)
                s.blit(sheet, (0, 0), pg.Rect(x0+c*w, y0+r*h, w, h))
                s = pg.transform.scale(s, (sizex, sizey))
                rr.append(s)
            ret[DIR[r]] = rr
        return ret
    
    else:   # 今回のバージョンではelseはゴースト（今後拡張）
        ret = {}
        for c in range(cols):
            if c%2 == 0:
                rr = []
            s = pg.Surface((w, h), pg.SRCALPHA)
            s.blit(sheet, (0, 0), pg.Rect(x0+c*w, y0, w, h))
            s = pg.transform.scale(s, (sizex, sizey))
            rr.append(s)
            if c%2==1:
                ret[DIR[c//2]] = rr 
        return ret           

