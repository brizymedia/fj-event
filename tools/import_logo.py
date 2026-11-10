# -*- coding: utf-8 -*-
"""대표가 보낸 로고 2종(워드마크 Fun&joy · 마크 F&j)을 여백 자르고 흰 배경을 투명하게 해서 assets/img 에 넣는다.
사용: python tools/import_logo.py <워드마크 파일> <마크 파일>"""
import os, sys
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')


def trim(im, pad=12):
    im = im.convert('RGBA')
    comp = Image.alpha_composite(Image.new('RGBA', im.size, (255, 255, 255, 255)), im).convert('RGB')
    diff = ImageChops.difference(comp, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 14 else 0)
    x0, y0, x1, y1 = diff.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def alpha_white(im):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            if m > 235:
                px[x, y] = (r, g, b, 0)
            elif m > 200:
                px[x, y] = (r, g, b, int(255 * (235 - m) / 35))
    return im


word, mark = alpha_white(trim(Image.open(sys.argv[1]))), alpha_white(trim(Image.open(sys.argv[2])))
w = word.copy(); w.thumbnail((900, 900)); w.save(os.path.join(OUT, 'logo-fj.png'), optimize=True); print('logo-fj', w.size)
m = mark.copy(); m.thumbnail((512, 512)); m.save(os.path.join(OUT, 'logo-mark-fj.png'), optimize=True); print('mark', m.size)
# 파비콘: 정사각 캔버스에 마크
s = 64; f = mark.copy(); f.thumbnail((s - 4, s - 4)); c = Image.new('RGBA', (s, s), (0, 0, 0, 0)); c.paste(f, ((s - f.width) // 2, (s - f.height) // 2)); c.save(os.path.join(OUT, 'favicon.png'))
# 견적 메일 머리용 마크(흰 바탕 정사각)
k = Image.new('RGBA', (160, 160), (255, 255, 255, 255)); f = mark.copy(); f.thumbnail((140, 140)); k.paste(f, ((160 - f.width) // 2, (160 - f.height) // 2), f); k.convert('RGB').save(os.path.join(OUT, 'logo-mark.png'))
