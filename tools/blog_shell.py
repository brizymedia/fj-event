# -*- coding: utf-8 -*-
"""
블로그 페이지의 머리(header) · 꼬리(footer)를 tools/build_site.py 에서 그대로 가져와 _blog/shell.json 으로 저장한다.
build_site.py 는 읽기만 한다(고치지 않는다). 메뉴 · 연락처가 바뀌면 build_site.py 를 돌린 뒤 이것도 다시 돌린다.

  PYTHONUTF8=1 python tools/blog_shell.py
  node scripts/build-blog.mjs

순서: build_site.py → blog_shell.py → build-blog.mjs  (build_site.py 가 sitemap.xml · llms.txt 를 덮어쓰기 때문)
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_site as b  # noqa: E402  (불러오기만 하면 아무 파일도 만들지 않는다)

out = {
    'name': b.NAME, 'nameFull': b.NAME_FULL, 'ceo': b.CEO, 'tel': b.TEL, 'telRaw': b.TEL_RAW, 'email': b.EMAIL,
    'addr': b.ADDR, 'base': b.BASE, 'noindex': bool(b.NOINDEX), 'ver': b.VER, 'og': b.OG,
    'header': b.header(''), 'footer': b.footer(),
}
os.makedirs(os.path.join(ROOT, '_blog'), exist_ok=True)
with open(os.path.join(ROOT, '_blog', 'shell.json'), 'w', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('wrote _blog/shell.json  base=%s noindex=%s' % (b.BASE, b.NOINDEX))
