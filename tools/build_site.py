# -*- coding: utf-8 -*-
"""
F&J 이벤트(펀앤조이체육교실) 홈페이지 생성기.

  python tools/build_site.py

index · about · event · kids · portfolio · notice · contact · 404 와 sitemap.xml · robots.txt · llms.txt 를 만든다.
글 · 사진 목록은 이 파일 맨 위(회사 정보 · 자료)를 고치고 다시 돌린다. 결과 HTML 을 손으로 고치지 말 것.
사진은 assets/img/p/ 에 넣고 PHOTOS 에 적으면 자리표(그림)가 사진으로 바뀐다. 없으면 자리표가 나온다.
공지는 assets/data/notices.json 만 고치면 된다.
"""
import os, json, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img')

# ════════════════════════ 회사 정보 (제작 자료 제출서 2026-11-05 기준) ════════════════════════
NAME = 'F&J 이벤트'
NAME_FULL = 'F&J 이벤트 · 펀앤조이 체육교실'
CEO = '최원창'
BIZNO = '508-34-00436'
ADDR = '경기도 화성시 효행구 비봉면 일묵동안길 3-6'
TEL = '010-9121-9982'
TEL_RAW = TEL.replace('-', '')
EMAIL = 'cwc9982@naver.com'
HOURS = ['평일 10:00 ~ 19:00', '토요일 10:00 ~ 19:00', '일요일 휴무']
INSTA = 'https://www.instagram.com/fun_and_joy_'
NBLOG = 'https://blog.naver.com/funandjoy12'
YT = 'https://www.youtube.com/@FJEVENT'
KAKAO = ''            # 카카오톡 채널 주소를 받으면 여기에 (https://pf.kakao.com/_xxxx/chat). 비어 있으면 단추가 안 나온다
REPO = 'brizymedia/fj-event'   # 공지 관리자가 올린 공지(photos 가지)를 읽는 레포
BASE = 'https://brizymedia.github.io/fj-event'   # 도메인(F&J EVENT.co.kr 희망)을 잡으면 여기만 바꾸고 다시 실행
NOINDEX = True        # 오픈 확정 뒤 False
VER = "4"
EDIT_HASH = 'ca804a9435800bfb2ae99ecbc044bbcd4761f67b4aff81175e4f7bc1bc453830'   # 사장님 직접 수정 열쇠의 sha256 (열쇠 자체는 어디에도 적지 않는다 — 큰길브리지 Desktop 메모에만)
FORM_ENDPOINT = ''    # 문의 서버(Apps Script) 배포 뒤 /exec 주소. 비어 있으면 문자 앱으로 연결
MAP = 'https://map.naver.com/p/search/' + '%EA%B2%BD%EA%B8%B0%EB%8F%84%20%ED%99%94%EC%84%B1%EC%8B%9C%20%EB%B9%84%EB%B4%89%EB%A9%B4%20%EC%9D%BC%EB%AC%B5%EB%8F%99%EC%95%88%EA%B8%B8%203-6'
OG = BASE + '/assets/img/og.png'

NAV = [('about.html', '회사 소개'), ('event.html', '행사 · 대여'), ('kids.html', '유아체육 · 체험'), ('portfolio.html', '포트폴리오'), ('contact.html', '견적 문의')]

# ════════════════════════ 자료 ════════════════════════
# 하는 일 · 메뉴: 제출서의 「음향, 조명 100~」 등 (단위는 만 원으로 보고 적었다 — 대표 확인 필요)
MENU = [
    dict(k='sound', n='음향 · 조명', p='100', c='#2E9BFF', t='무대 음향과 조명을 설치하고 철수까지 맡습니다. 발표회 · 송년회 · 행사장 규모에 맞춰 구성합니다.'),
    dict(k='sports', n='체육대회 · 운동회', p='200', c='#FF6B5B', t='어린이집 · 유치원 · 초등학교 운동회와 기업 체육대회. 종목 기획부터 진행, 장비까지 한 번에.'),
    dict(k='bounce', n='놀이기구 · 에어바운스', p='44', c='#FFB400', t='에어바운스와 놀이기구를 세팅하고 철수합니다. 자체 장비라 제작과 수리까지 가능합니다.'),
    dict(k='water', n='워터슬라이드 · 수영장', p='44', c='#14B8A6', t='여름 물놀이 행사. 워터슬라이드와 수영장을 설치하고 안전하게 운영합니다.'),
    dict(k='rec', n='레크리에이션', p='80', c='#A06CF0', t='연령과 분위기에 맞춘 진행. 아이들부터 어른들 행사까지 분위기를 끌어올립니다.'),
    dict(k='party', n='송년회 · 신년회', p='80', c='#F0508C', t='회사 · 단체 모임을 위한 진행과 게임, 음향 구성.'),
]
KIDS = [
    ('유아체육', '연령에 맞춘 체육 수업. 스카프, 낙하산 같은 교구로 몸을 움직이며 배웁니다.'),
    ('체험놀이', '꼬마농부 체험놀이처럼 실내에서 즐기는 역할 놀이와 체험 프로그램.'),
    ('교구 대여', '놀이와 수업에 쓰는 교구를 빌려 드립니다.'),
    ('발표회', '어린이집 · 유치원 발표회의 의상, 무대, 진행을 함께합니다.'),
]
STRENGTHS = [
    ('15년 이상', '유아체육과 이벤트 행사를 15년 넘게 해 왔습니다.'),
    ('자체 장비', '장비를 직접 보유하고 대여하며, 제작까지 하고 있습니다.'),
    ('영상으로 확인', '유튜브와 인스타그램에서 실제 진행 모습을 미리 볼 수 있습니다.'),
]
RECORDS = [
    ('연 100회', '경기 남부 초등학교 · 어린이집 · 유치원 운동회'),
    ('연 50회', '경기 남부 지역 물놀이 행사'),
    ('여러 행사', '경기도교육청 주관 행사 진행'),
]
TICKER = ['유아체육', '어린이집 · 유치원 운동회', '초등학교 체육대회', '에어바운스', '워터슬라이드', '수영장 대여', '레크리에이션', '송년회 · 신년회', '발표회', '무대 음향 · 조명', '체험놀이', '교구 대여']
# 유튜브 영상(대표 채널 @FJEVENT) — 삽입 재생
VIDEOS = [
    ('S1a3lRav3-I', '즐거운 운동회는 어떻게 만들어질까? (운동회 세팅편)', '11:04'),
    ('_itNao4BpXo', '운동회가 재미있는 이유!', '7:39'),
    ('KUuAzG_oi_c', '입구아치 · 조형물 소개 (펀앤조이 체육교실)', '2:31'),
    ('4zSj4dSBc2E', '펀앤조이 미로바운스', 'Shorts'),
]
# 사진: 코드 → (제목, 파일명 assets/img/p/ 안). 파일이 있으면 사진, 없으면 자리표
PHOTOS = [
    ('hero', '안산 · 가을 운동회', '', 'sports'), ('arch', '향남 · 입구 아치 세팅', '', 'sports'), ('sports', '안산 · 운동회 게임', '', 'sports'),
    ('sports2', '향남 · 병설유치원 운동회', '', 'sports'), ('sports3', '수원 · 체육대회', '', 'sports'), ('sports4', '오산 · 초등학교 체육대회', '', 'sports'),
    ('rec', '군포 · 가족운동회', '', 'rec'),
    ('bounce', '어린이날 에어바운스', '', 'bounce'), ('bounce2', '어린이날 에어바운스', '', 'bounce'), ('bounce3', '시흥 · 뽀로로 슬라이드', '', 'bounce'),
    ('water', '화성 · 워터슬라이드', '', 'water'), ('water2', '안산 · 물놀이', '', 'water'), ('water3', '서울 · 해적 워터슬라이드', '', 'water'),
    ('pool', '인천 · 10x10 수영장 대여', '', 'water'), ('indoor', '동탄 · 실내 수영장', '', 'water'),
    ('kids1', '스카프 유아체육', '', 'sports'), ('kids2', '꼬마농부 체험놀이', '', 'sports'), ('kids3', '교통안전 체험놀이', '', 'sports'), ('kids4', '철봉 유아체육', '', 'sports'),
]
GROUPS = [
    ('운동회 · 체육대회', ['hero', 'arch', 'sports', 'sports2', 'sports3', 'sports4', 'rec']),
    ('에어바운스', ['bounce', 'bounce2', 'bounce3']),
    ('물놀이 · 수영장', ['water', 'water2', 'water3', 'pool', 'indoor']),
    ('유아체육 · 체험놀이', ['kids1', 'kids2', 'kids3', 'kids4']),
]
CAP = {c: t for c, t, _, _ in PHOTOS}
FAQ = [
    ('견적은 어떻게 받나요?', '행사 날짜, 장소, 예상 인원만 알려 주세요. 전화, 문자, 카카오톡, 아래 문의 양식 중 편한 방법이면 됩니다. 확인 뒤 구성과 비용을 정리해 드립니다.'),
    ('어느 지역까지 가나요?', '경기 남부를 중심으로 진행하고 있습니다. 화성 · 동탄 · 안산 · 인천 등에서 진행한 기록이 있고, 지역이 멀어도 문의는 받습니다.'),
    ('장비만 빌릴 수 있나요?', '네. 음향 · 조명, 에어바운스, 워터슬라이드, 수영장은 설치와 철수까지 하는 대여가 가능합니다. 진행 인력이 필요하면 함께 구성합니다.'),
    ('우천이나 날씨 걱정이 있는 행사는요?', '실내 대체 장소와 프로그램을 미리 정해 두고 준비합니다. 야외 행사는 상담 때 먼저 말씀해 주세요.'),
    ('운동회 종목도 정해 주시나요?', '아이들 나이와 인원, 운동장 크기에 맞춰 종목을 제안합니다. 원하시는 게임이 있으면 반영합니다.'),
]
NOTICES = json.load(open(os.path.join(ROOT, 'assets/data/notices.json'), encoding='utf-8'))
NJ = html.escape(json.dumps(NOTICES, ensure_ascii=False), quote=True).replace("'", '&#39;')

# ════════════════════════ 조각 ════════════════════════
esc = lambda s: html.escape(str(s), quote=True)
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
# 자리표 그림(사진 대신) — 종류별
ART = {
    'sports': '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M20 98V44a40 40 0 0 1 80 0v54" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round"/><circle cx="20" cy="104" r="6" fill="currentColor"/><circle cx="100" cy="104" r="6" fill="currentColor"/><path d="M34 98V48a26 26 0 0 1 52 0v50" fill="none" stroke="currentColor" stroke-width="5" opacity=".5"/></svg>',
    'bounce': '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M14 100V58l14-10 14 10 18-14 18 14 14-10 14 10v42z" fill="currentColor" opacity=".85"/><rect x="48" y="72" width="24" height="28" rx="12" fill="#fff" opacity=".8"/></svg>',
    'water': '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M16 30c22 0 22 26 44 26s22 26 44 26" fill="none" stroke="currentColor" stroke-width="12" stroke-linecap="round"/><path d="M10 100c10-8 20-8 30 0s20 8 30 0 20-8 30 0" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" opacity=".55"/></svg>',
    'rec': '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M30 26l50 58-14 4zM80 84l20 16" fill="none"/><rect x="48" y="14" width="24" height="46" rx="12" fill="currentColor"/><path d="M34 52a26 26 0 0 0 52 0M60 78v22M44 100h32" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg>',
    'sound': '<svg viewBox="0 0 120 120" aria-hidden="true"><rect x="22" y="12" width="76" height="96" rx="14" fill="currentColor" opacity=".9"/><circle cx="60" cy="40" r="12" fill="#fff" opacity=".85"/><circle cx="60" cy="80" r="20" fill="#fff" opacity=".85"/><circle cx="60" cy="80" r="9" fill="currentColor"/></svg>',
    'party': '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M20 100l22-60 38 38z" fill="currentColor"/><path d="M62 24l4 12M92 38l-10 6M96 66l-12-2M72 14l-2 12" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>',
}


def photo(code, cls='', alt=None, w=None, h=None, eager=False):
    """사진이 있으면 <img>, 없으면 색 자리표."""
    rec = next((p for p in PHOTOS if p[0] == code), None)
    title, kind = (rec[1], rec[3]) if rec else (code, 'sports')
    for ext in ('webp', 'jpg', 'png'):
        if os.path.exists(os.path.join(IMG, 'p', f'{code}.{ext}')):
            ld = '' if eager else ' loading="lazy" decoding="async"'
            sz = f' width="{w}" height="{h}"' if w and h else ''
            return f'<img class="{cls}" src="assets/img/p/{code}.{ext}" alt="{esc(alt or title)}"{sz}{ld}>'
    return f'<div class="ph k-{kind} {cls}" role="img" aria-label="{esc(title)} 사진 자리">{ART.get(kind, ART["sports"])}<span>{esc(title)}</span></div>'


def btn(href, text, cls='', ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="btn {cls}" href="{href}"{t}>{text}<span class="ar">{ARROW}</span></a>'


def header(cur):
    items = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV)
    sheet = ''.join(f'<a class="m" href="{h}">{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">본문으로 바로가기</a>
<header class="hdr"><div class="pill">
  <a class="logo" href="index.html" aria-label="{NAME} 처음으로"><img src="assets/img/logo-fj.png" alt="Fun&amp;joy 펀앤조이 체육교실 F&amp;J 이벤트" width="81" height="44"></a>
  <nav aria-label="주 메뉴">{items}</nav>
  <a class="tel" href="tel:{TEL_RAW}">{PHONE}{TEL}</a>
  <button class="mbtn" aria-label="메뉴 열기" aria-expanded="false" aria-controls="sheet"><i></i><i></i><i></i></button>
</div></header>
<div class="sheet" id="sheet">{sheet}
  <div class="sub"><a href="notice.html">공지사항</a><a href="blog/index.html">블로그</a><a href="quote.html">자동 견적서</a><a href="{NBLOG}" target="_blank" rel="noopener">네이버 블로그</a><a href="{YT}" target="_blank" rel="noopener">유튜브</a><a href="{INSTA}" target="_blank" rel="noopener">인스타그램</a></div>
  <div class="btns" style="margin-top:28px">{btn("tel:" + TEL_RAW, "전화 " + TEL, "sun")}</div>
</div>'''


def footer():
    kk = f'<a href="{KAKAO}" target="_blank" rel="noopener">카카오톡 상담</a>' if KAKAO else f'<a href="sms:{TEL_RAW}">문자 상담</a>'
    return f'''<footer class="ft"><div class="wrap">
  <div class="grid">
    <div><span class="flw"><img class="fl" src="assets/img/logo-fj.png" alt="Fun&amp;joy 펀앤조이 체육교실" width="81" height="44"></span>
      <div class="info"><b style="color:#fff">{NAME_FULL}</b> · 대표 {CEO}<br>사업자등록번호 {BIZNO}<br>{ADDR}<br>전화 <a href="tel:{TEL_RAW}" style="display:inline">{TEL}</a> · <a href="mailto:{EMAIL}" style="display:inline">{EMAIL}</a><br>{' · '.join(HOURS)}</div></div>
    <div><h4>회사</h4><a href="about.html">회사 소개</a><a href="portfolio.html">포트폴리오</a><a href="notice.html">공지사항</a><a href="contact.html">오시는 길</a></div>
    <div><h4>서비스</h4><a href="event.html">행사 · 대여</a><a href="kids.html">유아체육 · 체험</a><a href="blog/index.html">행사 준비 블로그</a><a href="contact.html">견적 문의</a></div>
    <div><h4>채널</h4><a href="{NBLOG}" target="_blank" rel="noopener">네이버 블로그</a><a href="{YT}" target="_blank" rel="noopener">유튜브</a><a href="{INSTA}" target="_blank" rel="noopener">인스타그램</a></div>
  </div>
  <div class="copy"><span>© {datetime.date.today().year} {NAME}. All rights reserved.</span><span>고객의 웃음과 즐거움을 위해</span></div>
  <div class="admin-entry" style="text-align:center;padding:14px 0 0;font-size:12px"><a href="office.html" rel="nofollow" style="display:inline-flex;gap:5px;align-items:center;opacity:.5;padding:0"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>관리자 모드</a></div>
</div></footer>
<div class="dock"><a href="tel:{TEL_RAW}">전화 상담</a>{kk}</div>
<script src="assets/app.js?v={VER}"></script>
<script src="assets/edit.js?v={VER}" defer></script>
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="fj"></script>'''


def jsonld_biz():
    d = {
        '@context': 'https://schema.org', '@type': 'LocalBusiness', '@id': BASE + '/#business', 'name': NAME, 'alternateName': ['펀앤조이 체육교실', 'F&J EVENT'],
        'url': BASE + '/', 'image': OG, 'telephone': TEL, 'email': EMAIL,
        'description': '경기 화성의 유아체육 · 이벤트 행사 전문. 어린이집 · 유치원 · 초등학교 운동회, 에어바운스, 워터슬라이드, 수영장 대여, 음향 · 조명, 레크리에이션.',
        'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '경기도', 'addressLocality': '화성시', 'streetAddress': '비봉면 일묵동안길 3-6'},
        'founder': {'@type': 'Person', 'name': CEO},
        'areaServed': ['화성', '동탄', '안산', '인천', '경기 남부'], 'sameAs': [NBLOG, YT, INSTA],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'opens': '10:00', 'closes': '19:00'}],
        'knowsAbout': ['유아체육', '운동회', '체육대회', '에어바운스', '워터슬라이드', '수영장 대여', '레크리에이션', '무대 음향 조명', '발표회'],
    }
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def jsonld_faq():
    d = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def page(fn, title, desc, body, cur='', extra_head=''):
    url = BASE + '/' + ('' if fn == 'index.html' else fn)
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    EDIT_META = ('<meta name="fj-edit" content="' + EDIT_HASH + '">') if fn not in ('notice-admin.html', '404.html') else ''
    out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<meta name="theme-color" content="#FFFBF0">
{EDIT_META}
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{OG}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&family=Gothic+A1:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="assets/style.css?v={VER}">
{extra_head}
</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    open(os.path.join(ROOT, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn)


def phead(crumb, eb, h1, lead=''):
    return f'''<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">홈</a> › {crumb}</p>
  <span class="eb"><i></i>{eb}</span>
  <h1 class="rv">{h1}</h1>
  {f'<p class="lead rv d1">{lead}</p>' if lead else ''}
</div></section>'''


def cta_band(title='행사 날짜가 정해지셨나요?', sub='날짜 · 장소 · 인원만 알려 주세요. 바로 견적을 정리해 드립니다.'):
    kk = btn(KAKAO, '카카오톡 상담', 'sun', True) if KAKAO else btn('sms:' + TEL_RAW, '문자로 문의', 'sun')
    return f'''<section class="sec cta"><div class="wrap"><div class="box rv">
  <span class="eb"><i></i>CONTACT</span>
  <h2 style="margin-top:18px">{title}</h2>
  <p>{sub}</p>
  <a class="phone" href="tel:{TEL_RAW}">{TEL}</a>
  <div class="btns">{btn("contact.html", "견적 문의하기", "white")}{kk}</div>
</div></div></section>'''


def yt_card(v, i=0):
    vid, t, dur = v
    return (f'<figure class="vid rv d{i % 4 + 1}"><button class="vbtn" data-yt="{vid}" aria-label="{esc(t)} 재생">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" decoding="async">'
            f'<span class="play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span><span class="dur">{dur}</span></button>'
            f'<figcaption>{esc(t)}</figcaption></figure>')


# ════════════════════════ 대문 ════════════════════════
def build_index():
    tick = ''.join(f'<span>{esc(t)}</span>' for t in TICKER) * 2
    menu = ''.join(
        f'<a class="mn rv d{i % 4 + 1}" href="event.html#{m["k"]}" style="--c:{m["c"]}"><span class="ic">{ART[m["k"] if m["k"] in ART else "sports"]}</span><h3>{m["n"]}</h3><p class="from"><b>{m["p"]}</b>만 원~</p><span class="more">자세히 보기 →</span></a>'
        for i, m in enumerate(MENU))
    st = ''.join(f'<li class="rv d{i + 1}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(STRENGTHS))
    rec = ''.join(f'<div class="rc rv d{i + 1}"><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(RECORDS))
    vids = ''.join(yt_card(v, i) for i, v in enumerate(VIDEOS))
    gal = ''.join(f'<figure class="g rv d{i % 4 + 1}">{photo(code, "gi")}<figcaption>{esc(CAP[code])}</figcaption></figure>' for i, code in enumerate(['arch', 'bounce', 'water', 'sports', 'kids2', 'indoor']))
    notes = ''.join(
        f'<li><a href="notice.html#n{i}"><time>{esc(n["d"])}</time><span class="t">{esc(n["t"])}</span></a></li>' for i, n in enumerate(NOTICES[:4]))
    faq = ''.join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    body = f'''
<section class="hero" aria-label="{NAME} 소개">
  <div class="hbg" aria-hidden="true"><i class="b b1"></i><i class="b b2"></i><i class="b b3"></i><i class="b b4"></i><i class="b b5"></i></div>
  <div class="wrap hgrid">
    <div class="htxt">
      <span class="eb"><i></i>FUN &amp; JOY EVENT</span>
      <h1>고객의 <em>웃음</em>과<br><em class="e2">즐거움</em>을 위해</h1>
      <p class="sub">유아체육 · 운동회 · 에어바운스 · 워터슬라이드<br>경기 남부 15년, 펀앤조이가 현장을 만듭니다.</p>
      <div class="btns">{btn("contact.html", "견적 문의", "sun")}{btn("event.html", "행사 · 대여 보기", "white")}</div>
      <ul class="hnum"><li><b>15<small>년+</small></b><span>현장 경력</span></li><li><b>100<small>회</small></b><span>연 운동회</span></li><li><b>50<small>회</small></b><span>연 물놀이</span></li></ul>
    </div>
    <div class="hpic">{photo("hero", "hp", w=720, h=560, eager=True)}<span class="sticker s1">운동회</span><span class="sticker s2">에어바운스</span></div>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="tr">{tick}</div></div>

<section class="sec" id="menu"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>SERVICE</span><h2 class="h2 rv">이런 <span class="hl">행사</span>를 합니다</h2></div>
    <p class="lead rv" style="margin:0">시작 금액 기준입니다. 규모와 장소에 따라 달라지니 견적을 받아 보세요.</p></div>
  <div class="menu">{menu}</div>
</div></section>

<section class="sec sun" id="why"><div class="wrap two">
  <div><span class="eb"><i></i>WHY F&amp;J</span><h2 class="h2 rv">믿고 맡기실 수 있는 <span class="hl">이유</span></h2>
    <p class="lead rv">「믿고 맡겨주시면 실망시키지 않도록 최선을 다 하겠습니다.」 대표 최원창의 약속입니다.</p></div>
  <ul class="why">{st}</ul>
</div></section>

<section class="sec" id="rec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>TRACK RECORD</span><h2 class="h2 rv">해마다 이만큼 <span class="hl">현장</span>에 섭니다</h2></div></div>
  <div class="recs">{rec}</div>
</div></section>

<section class="sec cream" id="videos"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>VIDEO</span><h2 class="h2 rv">영상으로 먼저 <span class="hl">확인</span>하세요</h2></div>{btn(YT, "유튜브 채널 보기", "line sm", True)}</div>
  <div class="vids">{vids}</div>
</div></section>

<section class="sec" id="gallery"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>GALLERY</span><h2 class="h2 rv">현장 <span class="hl">갤러리</span></h2></div>{btn("portfolio.html", "포트폴리오 보기", "line sm")}</div>
  <div class="gal">{gal}</div>
  <p class="lead" style="margin-top:22px">더 많은 현장 이야기는 <a href="{NBLOG}" target="_blank" rel="noopener" style="color:var(--blue-ink);font-weight:800">네이버 블로그</a>와 <a href="{INSTA}" target="_blank" rel="noopener" style="color:var(--blue-ink);font-weight:800">인스타그램</a>에서 볼 수 있어요.</p>
</div></section>

<section class="sec cream" id="notice"><div class="wrap two">
  <div><span class="eb"><i></i>NOTICE</span><h2 class="h2 rv">공지사항</h2><p class="lead rv">행사 일정과 새 소식을 알려 드립니다.</p><div style="margin-top:26px">{btn("notice.html", "공지 전체 보기", "line sm")}</div></div>
  <ul class="notes rv d1">{notes}</ul>
</div></section>

<section class="sec" id="faq"><div class="wrap two">
  <div><span class="eb"><i></i>FAQ</span><h2 class="h2 rv">자주 묻는 <span class="hl">질문</span></h2></div>
  <div class="faq">{faq}</div>
</div></section>
{cta_band()}
'''
    page('index.html', f'{NAME} | 경기 화성 유아체육 · 운동회 · 에어바운스 · 워터슬라이드', '경기 화성 F&J 이벤트(펀앤조이 체육교실). 어린이집 · 유치원 · 초등학교 운동회, 에어바운스, 워터슬라이드, 수영장 대여, 음향 · 조명, 레크리에이션을 15년 넘게 진행합니다.',
         body, 'index.html', extra_head=jsonld_biz() + jsonld_faq())


# ════════════════════════ 회사 소개 ════════════════════════
def build_about():
    st = ''.join(f'<li class="rv d{i + 1}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(STRENGTHS))
    hours = ''.join(f'<li>{h}</li>' for h in HOURS)
    body = phead('회사 소개', 'ABOUT', '유아체육과 이벤트,<br><span class="hl">15년</span>을 한결같이',
                 '고객의 웃음과 즐거움을 위해 최선을 다하겠습니다.') + f'''
<section class="sec"><div class="wrap two">
  <div class="rv"><span class="eb"><i></i>INTRO</span><h2 class="h2">F&amp;J 이벤트<br>펀앤조이 체육교실</h2></div>
  <div class="prose rv d1">
    <p>유아체육과 이벤트 행사를 <strong>15년 이상</strong> 해 오고 있습니다.</p>
    <p>어린이집 · 유치원 · 초등학교 운동회와 체육대회를 진행하고, 놀이기구와 에어바운스, 물놀이, 워터슬라이드, 수영장을 세팅하고 철수해 드립니다. 송년회 · 신년회 같은 모임 행사와 함께 어린이집 · 유치원 발표회의 의상과 진행도 해 오고 있습니다.</p>
    <p>장비는 직접 보유하고 대여하며, 필요한 장비는 제작까지 합니다. 그래서 세팅부터 진행, 철수까지 한 곳에 맡기실 수 있습니다.</p>
    <blockquote>「믿고 맡겨주시면 실망시키지 않도록 최선을 다 하겠습니다.」<cite>대표 {CEO}</cite></blockquote>
  </div>
</div></section>

<section class="sec sun"><div class="wrap two">
  <div><span class="eb"><i></i>STRENGTH</span><h2 class="h2 rv">우리의 <span class="hl">강점</span></h2></div>
  <ul class="why">{st}</ul>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>TRACK RECORD</span><h2 class="h2 rv">진행 <span class="hl">실적</span></h2></div></div>
  <div class="recs">{''.join(f'<div class="rc rv d{i + 1}"><b>{a}</b><span>{b}</span></div>' for i, (a, b) in enumerate(RECORDS))}</div>
</div></section>

<section class="sec cream"><div class="wrap two">
  <div><span class="eb"><i></i>INFO</span><h2 class="h2 rv">회사 정보</h2></div>
  <dl class="info2 rv d1">
    <div><dt>상호</dt><dd>{NAME_FULL}</dd></div><div><dt>대표</dt><dd>{CEO}</dd></div>
    <div><dt>사업자등록번호</dt><dd>{BIZNO}</dd></div><div><dt>주소</dt><dd>{ADDR}</dd></div>
    <div><dt>전화</dt><dd><a href="tel:{TEL_RAW}">{TEL}</a></dd></div><div><dt>이메일</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    <div><dt>영업시간</dt><dd><ul class="hrs">{hours}</ul></dd></div>
  </dl>
</div></section>
{cta_band()}
'''
    page('about.html', f'회사 소개 | {NAME}', 'F&J 이벤트(펀앤조이 체육교실)는 유아체육과 이벤트 행사를 15년 이상 해 온 경기 화성의 행사 회사입니다. 자체 장비 대여와 제작까지 합니다.', body, 'about.html')


# ════════════════════════ 행사 · 대여 ════════════════════════
def build_event():
    cards = ''
    for i, m in enumerate(MENU):
        k = m['k']
        cards += f'''<article class="svc rv" id="{k}" style="--c:{m['c']}"><div class="sp">{photo({'sound': 'arch', 'sports': 'sports2', 'bounce': 'bounce', 'water': 'water', 'rec': 'rec', 'party': 'sports3'}[k], "gi")}</div>
  <div class="st"><span class="no">0{i + 1}</span><h3>{m['n']}</h3><p>{m['t']}</p><p class="from"><b>{m['p']}</b>만 원~ <small>(규모 · 장소에 따라 달라집니다)</small></p>{btn("contact.html?s=" + k + "#form", "이 항목 견적 문의", "ink sm")}</div></article>'''
    body = phead('행사 · 대여', 'EVENT', '행사와 장비,<br><span class="hl">한 곳</span>에 맡기세요',
                 '세팅부터 진행, 철수까지. 자체 장비로 운영하고 제작까지 합니다.') + f'''
<section class="sec"><div class="wrap"><div class="svcs">{cards}</div></div></section>
<section class="sec cream"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>HOW IT WORKS</span><h2 class="h2 rv">진행은 이렇게 됩니다</h2></div></div>
  <ol class="steps"><li class="rv d1"><b>1</b><h3>문의</h3><p>날짜 · 장소 · 인원을 알려 주세요.</p></li><li class="rv d2"><b>2</b><h3>상담 · 견적</h3><p>구성과 비용을 정리해 드립니다.</p></li><li class="rv d3"><b>3</b><h3>세팅</h3><p>행사 전 장비와 무대를 설치합니다.</p></li><li class="rv d4"><b>4</b><h3>진행 · 철수</h3><p>현장 진행 뒤 깔끔히 철수합니다.</p></li></ol>
</div></section>
{cta_band()}'''
    page('event.html', f'행사 · 대여 | {NAME}', '운동회 · 체육대회, 에어바운스, 워터슬라이드, 수영장 대여, 음향 · 조명, 레크리에이션, 송년회 · 신년회. 경기 화성 F&J 이벤트.', body, 'event.html')


# ════════════════════════ 유아체육 · 체험 ════════════════════════
def build_kids():
    cards = ''.join(f'<div class="kd rv d{i % 4 + 1}"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(KIDS))
    body = phead('유아체육 · 체험', 'KIDS', '아이들이 <span class="hl">뛰어노는</span><br>펀앤조이 체육교실',
                 '유아체육, 체험놀이, 교구 대여, 발표회까지 어린이집 · 유치원 · 놀이학교와 함께합니다.') + f'''
<section class="sec"><div class="wrap"><div class="kds">{cards}</div>
  <div class="gal" style="margin-top:34px">{''.join(f'<figure class="g rv d{i + 1}">{photo(c, "gi")}<figcaption>{esc(CAP[c])}</figcaption></figure>' for i, c in enumerate(['kids1', 'kids2', 'kids3']))}</div></div></section>
<section class="sec cream"><div class="wrap two">
  <div><span class="eb"><i></i>SEASON</span><h2 class="h2 rv">계절 따라 <span class="hl">이런 행사</span></h2></div>
  <ul class="why"><li class="rv d1"><b>봄 · 가을</b><span>어린이집 · 유치원 · 초등학교 운동회, 체육대회.</span></li><li class="rv d2"><b>여름</b><span>워터슬라이드와 수영장 대여로 물놀이 행사.</span></li><li class="rv d3"><b>겨울</b><span>발표회, 송년회 · 신년회, 시무식 · 종무식.</span></li></ul>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>VIDEO</span><h2 class="h2 rv">수업 · 행사 <span class="hl">영상</span></h2></div>{btn(YT, "유튜브 채널", "line sm", True)}</div>
  <div class="vids">{''.join(yt_card(v, i) for i, v in enumerate(VIDEOS[:4]))}</div>
</div></section>
{cta_band('수업 · 행사 문의', '원 · 학교 이름과 원하는 시기를 알려 주세요.')}'''
    page('kids.html', f'유아체육 · 체험놀이 | {NAME}', '어린이집 · 유치원 · 놀이학교 유아체육, 체험놀이, 교구 대여, 발표회. 경기 화성 펀앤조이 체육교실.', body, 'kids.html')


# ════════════════════════ 포트폴리오 ════════════════════════
def build_portfolio():
    gal = ''.join(f'<h3 class="gh">{g}</h3><div class="gal">' + ''.join(f'<figure class="g rv d{i % 4 + 1}">{photo(code, "gi")}<figcaption>{esc(CAP[code])}</figcaption></figure>' for i, code in enumerate(cs)) + '</div>' for g, cs in GROUPS)
    body = phead('포트폴리오', 'PORTFOLIO', '현장에서 <span class="hl">보여드립니다</span>',
                 '영상 · 사진 · 블로그 후기까지, 실제 진행 모습을 볼 수 있습니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>VIDEO</span><h2 class="h2 rv">영상</h2></div>{btn(YT, "유튜브 채널", "line sm", True)}</div>
  <div class="vids">{''.join(yt_card(v, i) for i, v in enumerate(VIDEOS))}</div>
</div></section>
<section class="sec cream"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>PHOTO</span><h2 class="h2 rv">사진</h2></div></div>
  {gal}
</div></section>
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>CHANNELS</span><h2 class="h2 rv">더 많은 <span class="hl">현장 이야기</span></h2></div></div>
  <div class="chs">
    <a class="ch rv d1" href="{NBLOG}" target="_blank" rel="noopener" style="--c:#03C75A"><b>네이버 블로그</b><span>운동회 · 물놀이 · 체험놀이 현장 후기</span><i>바로가기 →</i></a>
    <a class="ch rv d2" href="{YT}" target="_blank" rel="noopener" style="--c:#FF3B30"><b>유튜브</b><span>운동회 세팅부터 입구 아치까지</span><i>바로가기 →</i></a>
    <a class="ch rv d3" href="{INSTA}" target="_blank" rel="noopener" style="--c:#E1306C"><b>인스타그램</b><span>fun_and_joy_ 일상 · 행사 사진</span><i>바로가기 →</i></a>
  </div>
</div></section>
{cta_band()}'''
    page('portfolio.html', f'포트폴리오 | {NAME}', 'F&J 이벤트 운동회 · 물놀이 · 체험놀이 현장 영상과 사진, 블로그 후기.', body, 'portfolio.html')


# ════════════════════════ 공지 ════════════════════════
def build_notice():
    items = ''.join(
        f'<article class="nt rv" id="n{i}"><time>{esc(n["d"])}</time><h3>{esc(n["t"])}</h3><p>{esc(n["b"])}</p></article>' for i, n in enumerate(NOTICES))
    # 공지 관리자(notice-admin.html)로 올린 공지는 photos 가지의 notices.json 에 쌓인다 — 있으면 이 목록 앞에 붙인다(없거나 못 읽으면 아래 정적 목록 그대로)
    live = f'''<script>
(function(){{
  var box=document.getElementById('nlist'); if(!box||location.protocol.indexOf('http')!==0) return;
  function esc(t){{return String(t==null?'':t).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  fetch('https://raw.githubusercontent.com/{REPO}/photos/photos/notices.json?t='+Math.floor(Date.now()/120000),{{cache:'no-store'}}).then(function(r){{return r.ok?r.json():null;}}).then(function(j){{
    if(!j||!j.notices||!j.notices.length) return;
    var st=[]; try{{st=JSON.parse(box.getAttribute('data-static')||'[]');}}catch(x){{}}
    box.innerHTML=j.notices.concat(st).map(function(n,i){{return '<article class="nt in" id="n'+i+'"><time>'+esc(n.d)+'</time><h3>'+esc(n.t)+'</h3><p>'+esc(n.b||'')+'</p></article>';}}).join('');
  }}).catch(function(){{}});
}})();
</script>'''
    body = phead('공지사항', 'NOTICE', '공지사항', '행사 일정과 새 소식을 알려 드립니다.') + f'<section class="sec"><div class="wrap narrow" id="nlist" data-static=\'{NJ}\'>{items}</div></section>' + live + cta_band()
    page('notice.html', f'공지사항 | {NAME}', 'F&J 이벤트 공지사항.', body, 'notice.html')


# ════════════════════════ 공지 관리자 (서버 연결 뒤 작동) ════════════════════════
def build_notice_admin():
    import re
    pd = open(os.path.join(ROOT, 'tools/port_docs.py'), encoding='utf-8').read()
    m = re.search(r"^GALLERY_URL\s*=\s*'([^']*)'", pd, re.M)
    gurl = m.group(1) if m else ''
    body = f"""<section class="phead" style="padding-bottom:30px"><div class="wrap"><span class="eb"><i></i>ADMIN</span><h1 style="font-size:clamp(30px,5vw,52px)">공지사항 관리</h1>
<p class="lead">공지를 쓰면 홈페이지 공지사항에 올라갑니다(몇 분 안에). 사진 올리기와 같은 비밀번호를 씁니다.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap" style="max-width:900px">
<style>.nadm .nrow{{display:flex;gap:14px;flex-wrap:wrap;align-items:baseline;padding:16px 0;border-bottom:2px dashed var(--line)}}.nadm .nrow time{{color:var(--blue-ink);font-weight:800;font-size:14px;width:96px;flex:none}}.nadm .nrow .t{{font-weight:800;flex:1;min-width:200px}}.nadm .nrow .t small{{display:block;font-weight:500;color:var(--soft)}}.nadm .new{{background:var(--coral);color:#fff;border-radius:999px;padding:1px 9px;font-size:11px;margin-left:6px}}.nadm .msg{{color:var(--soft);font-weight:700;margin:8px 0 0}}.nadm .box{{background:#fff;border:2px solid var(--ink);border-radius:20px;padding:22px}}</style>
<div class="nadm">
<div id="setup" class="box" hidden></div>
<form class="form" id="login" style="max-width:420px"><label>비밀번호<input type="password" id="pw" autocomplete="current-password"></label><button class="btn sun" type="submit">들어가기<span class="ar">{ARROW}</span></button><p id="lmsg" class="msg" style="color:var(--coral)"></p></form>
<div id="panel" hidden>
  <form class="form box" id="nf"><input type="hidden" id="nid">
    <div class="row2"><label>날짜<input id="nd" placeholder="2026.11.20"></label><label>NEW 표시<select id="nn"><option value="1">표시함</option><option value="0">표시 안 함</option></select></label></div>
    <label>제목 *<input id="nt" maxlength="120"></label>
    <label>내용 (선택)<textarea id="nb" rows="4" maxlength="1500" placeholder="자세한 안내가 있으면 적어 주세요."></textarea></label>
    <div class="btns"><button class="btn sun" type="submit">저장하기<span class="ar">{ARROW}</span></button><button class="btn line" type="button" id="nreset">새로 쓰기<span class="ar">{ARROW}</span></button></div>
    <p id="nmsg" class="msg" role="status"></p>
  </form>
  <h2 class="h2" style="font-size:26px;margin:36px 0 6px">올린 공지</h2>
  <div id="nlist"></div>
</div>
</div>
<script>
(function(){{
  var SERVER = '{gurl}', KEY = 'fj-notice-pw';
  var $ = function(i){{ return document.getElementById(i); }};
  var pw = ''; try {{ pw = sessionStorage.getItem(KEY) || ''; }} catch(e) {{}}
  var list = [];
  function esc(t){{ return String(t==null?'':t).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}}); }}
  function call(body){{
    body.pw = pw;
    return fetch(SERVER, {{method:'POST', headers:{{'Content-Type':'text/plain;charset=utf-8'}}, body: JSON.stringify(body)}}).then(function(r){{return r.json();}});
  }}
  function today(){{ var d=new Date(); return d.getFullYear()+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+('0'+d.getDate()).slice(-2); }}
  function reset(){{ $('nid').value=''; $('nd').value=today(); $('nt').value=''; $('nb').value=''; $('nn').value='1'; }}
  function draw(){{
    $('nlist').innerHTML = list.length ? list.map(function(n,i){{
      return '<div class="nrow"><time>'+esc(n.d)+'</time><span class="t">'+esc(n.t)+(n.n?'<span class="new">NEW</span>':'')+(n.b?'<small>'+esc(n.b)+'</small>':'')+'</span><span class="btns"><button class="btn sm line" data-e="'+i+'">수정</button><button class="btn sm" data-x="'+i+'">삭제</button></span></div>';
    }}).join('') : '<p class="msg">아직 이 화면으로 올린 공지가 없습니다. (처음 열 때 홈페이지에 보이는 기본 공지는 사이트에 들어 있는 것입니다.)</p>';
  }}
  function open(){{
    $('login').hidden = true; $('panel').hidden = false; reset();
    call({{action:'notice-list'}}).then(function(j){{ if(j && j.ok){{ list=j.notices||[]; draw(); }} else {{ $('login').hidden=false; $('panel').hidden=true; $('lmsg').textContent=(j&&j.error)||'열 수 없습니다.'; }} }})
      .catch(function(){{ $('lmsg').textContent='서버에 연결하지 못했습니다.'; $('login').hidden=false; $('panel').hidden=true; }});
  }}
  if(!SERVER){{
    $('login').hidden = true;
    var s = $('setup'); s.hidden = false;
    s.innerHTML = '<b>아직 공지 서버가 연결되지 않았습니다.</b><br>큰길브리지가 사진 업로드 서버(apps-script/gallery)를 배포하고 주소를 넣으면 이 화면이 열립니다. 그 전에는 큰길브리지(1533-7295)에 공지 내용을 알려 주세요.';
  }}
  $('login').addEventListener('submit', function(e){{
    e.preventDefault(); pw = $('pw').value; if(!pw) return;
    try {{ sessionStorage.setItem(KEY, pw); }} catch(x) {{}}
    open();
  }});
  $('nf').addEventListener('submit', function(e){{
    e.preventDefault();
    var t = $('nt').value.trim(); if(!t){{ $('nmsg').textContent='제목을 적어 주세요.'; return; }}
    $('nmsg').textContent='저장하는 중…';
    call({{action:'notice-save', notice:{{id:$('nid').value, d:$('nd').value, t:t, b:$('nb').value, n:$('nn').value==='1'}}}})
      .then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); reset(); $('nmsg').textContent='저장했습니다. 홈페이지에는 몇 분 안에 보입니다.'; }} else $('nmsg').textContent=(j&&j.error)||'저장하지 못했습니다.'; }})
      .catch(function(){{ $('nmsg').textContent='서버에 연결하지 못했습니다.'; }});
  }});
  $('nreset').addEventListener('click', reset);
  $('nlist').addEventListener('click', function(e){{
    var b = e.target.closest('button'); if(!b) return;
    if(b.dataset.e){{ var n=list[+b.dataset.e]; $('nid').value=n.id; $('nd').value=n.d; $('nt').value=n.t; $('nb').value=n.b||''; $('nn').value=n.n?'1':'0'; scrollTo({{top:0,behavior:'smooth'}}); }}
    if(b.dataset.x && confirm('이 공지를 삭제할까요?')){{ var n2=list[+b.dataset.x]; call({{action:'notice-delete', id:n2.id}}).then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); }} else alert((j&&j.error)||'삭제하지 못했습니다.'); }}); }}
  }});
  if(SERVER && pw) open();
}})();
</script></div></section>"""
    page('notice-admin.html', f'공지사항 관리 | {NAME}', '공지사항 관리 화면', body, '', extra_head='<meta name="robots" content="noindex,nofollow">')


# ════════════════════════ 견적 문의 ════════════════════════
def build_contact():
    opts = ''.join(f'<option value="{m["k"]}">{m["n"]}</option>' for m in MENU) + '<option value="kids">유아체육 · 체험놀이</option><option value="etc">기타</option>'
    faq = ''.join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    hours = ''.join(f'<li>{h}</li>' for h in HOURS)
    kk = f'<a class="cc" href="{KAKAO}" target="_blank" rel="noopener"><b>카카오톡</b><span>채널로 바로 상담</span></a>' if KAKAO else ''
    body = phead('견적 문의', 'CONTACT', '날짜 · 장소 · 인원만<br><span class="hl">알려 주세요</span>', '전화, 문자, 아래 양식 어느 쪽이든 괜찮습니다.') + f'''
<section class="sec"><div class="wrap cgrid">
  <form class="form rv" id="form" data-endpoint="{FORM_ENDPOINT}" data-tel="{TEL_RAW}" data-email="{EMAIL}" novalidate>
    <h2>견적 문의 양식</h2>
    <label>성함 · 기관명<input name="name" required autocomplete="organization" placeholder="예: ○○어린이집 원장"></label>
    <label>연락처<input name="phone" required type="tel" inputmode="tel" autocomplete="tel" placeholder="010-0000-0000"></label>
    <label>필요한 서비스<select name="service">{opts}</select></label>
    <div class="row2"><label>행사 날짜<input name="date" placeholder="예: 11월 20일 / 미정"></label><label>예상 인원<input name="people" placeholder="예: 80명"></label></div>
    <label>장소<input name="place" placeholder="예: 화성시 ○○초등학교 운동장"></label>
    <label>문의 내용<textarea name="msg" rows="4" placeholder="원하시는 프로그램이나 궁금한 점"></textarea></label>
    <label class="agree"><input type="checkbox" name="agree" required> 문의 답변을 위해 성함 · 연락처를 사용하는 데 동의합니다.</label>
    <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
    <button class="btn sun" type="submit">문의 보내기<span class="ar">{ARROW}</span></button>
    <p class="fmsg" role="status" aria-live="polite"></p>
  </form>
  <aside class="rv d1">
    <a class="cc big" href="tel:{TEL_RAW}"><b>전화 상담</b><span>{TEL}</span></a>
    <a class="cc" href="sms:{TEL_RAW}"><b>문자 상담</b><span>{TEL}</span></a>
    {kk}
    <a class="cc" href="mailto:{EMAIL}"><b>이메일</b><span>{EMAIL}</span></a>
    <div class="cc plain"><b>영업시간</b><ul class="hrs">{hours}</ul></div>
    <div class="cc plain"><b>주소</b><span>{ADDR}</span><a class="map" href="{MAP}" target="_blank" rel="noopener">네이버 지도에서 보기 →</a></div>
  </aside>
</div></section>
<section class="sec cream"><div class="wrap two">
  <div><span class="eb"><i></i>FAQ</span><h2 class="h2 rv">자주 묻는 <span class="hl">질문</span></h2></div>
  <div class="faq">{faq}</div>
</div></section>'''
    page('contact.html', f'견적 문의 | {NAME}', 'F&J 이벤트 견적 문의. 전화 010-9121-9982, 문자, 문의 양식. 경기 화성.', body, 'contact.html', extra_head=jsonld_faq())


def build_404():
    body = f'<section class="phead"><div class="wrap"><span class="eb"><i></i>404</span><h1>찾는 페이지가 없어요</h1><p class="lead">주소가 바뀌었거나 잘못 입력되었을 수 있어요.</p><div class="btns" style="margin-top:24px">{btn("index.html", "처음으로", "sun")}</div></div></section>'
    page('404.html', f'페이지를 찾을 수 없어요 | {NAME}', '페이지를 찾을 수 없습니다.', body)


def build_seo():
    pages = ['', 'about.html', 'event.html', 'kids.html', 'portfolio.html', 'notice.html', 'contact.html', 'quote.html']
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sm)
    rb = ('User-agent: *\nDisallow: /\n' if NOINDEX else 'User-agent: *\nAllow: /\nDisallow: /contract.html\nDisallow: /statement.html\nDisallow: /office.html\nDisallow: /schedule.html\nDisallow: /upload.html\nDisallow: /notice-admin.html\n') + f'Sitemap: {BASE}/sitemap.xml\n'
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(rb)
    ll = f'''# {NAME_FULL}
> 경기 화성의 유아체육 · 이벤트 행사 전문. 어린이집 · 유치원 · 초등학교 운동회, 에어바운스, 워터슬라이드, 수영장 대여, 음향 · 조명, 레크리에이션을 15년 이상 진행.

- 대표: {CEO} · 전화 {TEL} · {EMAIL}
- 주소: {ADDR}
- 영업시간: {' / '.join(HOURS)}
- 진행 실적: 경기 남부 운동회 연 100회, 물놀이 행사 연 50회, 경기도교육청 행사 진행
- 서비스: 음향 · 조명 / 체육대회 · 운동회 / 놀이기구 · 에어바운스 / 워터슬라이드 · 수영장 / 레크리에이션 / 송년회 · 신년회 / 유아체육 · 체험놀이 · 교구 대여 · 발표회

## 페이지
- [회사 소개]({BASE}/about.html)
- [행사 · 대여]({BASE}/event.html)
- [유아체육 · 체험]({BASE}/kids.html)
- [포트폴리오]({BASE}/portfolio.html)
- [견적 문의]({BASE}/contact.html)
'''
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8', newline='\n').write(ll)


if __name__ == '__main__':
    build_index(); build_about(); build_event(); build_kids(); build_portfolio(); build_notice(); build_notice_admin(); build_contact(); build_404(); build_seo()
