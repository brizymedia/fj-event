# -*- coding: utf-8 -*-
"""고객 네이버 블로그(funandjoy12)에서 받은 원본 사진을 assets/img/p/<코드>.webp 로 변환한다.
원본 폴더(RAW)는 세션 임시 폴더라 없을 수 있다 — 이미 변환된 결과가 레포에 들어 있으니 다시 돌릴 일은 드물다.
사용: python tools/import_photos.py <RAW 폴더>   (파일명 <글번호>_<순번>.jpg)
"""
import os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = sys.argv[1] if len(sys.argv) > 1 else r'.'
OUT = os.path.join(ROOT, 'assets', 'img', 'p')
# 코드 → 원본 파일
MAP = {
    'hero': '224455253318_2', 'arch': '224424936543_3', 'sports': '224455253318_5', 'sports2': '224424936543_5',
    'sports3': '224304013568_1', 'sports4': '224309610512_1', 'rec': '224300197514_5',
    'bounce': '223810366865_4', 'bounce2': '223810366865_3', 'bounce3': '224321109260_3',
    'water': '224331630537_3', 'water2': '224342579872_1', 'water3': '224397194733_1', 'pool': '222785928595_2', 'indoor': '224367502395_2',
    'kids1': '222867508444_1', 'kids2': '222904661178_1', 'kids3': '224338184958_2', 'kids4': '223091498611_1',
}
os.makedirs(OUT, exist_ok=True)
for code, src in MAP.items():
    im = Image.open(os.path.join(RAW, src + '.jpg')).convert('RGB')
    im.thumbnail((1400, 1400))
    im.save(os.path.join(OUT, code + '.webp'), 'WEBP', quality=80, method=6)
    print(code, im.size)
