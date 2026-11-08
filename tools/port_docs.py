# -*- coding: utf-8 -*-
"""
큰길이벤트기획의 업무 도구를 이 회사용으로 옮긴다.

  python tools/port_docs.py [큰길이벤트 레포 경로]      (기본 ~/Documents/클로드코드)

옮기는 것: 견적서(quote.html + quote-catalog.js) · 전자계약서 · 거래명세서 · 사진 올리기 ·
          행사 일정(schedule.html) · 서버 코드 2개(apps-script/contract · gallery) · 대표 전용 업무 문서함(office.html)
원본을 고친 뒤 다시 돌리면 같은 규칙으로 다시 옮긴다. 결과 HTML 은 손으로 고치지 말고 여기 규칙으로 넣을 것.

▶ 다른 회사에 쓰려면 「회사 설정」 칸만 바꾸면 된다(아래 「공통 규칙」은 그대로).
"""
import os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/클로드코드')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ════════════════════════════ 회사 설정 ════════════════════════════
ID       = 'fj'                                     # 기기 저장 이름 · 유입 표시(data-site) 앞글자
NAME     = 'F&J 이벤트'
NAME_EN  = 'FUN & JOY EVENT'
CEO      = '최원창'
BIZNO    = '508-34-00436'                           # 계약서 KB-20260923-321
ADDR     = '경기도 화성시 효행구 비봉면 일묵동안길 3-6'
ADDR_S   = '경기도 화성시 효행구 비봉면 일묵동안길 3-6'
TEL      = '010-9121-9982'
EMAIL    = 'cwc9982@naver.com'
REPO     = 'brizymedia/fj-event'
HOME     = 'https://brizymedia.github.io/fj-event'  # 도메인(F&J EVENT.co.kr 희망)을 정하면 바꾸고 다시 실행
CODE_PRE = 'FJ-'                                    # 계약 번호 앞글자
BLOG     = 'https://blog.naver.com/funandjoy12'

# 서버(앱스 스크립트) — 배포하면 주소를 넣고 다시 돌린다. 비어 있으면 서버 없이 동작(저장함은 이 기기만, 계약은 긴 링크).
CONTRACT_URL = ''   # apps-script/contract 배포 뒤 /exec 주소
GALLERY_URL  = ''   # apps-script/gallery 배포 뒤 /exec 주소

LOGO_FILE = 'assets/img/favicon.svg'                # 머리글에 쓰는 네모 마크
MAIL_LOGO = HOME + '/assets/img/logo-mark.png'      # 메일 머리(PNG — 메일은 SVG 를 못 읽는다. favicon.svg 를 변환해 둔 것)
STAMP     = 'assets/img/stamp-fj.png'               # 대표 인감(투명 PNG). 파일이 없으면 「(인)」 자리만

# 색: 큰길이벤트 주황 → F&J 팔레트 (잉크 #1F2A44 · 해바라기 노랑 #FFC21A · 파랑 #2E9BFF · 산호 #FF6B5B)
COLORS = [
    ('#F59E0B', '#FFC21A'), ('#FBBF24', '#FFD35C'), ('#D97706', '#F5A800'), ('#B45309', '#C98600'),
    ('#FCD34D', '#FFE08A'), ('#a05c00', '#8A5A00'), ('#09090b', '#1F2A44'), ('#0B0A10', '#1F2A44'),
    ('#16141C', '#2A3757'), ('#131317', '#2A3757'),
    ('rgba(245,158,11', 'rgba(255,194,26'), ('rgba(251,191,36', 'rgba(255,211,92'),
    ('rgba(9,9,11', 'rgba(31,42,68'), ('rgba(11,10,16', 'rgba(31,42,68'),
]
# 업무 문서함(office.html) 색 — accent2 는 COLORS 의 '#FBBF24' 변환값과 같아야 한다(upload 안내문 치환이 그 색을 찾는다)
OFFICE = dict(bg='#1F2A44', card='#2A3757', line='rgba(255,194,26,.22)', accent='#FFC21A', accent2='#FFD35C', ink='#1F2A44')

# 예시 문구(견적서 · 계약서 입력칸 회색 글씨)
EXAMPLES = [
    ('예) 광양시청 / ○○총동문회', '예) ○○어린이집 / ○○초등학교'),
    ('예) 광양시 광양읍 일원', '예) 화성시 ○○초등학교 운동장'),
    ('예) 제25회 광양 매화축제', '예) 2026 ○○초등학교 가을운동회'),
    ('예) 고흥군청 문화관광과', '예) ○○초등학교 행정실'),
    ('고흥군 녹동항 일원', '화성시 ○○초등학교'),
    ('2026 녹동바다불꽃축제 무대음향 운영', '2026 ○○초등학교 가을운동회 진행'),
    ('2026 녹동바다불꽃축제 무대·음향 운영', '2026 ○○초등학교 가을운동회 진행'),
    ("spec:'전남 외 지역'", "spec:'경기 남부 외 지역'"),
    ('예: 2026 진향제', '예: 2026 ○○초등학교 가을운동회'),          # 행사 일정
    ('예: 광양읍 공설운동장', '예: ○○초등학교 운동장'),
    ('예: 한국항만물류고등학교', '예: ○○초등학교 행정실'),
]

QUOTE_TITLE = '자동 견적서 — 운동회 · 에어바운스 · 워터슬라이드 · 음향 조명 · 유아체육 | F&J 이벤트'
QUOTE_DESC  = '경기 화성 F&J 이벤트(펀앤조이 체육교실). 운동회 · 체육대회, 레크리에이션, 에어바운스, 워터슬라이드, 수영장 대여, 음향 · 조명, 유아체육까지. 필요한 항목만 골라 견적을 문의하세요. 010-9121-9982'

CATALOG = """const CATALOG = [
  { group:'행사 진행', items:[
    { id:'p1', name:'운동회 · 체육대회',        spec:'어린이집 · 유치원 · 초등학교 · 기업 · 종목 기획 · 진행 · 음향', unit:'식', price:null },
    { id:'p2', name:'레크리에이션',             spec:'연령과 분위기에 맞춘 진행 · 단체 게임 · 응원전',             unit:'식', price:null },
    { id:'p3', name:'송년회 · 신년회 · 시무식 · 종무식', spec:'진행 · 게임 · 음향 구성',                           unit:'식', price:null },
  ]},
  { group:'장비 · 대여', items:[
    { id:'a1', name:'음향 · 조명 무대세팅',      spec:'무대 음향 · 조명 · 설치 · 철수 포함',   unit:'식', price:null },
    { id:'a2', name:'에어바운스 · 놀이기구',     spec:'세팅 · 운영 · 철수 포함',               unit:'동', price:null, qty:true },
    { id:'a3', name:'워터슬라이드',              spec:'여름 물놀이 · 설치 · 안전 운영 · 철수 포함', unit:'동', price:null, qty:true },
    { id:'a4', name:'수영장 대여',               spec:'설치 · 철수 포함',                       unit:'동', price:null, qty:true },
  ]},
  { group:'유아체육 · 체험놀이', items:[
    { id:'k1', name:'유아체육',                  spec:'연령에 맞춘 체육 수업 · 스카프 · 낙하산 등 교구 활용', unit:'회', price:null, qty:true },
    { id:'k2', name:'체험놀이',                  spec:'실내 역할 놀이 · 체험 프로그램',          unit:'회', price:null, qty:true },
    { id:'k3', name:'교구 대여',                 spec:'놀이 · 수업용 교구',                      unit:'세트', price:null, qty:true },
    { id:'k4', name:'발표회 의상 · 진행',        spec:'어린이집 · 유치원 발표회 의상 · 무대 · 진행', unit:'식', price:null },
  ]},
];"""

# 사진 올리기 — 사진 칸(포트폴리오 페이지 분류). slug 는 portfolio.html 필터(data-f)와 같게 둔다
UPLOAD_CATS = """const 갤러리항목 = [
  { slug: 'sports', name: '운동회 · 체육대회',
    desc: '어린이집 · 유치원 · 초등학교 운동회와 기업 체육대회. 종목 기획부터 진행, 장비까지 맡은 현장입니다.' },
  { slug: 'bounce', name: '에어바운스 · 놀이기구',
    desc: '어린이날 행사와 축제의 에어바운스 · 놀이기구 세팅과 운영 현장입니다.' },
  { slug: 'water',  name: '물놀이 · 수영장',
    desc: '워터슬라이드와 수영장 대여, 여름 물놀이 행사 현장입니다.' },
  { slug: 'kids',   name: '유아체육 · 체험놀이',
    desc: '유아체육 수업, 체험놀이, 교구, 발표회 현장입니다.' },
];"""

# 사진 올리기 — 행사명 · 장소 글자에서 지역 찾기
UPLOAD_REGIONS = """const 지역표 = [
  ['동탄', ['동탄']], ['향남', ['향남', '발안']], ['봉담', ['봉담']], ['비봉', ['비봉']], ['화성', ['화성']],
  ['수원', ['수원']], ['오산', ['오산']], ['안산', ['안산', '상록', '단원']], ['시흥', ['시흥']], ['평택', ['평택']],
  ['군포', ['군포']], ['용인', ['용인']], ['안성', ['안성']], ['인천', ['인천']], ['서울', ['서울']], ['경기', ['경기']],
];"""

# 사진 올리기 — 블로그 · 인스타 글을 만들 때 쓰는 이 회사 말
UPLOAD_PAIRS = [
    ("['순천', '여수', '광양', '고흥', '하동', '남원', '광주', '진주', '통영']", "['화성', '동탄', '수원', '오산', '안산', '시흥', '평택', '인천', '군포', '용인']"),
    ("  ['천막',   ['천막', '몽골텐트', '부스']],\n];", "  ['천막',   ['천막', '몽골텐트', '부스']],\n  ['운동회', ['운동회', '체육대회', '레크', '레크리에이션']],\n  ['에어바운스', ['에어바운스', '놀이기구', '슬라이드']],\n  ['물놀이', ['워터슬라이드', '수영장', '물놀이']],\n  ['유아체육', ['유아체육', '체험놀이', '교구', '발표회']],\n];"),
    ("'F&J 이벤트 · 전남광주통합특별시 광양'", "'F&J 이벤트 · 경기 화성'"),
    ("'행사기획 · 무대 · 음향 · LED · 조명 · MC/가수 섭외 · 드론쇼 — 광주·전남·경남 전역'", "'운동회 · 에어바운스 · 워터슬라이드 · 수영장 대여 · 음향 조명 · 유아체육 — 경기 남부'"),
    ("' 등 광주·전남·경남 어디든 광양에서 출발해 당일 세팅합니다. '", "' 등 경기 남부 어디든 장비를 싣고 가서 당일 세팅합니다. '"),
    ("당일 안에 개략 견적을 드립니다.", "빠르게 1차 구성안과 견적을 드립니다."),
    ("(지역 ? 지역 : '전남') + ' 일원에서", "(지역 ? 지역 : '화성') + ' 일원에서"),
    ("'행사기획', '행사대행', '이벤트회사추천', '전남이벤트', '경남이벤트', '광양이벤트', 'F&J 이벤트'", "'행사기획', '운동회', '에어바운스', '워터슬라이드', '화성이벤트', '동탄이벤트', 'F&J이벤트'"),
    ("    '천막':   '천막·부스 설치',\n  };", "    '천막':   '천막·부스 설치',\n    '운동회': '운동회 · 체육대회 · 레크리에이션 진행',\n    '에어바운스': '에어바운스 · 놀이기구 설치와 운영',\n    '물놀이': '워터슬라이드 · 수영장 설치와 운영',\n    '유아체육': '유아체육 · 체험놀이 · 교구 · 발표회',\n  };"),
    ("'천막': ['천막대여'] };", "'천막': ['천막대여'], '운동회': ['운동회', '체육대회'], '에어바운스': ['에어바운스'], '물놀이': ['워터슬라이드', '수영장대여'], '유아체육': ['유아체육', '체험놀이'] };"),
    ("(무대·음향·LED·조명·MC·가수·드론쇼)", "(운동회 · 에어바운스 · 워터슬라이드 · 음향 · 조명 · 유아체육)"),
]
UPLOAD_PLACEHOLDER = '예) 화성 ○○초등학교 운동장에서 열린 가을운동회. 학년별 종목을 구성하고 레크리에이션 진행과 음향, 에어바운스 운영을 맡았습니다.'

# 머리글 메뉴: 큰길이벤트 주소 → 이 회사 페이지
NAV_SITE = [
    ('href="index.html#services"', 'href="event.html"'),
    ('href="index.html#portfolio"', 'href="portfolio.html"'),
    ('href="index.html#gallery"', 'href="portfolio.html"'),
    ('href="/blog/"', 'href="notice.html"'),
    ('>서비스</a>', '>행사 · 대여</a>'),
    ('>행사이력</a>', '>포트폴리오</a>'),
    ('>블로그</a>', '>공지사항</a>'),
]
GALLERY_PAGE = 'portfolio.html'                     # 사진이 모이는 페이지
# ════════════════════════════ 회사 설정 끝 ════════════════════════════


def common():
    return [
        ('큰길이벤트기획 (주식회사 브리지미디어)', NAME),
        (' <span style="color:#9ca3af;">(주식회사 브리지미디어)</span>', ''),
        ('주식회사 브리지미디어 대표 직인', NAME + ' 대표 직인'),
        ('(예금주: 주식회사 브리지미디어)', ''),
        ('주식회사 브리지미디어', NAME),
        ('큰길이벤트기획', NAME),
        ('[큰길이벤트]', '[' + NAME + ']'),
        ('큰길이벤트.com/quote.html', HOME.replace('https://', '') + '/quote.html'),
        ('큰길이벤트.com', HOME.replace('https://', '')),
        ('김동길', CEO),
        ('813-81-02252', BIZNO),
        ("corp:'204611-0065269'", "corp:''"),
        ('전남광주통합특별시 광양시 광양읍 강변동길 1, 2층', ADDR),
        ('전남광주통합특별시 광양시 광양읍 강변동길 1', ADDR_S),
        ('1533-7295', TEL),
        ('gilcaro@naver.com', EMAIL),
        ("'KB국민은행 788101-01-397776 '", "''"),
        ("bank:'KB국민은행 788101-01-397776 '", "bank:''"),
        ("'KG-'", "'" + CODE_PRE + "'"),
        ('data-site="keungil"', 'data-site="' + ID + '"'),
        ('keungil-quote-box', ID + '-quote-box'),
        ('keungil-contract', ID + '-contract'),
        ('keungil-statement', ID + '-statement'),
        ('keungil-sched', ID + '-sched'),
        ('우리(큰길)', '우리(' + NAME + ')'),
    ] + EXAMPLES + [
        # 아이콘 · 파비콘
        ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n', ''),
        ('href="/favicon.svg"', 'href="assets/img/favicon.svg"'),
        ('<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n', ''),
        ('  <link rel="alternate" type="application/rss+xml" title="' + NAME + ' 소식" href="/rss.xml">\n', ''),
        ('src="logo-kgm-transparent.png"', 'src="' + LOGO_FILE + '"'),
        ('src="/quote-catalog.js"', 'src="quote-catalog.js"'),
    ] + COLORS


def nav():
    return NAV_SITE + [
        ('href="/stories/"', 'href="stories/"'), ('    <a href="stories/">행사 이야기</a>\n', ''), ('href="/office.html"', 'href="office.html"'),
        ('href="/quote.html', 'href="quote.html'), ('href="/contract.html', 'href="contract.html'),
        ('href="/statement.html', 'href="statement.html'), ('href="/schedule.html', 'href="schedule.html'),
        ('href="/"', 'href="index.html"'),
        ('TOTAL EVENT AGENCY', NAME_EN),
    ]


def img(size, radius):
    return '<img src="' + LOGO_FILE + '" alt="" style="width:' + size + ';height:' + size + ';border-radius:' + radius + ';display:block">'


def logo_fix(s):
    # 「KG」 네모 → 이 회사 마크
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.3rem;height:2\.3rem;[^"]*">KG</span>', img('2.3rem', '.6rem'), s)
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.(1|2)rem;height:2\.(1|2)rem;[^"]*">KG</span>', img('2.1rem', '.55rem'), s)
    s = re.sub(r'<span style="display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;\s*background:[^;]+;[^"]*">KG</span>\s*<span style="[^"]*">' + re.escape(NAME) + '</span>',
               '<img src="' + MAIL_LOGO + '" height="32" alt="' + NAME + '" style="vertical-align:middle;">', s)
    mark = '<img src="' + LOGO_FILE + '" alt="" style="width:26px;height:26px;border-radius:6px;vertical-align:-7px;margin-right:6px">'
    s = re.sub(r'<a class="brand" href="(?:/|index\.html)"><i>KG</i> ([^<]*)</a>', lambda m: '<a class="brand" href="index.html">' + mark + m.group(1) + '</a>', s)
    return s


def no_stamp(s):
    s = s.replace('<img class="stamp" src="stamp-keungil.png" alt="' + NAME + ' 대표 직인" onerror="this.style.display=\'none\'">', '')
    s = s.replace("'stamp-keungil.png'", "'" + STAMP + "'")
    s = s.replace("'https://xn--wk0bn7yi8h24iszc.com/stamp-keungil.png'", "'" + HOME + '/' + STAMP + "'")
    s = s.replace('src="stamp-keungil\\.png', 'src="' + STAMP.replace('/', '\\/').replace('.png', '\\.png'))
    return s


def servers(s):
    s = re.sub(r"'https://script\.google\.com/macros/s/AKfycbwgO5Ry[A-Za-z0-9_-]+/exec'", "'" + CONTRACT_URL + "'", s)
    s = s.replace("const 서버주소_기본 = '';", "const 서버주소_기본 = '" + GALLERY_URL + "';")
    return s


def rep(s, pairs):
    for a, b in pairs:
        s = s.replace(a, b)
    return s


TRACES = ('큰길이벤트', '김동길', '광양', '브리지미디어', '788101', 'xn--wk0', 'keungil', 'KG<', '>KG', '교육연구소', '이벤트와 교육', '황윤수', '578-03', '남동구')


def write(name, s):
    left = [w for w in TRACES if w in s]
    p = os.path.join(SITE, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(name, '남은 큰길 흔적:', left or '없음')


def port(name, extra=None, out=None):
    s = open(os.path.join(SRC, name), encoding='utf-8').read()
    s = rep(s, common())
    # 큰길이벤트 사이트의 검색엔진 소유확인 태그는 옮기지 않는다(이 사이트 것이 아님)
    s = re.sub(r'\s*<!-- 네이버 서치어드바이저 소유확인 -->', '', s)
    s = re.sub(r'\s*<meta name="(?:naver|google)-site-verification"[^>]*>', '', s)
    s = rep(s, nav())
    s = re.sub(r'\s*<a href="' + re.escape(GALLERY_PAGE) + r'"[^>]*>갤러리</a>', '', s) if GALLERY_PAGE != 'gallery.html' else s
    s = logo_fix(s)
    s = no_stamp(s)
    s = servers(s)
    if extra: s = extra(s)
    write(out or name, s)


def noindex(s, title_tag):
    if 'name="robots"' in s: return s
    return s.replace(title_tag, title_tag + '\n<meta name="robots" content="noindex,nofollow">', 1)


def catalog_extra(s):
    a = s.index('const CATALOG = ['); b = s.index('];', a) + 2
    return s[:a] + CATALOG + s[b:]


def quote_extra(s):
    s = re.sub(r'\s*<p class="no-print" id="stamp-note".*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<td valign="middle" align="right" width="66" style="padding-left:6px;">\s*<img src="\$\{직인\}".*?</td>', '', s, count=1, flags=re.S)
    s = s.replace('상호명(…브리지미디어)', '상호명')
    s = re.sub(r'<title>[^<]*</title>', '<title>' + QUOTE_TITLE + '</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + QUOTE_DESC + '">', s, count=1)
    # 손님용 견적서는 검색에 나와도 되지만, 관리자 화면 주소가 같아 큰길이벤트처럼 noindex 를 두지 않는다
    return s


def contract_extra(s):
    s = re.sub(r'\.brand img\{ height:1\.8rem;filter:brightness\(0\) invert\(1\)[^}]*\}', '.brand img{ height:1.8rem;border-radius:.4rem; }', s)
    s = re.sub(r"const STAMP_SRC = '" + re.escape(STAMP) + r"';[^\n]*", "const STAMP_SRC = '" + STAMP + "';  // 대표님 인감(투명 PNG)을 이 이름으로 넣으면 찍힌다. 없으면 「(인)」", s)
    s = s.replace('return `<div class="seal-css">${esc(C.co.brand||C.co.name)}<br>대표<br>인</div>`;', 'return `<div class="seal-none">(인)</div>`;')
    s = s.replace('<span class="stamp-flag ok">날인 완료</span>', "${stampOK?'<span class=\"stamp-flag ok\">날인 완료</span>':''}")
    s = s.replace('  #paper .stamp-flag.ok{', '  #paper .party .sig-slot .box .seal-none{ position:absolute;right:6mm;top:50%;transform:translateY(-50%);color:#9CA3AF;font-size:10pt; }\n  #paper .stamp-flag.ok{', 1)
    return noindex(s, '<title>전자계약서 — ' + NAME + '</title>')


def statement_extra(s):
    s = s.replace("우리.name + ' (' + 우리.brand + ')'", "우리.name")
    s = s.replace("esc(우리.name) + ' (' + esc(우리.brand) + ')'", "esc(우리.name)")
    s = s.replace('alt="' + NAME + ' 대표 직인">', 'alt="' + NAME + ' 대표 직인" onerror="this.remove()">')
    s = s.replace('공급자 칸에 대표 직인이 찍혀 나갑니다. 인쇄 · PDF · 메일 발송본에도 그대로 들어갑니다.', '인쇄하거나 PDF 로 저장해 보내시면 됩니다.')
    return s


def schedule_extra(s):
    s = s.replace('<i>KG</i> ', '<img src="' + LOGO_FILE + '" alt="" style="width:26px;height:26px;border-radius:6px;vertical-align:-7px;margin-right:6px">')
    return s


def upload_extra(s):
    a = s.index('const 갤러리항목 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_CATS + s[b:]
    a = s.index('const 지역표 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_REGIONS + s[b:]
    pairs = [
        ("'https://raw.githubusercontent.com/brizymedia/keungil-event/photos/photos/photos.json'", "'https://raw.githubusercontent.com/" + REPO + "/photos/photos/photos.json'"),
        ("'https://cdn.jsdelivr.net/gh/brizymedia/keungil-event@photos/'", "'https://cdn.jsdelivr.net/gh/" + REPO + "@photos/'"),
        ("'https://큰길이벤트.com'", "'" + HOME + "'"),
        ("홈주소 + '/gallery.html#' + 갤러리슬러그(이름)", "홈주소 + '/" + GALLERY_PAGE + "'"),
        ("'kg_", "'" + ID + "_"),
        # 이 회사에는 사진으로 행사 이야기 글을 자동으로 만드는 작업이 없다 — 안내를 사실대로
        ('여기 쓰신 글이 <b style="color:' + OFFICE['accent2'] + ';">홈페이지의 「행사 이야기」 글로 그대로 올라갑니다.</b>\n      고객이 읽고, 네이버·구글·AI 검색에도 잡힙니다. 아래 블로그·인스타 글을 만들 때도 쓰입니다.',
         '여기 쓰신 글은 <b style="color:' + OFFICE['accent2'] + ';">현장사진 페이지의 사진 설명</b>으로 저장되고, 아래 <b style="color:' + OFFICE['accent2'] + ';">블로그 · 인스타 글</b>을 만들 때 쓰입니다.'),
        ('\n      <b>비워두면 글 페이지가 만들어지지 않습니다.</b>', ''),
        ('<b style="color:#a1a1aa;">행사 이야기 글의 대표 이미지</b>와\n        갤러리 칸 표지로 쓰입니다.', '<b style="color:#a1a1aa;">블로그 대표 이미지</b>로 쓰기 좋게 만들어 드립니다.'),
    ] + UPLOAD_PAIRS
    s = rep(s, pairs)
    s = re.sub(r'placeholder="예\) 순천만 일원에서[^"]*"', 'placeholder="' + UPLOAD_PLACEHOLDER + '"', s)
    return noindex(s, '<title>행사 사진 올리기 — ' + NAME + '</title>')



NOTICE_GS = """

/* ══════════════════════════════════════════════════════════════
   7. 공지사항 (F&J 이벤트 추가 기능)
   photos 브랜치의 photos/notices.json 에 공지 목록을 두고, 홈페이지가 읽어 보여 준다.
   요청: {action:'notice-list'} · {action:'notice-save', notice:{id?, d, t, b, n}} · {action:'notice-delete', id}
══════════════════════════════════════════════════════════════ */
const 공지파일 = 저장경로 + '/notices.json';

function 공지읽기() {
  const 응 = 깃허브(공지파일, 'get');
  if (응.getResponseCode() === 404) return { updated: '', notices: [] };
  try {
    const 내용 = JSON.parse(응.getContentText());
    const 값 = JSON.parse(Utilities.newBlob(Utilities.base64Decode(내용.content)).getDataAsString());
    return { updated: 값.updated || '', notices: Array.isArray(값.notices) ? 값.notices : [] };
  } catch (err) {
    throw new Error('notices.json 을 읽지 못했습니다: ' + err.message);
  }
}

function 공지쓰기(목록, 메모) {
  목록.updated = new Date().toISOString();
  목록.notices = 목록.notices.slice(0, 80);
  const 본문 = Utilities.base64Encode(Utilities.newBlob(JSON.stringify(목록, null, 1)).getBytes());
  return 깃허브에올리기(공지파일, 본문, 메모);
}

function 공지글자(값, 최대) {
  return String(값 == null ? '' : 값).replace(/[<>]/g, '').trim().slice(0, 최대);
}

function 공지저장(요청) {
  const 입력 = 요청.notice || {};
  const 제목 = 공지글자(입력.t, 120);
  if (!제목) return { ok: false, error: '제목을 적어 주세요.' };
  const 목록 = 공지읽기();
  const 글 = {
    id: 공지글자(입력.id, 40) || ('n' + Date.now().toString(36)),
    d: 공지글자(입력.d, 20) || Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy.MM.dd'),
    t: 제목,
    b: 공지글자(입력.b, 1500),
    n: !!입력.n,
  };
  const 자리 = 목록.notices.findIndex(function (x) { return x.id === 글.id; });
  if (자리 >= 0) 목록.notices[자리] = 글; else 목록.notices.unshift(글);
  const 결과 = 공지쓰기(목록, '공지 ' + (자리 >= 0 ? '수정' : '추가') + ': ' + 제목.slice(0, 30));
  if (!결과.ok) return 결과;
  return { ok: true, notices: 목록.notices };
}

function 공지삭제(요청) {
  const 목록 = 공지읽기();
  const 전 = 목록.notices.length;
  목록.notices = 목록.notices.filter(function (x) { return x.id !== 요청.id; });
  if (목록.notices.length === 전) return { ok: false, error: '없는 공지입니다.' };
  const 결과 = 공지쓰기(목록, '공지 삭제');
  if (!결과.ok) return 결과;
  return { ok: true, notices: 목록.notices };
}
"""

# ── 서버 코드(앱스 스크립트) — 형님 구글 계정으로 배포한다 ──
def port_servers():
    c = open(os.path.join(SRC, 'apps-script/contract/Code.gs'), encoding='utf-8').read()
    c = rep(c, [
        (' * 큰길이벤트기획 — 전자계약 서버 (Google Apps Script)', ' * ' + NAME + ' — 전자계약 서버 (Google Apps Script)'),
        ("const COMPANY_EMAIL    = 'gilauto325@gmail.com';    //", "const COMPANY_EMAIL    = '" + EMAIL + "';    //"),
        ("const ROOT_FOLDER_NAME = '큰길이벤트기획 계약서';", "const ROOT_FOLDER_NAME = '" + NAME + " 계약서';"),
        ("const COMPANY_NAME     = '큰길이벤트기획';", "const COMPANY_NAME     = '" + NAME + "';"),
        ("service: 'keungil-contract'", "service: '" + ID + "-contract'"),
        ('const recipients = uniq_([COMPANY_EMAIL, to.company', 'const recipients = uniq_([COMPANY_EMAIL, MANAGER_EMAIL, to.company'),
    ])
    c = c.replace("    // 서명본 사본을 항상 받을 주소 (계약서의 co.email 과 별개로 무조건 수신)\n",
                  "    // 서명본 사본을 항상 받을 주소 (계약서의 co.email 과 별개로 무조건 수신)\nconst MANAGER_EMAIL    = 'gilauto325@gmail.com'; // 관리하는 큰길브리지도 사본을 받는다 (빼려면 '' )\n", 1)
    c = c.replace('형님과 직원이', '대표님과 직원이').replace('형님 암호(BOX_PW)', '대표님 암호(BOX_PW)')
    assert 'MANAGER_EMAIL    =' in c, '계약 서버: MANAGER_EMAIL 넣을 자리를 못 찾음'
    # 보낸 견적 메일 모으기: 큰길 견적 메일([큰길이벤트기획] …)이 이 회사 저장함에 섞이지 않게 제목 머리를 이 회사로 (2026-11-06 어대리 발견 — 같은 gilauto325 계정에서 돈다)
    c = c.replace('/^\[큰길이벤트기획\]/', '/^\[' + NAME + '\]/').replace('「[큰길이벤트기획] … 견적서」', '「[' + NAME + '] … 견적서」')
    assert '[큰길이벤트기획\]' not in c, '계약 서버: 큰길 견적 메일 거르는 조건이 남음'
    write('apps-script/contract/Code.gs', c)
    g = open(os.path.join(SRC, 'apps-script/gallery/Code.gs'), encoding='utf-8').read()
    g = rep(g, [
        (' * 큰길이벤트기획 · 행사 사진 업로드 서버', ' * ' + NAME + ' · 행사 사진 업로드 서버'),
        ('GITHUB_REPO    brizymedia/keungil-event', 'GITHUB_REPO    ' + REPO),
        ("'큰길이벤트기획 사진 업로드 서버'", "'" + NAME + " 사진 업로드 서버'"),
        ("'keungil-photo-uploader'", "'" + ID + "-photo-uploader'"),
    ])
    g = g.replace("    if (요청.action === 'delete') return 응답(잠그고(function () { return 사진삭제(요청); }));",
                  "    if (요청.action === 'delete') return 응답(잠그고(function () { return 사진삭제(요청); }));\n"
                  "    if (요청.action === 'notice-list')   return 응답({ ok: true, notices: 공지읽기().notices });\n"
                  "    if (요청.action === 'notice-save')   return 응답(잠그고(function () { return 공지저장(요청); }));\n"
                  "    if (요청.action === 'notice-delete') return 응답(잠그고(function () { return 공지삭제(요청); }));")
    assert 'notice-save' in g, '갤러리 서버: doPost 연결 자리를 못 찾음'
    g = g.rstrip() + '\n' + NOTICE_GS
    write('apps-script/gallery/Code.gs', g)


# ── 대표 전용 업무 문서함 ──
def office():
    O = OFFICE
    tools = [
        ('견적 · 계약', [
            ('quote.html?admin=1', '견적서 발행', '항목을 골라 견적서를 만들고 메일 · 인쇄 · PDF 로 보냅니다. 「견적서 저장함」 단추로 저장 · 찾기 · 불러오기.'),
            ('quote.html', '손님용 자동 견적서', '고객이 항목을 골라 문의하는 화면입니다. 고객에게는 이 주소를 보내세요(금액 · 직인은 안 보입니다).'),
            ('contract.html?admin=1', '전자계약서', '견적서에서 넘어오거나 직접 써서 서명 링크를 만듭니다. 고객은 폰으로 서명하고, PDF 가 메일로 옵니다.'),
            ('statement.html?admin=1', '거래명세서', '행사가 끝난 뒤 견적서에서 「이 견적으로 거래명세서 작성」을 누르면 내용이 그대로 넘어옵니다.'),
        ]),
        ('행사 준비', [
            ('schedule.html', '행사 일정 · 체크리스트', '월간 일정표와 행사별 챙길 품목. 직원과 같은 목록을 봅니다(직원 암호로는 일정만 열림).'),
            ('upload.html', '사진 올리기 + 블로그 · 인스타 글', '현장 사진을 올리면 ' + GALLERY_PAGE.replace('.html', '') + ' 페이지에 붙고, 블로그 · 인스타 글을 같이 만들어 줍니다.'),
        ]),
        ('홈페이지 · 검색', [
            ('notice-admin.html', '공지사항 관리', '공지 · 새 소식을 작성해 홈페이지 공지사항에 올립니다.'),
            ('portfolio.html', '포트폴리오', '현장 사진이 모이는 페이지입니다.'),
            ('llms.txt', 'AI 검색 안내문 (llms.txt)', '챗GPT · 퍼플렉시티 같은 AI 가 회사 정보를 정확히 읽도록 정리한 글입니다.'),
            ('sitemap.xml', '사이트맵', '검색엔진에 알려 주는 페이지 목록입니다.'),
            ('https://www.ai-make.co.kr/stats/', '유입 현황', '어디서 몇 명이 들어왔는지(네이버 · 구글 · AI 검색 · 카톡) 큰길브리지가 함께 봅니다.'),
        ]),
    ]
    cards = ''
    for title, items in tools:
        cards += '<section class="grp"><h2>' + title + '</h2><div class="cards">'
        for href, name, desc in items:
            ext = href.startswith('http')
            cards += ('<a class="card" href="' + href + '"' + (' target="_blank" rel="noopener"' if ext else '') + '><b>' + name +
                      ('<i>↗</i>' if ext else '<i>→</i>') + '</b><span>' + desc + '</span><code>' + href.replace('https://', '') + '</code></a>')
        cards += '</div></section>'
    flow = ['문의가 오면 메일로 알림', '견적서 발행 · 저장', '전자계약 서명', '행사 일정 · 체크리스트', '행사 진행', '사진 올리기 · 블로그 글', '거래명세서']
    flow_html = ''.join('<li><em>' + str(i + 1) + '</em>' + f + '</li>' for i, f in enumerate(flow))
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>업무 문서함 — {NAME} 대표 전용</title>
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="{ID}"></script>
<style>
*,*::before,*::after{{box-sizing:border-box}}[hidden]{{display:none!important}}
body,h1,h2,p,ol{{margin:0}}
body{{background:{O['bg']};color:#fff;font-family:'Pretendard',system-ui,'Malgun Gothic',sans-serif;word-break:keep-all;-webkit-font-smoothing:antialiased;line-height:1.65}}
a{{color:inherit;text-decoration:none}}
.top{{position:sticky;top:0;z-index:5;background:{O['bg']}ee;backdrop-filter:blur(12px);border-bottom:1px solid {O['line']}}}
.top div{{max-width:64rem;margin:0 auto;padding:.85rem 1.25rem;display:flex;align-items:center;gap:.6rem;font-weight:800}}
.top img{{width:28px;height:28px;border-radius:7px}}
.top small{{margin-left:auto;font-weight:600;color:#9aa3b5;font-size:.78rem}}
.wrap{{max-width:64rem;margin:0 auto;padding:2rem 1.25rem 4rem}}
h1{{font-size:clamp(1.6rem,4.5vw,2.3rem);font-weight:900;letter-spacing:-.02em}}
h1 em{{font-style:normal;color:{O['accent2']}}}
.lead{{color:#aab2c3;margin-top:.6rem;font-size:.95rem}}
.flow{{list-style:none;padding:0;margin:1.6rem 0 0;display:flex;flex-wrap:wrap;gap:.45rem}}
.flow li{{background:{O['card']};border:1px solid {O['line']};border-radius:999px;padding:.38rem .85rem .38rem .4rem;font-size:.82rem;display:flex;align-items:center;gap:.45rem}}
.flow em{{font-style:normal;display:grid;place-items:center;width:1.45rem;height:1.45rem;border-radius:50%;background:{O['accent']};color:{O['ink']};font-weight:800;font-size:.75rem}}
.grp{{margin-top:2.2rem}}
.grp h2{{font-size:1rem;color:{O['accent2']};font-weight:800;margin-bottom:.8rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.8rem}}
.card{{display:flex;flex-direction:column;gap:.4rem;background:{O['card']};border:1px solid {O['line']};border-radius:14px;padding:1.05rem 1.1rem;transition:.2s}}
.card:hover{{border-color:{O['accent']};transform:translateY(-2px)}}
.card b{{font-size:1.02rem;display:flex;justify-content:space-between;gap:.5rem}}
.card b i{{font-style:normal;color:{O['accent']}}}
.card span{{font-size:.85rem;color:#b9c0cf}}
.card code{{margin-top:auto;font-size:.72rem;color:#7d879b;font-family:ui-monospace,Consolas,monospace;word-break:break-all}}
.box{{margin-top:2.2rem;background:{O['card']};border:1px solid {O['line']};border-radius:14px;padding:1.1rem 1.2rem}}
.box h2{{font-size:1rem;font-weight:800;margin-bottom:.6rem}}
.box p,.box li{{font-size:.88rem;color:#c3c9d6}}
.box ul{{margin:.3rem 0 0;padding-left:1.1rem}}
.st{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem;margin-top:.4rem}}
.st div{{border:1px solid {O['line']};border-radius:10px;padding:.65rem .8rem;font-size:.84rem}}
.st b{{display:block;margin-bottom:.15rem}}
.ok{{color:#5BE39B}}.no{{color:#FFB54A}}.wait{{color:#9aa3b5}}
.foot{{margin-top:2.5rem;font-size:.8rem;color:#7d879b;text-align:center}}
</style>
</head>
<body>
<header class="top"><div><img src="{LOGO_FILE}" alt="">{NAME} 업무 문서함<small>대표 전용 · 검색에 나오지 않는 페이지</small></div></header>
<main class="wrap">
  <h1>{NAME} <em>업무 문서함</em></h1>
  <p class="lead">견적부터 계약 · 일정 · 사진 · 명세서까지, 대표님이 쓰시는 화면을 한곳에 모았습니다. 이 주소는 즐겨찾기 해 두세요. 손님에게는 보내지 마세요.</p>
  <ol class="flow">{flow_html}</ol>
  {cards}
  <section class="box"><h2>서버 연결 상태</h2>
    <p>저장함 · 계약 · 일정 · 사진 올리기는 구글 서버를 씁니다. 빨간 표시가 있으면 큰길브리지에 알려 주세요.</p>
    <div class="st">
      <div><b>계약 · 저장함 · 일정 서버</b><span id="s-contract" class="wait">확인 중…</span></div>
      <div><b>사진 올리기 서버</b><span id="s-gallery" class="wait">확인 중…</span></div>
      <div><b>문의 알림</b><span class="ok">홈페이지 문의 · 견적 문의가 {EMAIL} 로 갑니다</span></div>
    </div>
  </section>
  <section class="box"><h2>암호 안내</h2>
    <ul>
      <li><b>보관함 암호</b> — 견적서 저장함 · 행사 일정을 엽니다. 대표님만 아시면 됩니다.</li>
      <li><b>직원 암호</b> — 행사 일정 · 체크리스트만 열립니다(견적 · 계약은 안 열림). 직원에게는 이것만 알려 주세요.</li>
      <li><b>사진 올리기 암호</b> — 사진 올리기 화면에서 씁니다.</li>
      <li>암호는 이 페이지 · 홈페이지 어디에도 적혀 있지 않습니다. 잊으셨으면 큰길브리지(1533-7295)로 연락 주세요. 카톡 · 메일로 암호를 주고받지 마세요.</li>
    </ul>
  </section>
  <section class="box"><h2>홈페이지 글 · 사진 고치기</h2>
    <p>홈페이지 주소 뒤에 <code>?edit=열쇠</code> 를 붙여 들어가면 글을 직접 고칠 수 있습니다(열쇠는 큰길브리지가 문자로 드린 것). 고친 뒤 「저장 파일 받기」로 보내 주시면 반영해 드립니다.</p>
  </section>
  <p class="foot">홈페이지 관리 · 큰길브리지 1533-7295 · www.ai-make.co.kr</p>
</main>
<script>
(function(){{
  var C = '{CONTRACT_URL}', G = '{GALLERY_URL}';
  function show(id, ok, msg){{ var el = document.getElementById(id); el.className = ok ? 'ok' : 'no'; el.textContent = msg; }}
  function ping(url, id, read){{
    if(!url){{ show(id, false, '아직 연결 전 — 서버 배포 대기'); return; }}
    var t = setTimeout(function(){{ show(id, false, '응답이 늦습니다 — 잠시 뒤 새로고침'); }}, 12000);
    fetch(url).then(function(r){{ return r.json(); }}).then(function(j){{ clearTimeout(t); read(j); }})
      .catch(function(){{ clearTimeout(t); show(id, false, '연결 안 됨 — 큰길브리지에 알려 주세요'); }});
  }}
  ping(C, 's-contract', function(j){{
    if(!j || !j.ok){{ show('s-contract', false, '응답 이상'); return; }}
    var m = ['연결됨'];
    m.push(j.box === 'ready' ? '저장함 암호 ✓' : '저장함 암호 미설정');
    if('sched' in j) m.push(j.sched === 'ready' ? '직원 암호 ✓' : '직원 암호 미설정');
    else m.push('일정 기능은 서버 새 버전 필요');
    show('s-contract', j.box === 'ready' && j.sched === 'ready', m.join(' · '));
  }});
  ping(G, 's-gallery', function(j){{ show('s-gallery', !!(j && j.ok), j && j.ok ? ('연결됨' + (j['설정완료'] === false ? ' · 설정 미완료' : '')) : '응답 이상'); }});
}})();
</script>
</body>
</html>
'''
    write('office.html', html)


if __name__ == '__main__':
    port('upload.html', upload_extra)
    port('quote.html', quote_extra)
    port('quote-catalog.js', catalog_extra)
    port('contract.html', contract_extra)
    port('statement.html', statement_extra)
    port('admin-lock.js')                  # 관리자 화면(?admin=1) 잠금 — 대표 암호(계약 서버 BOX_PW)
    port('schedule.html', schedule_extra)
    port_servers()
    office()
    import admin_gate                      # 관리자 모드 잠금 화면 (대표 암호 = 계약 서버 BOX_PW)
    admin_gate.apply(os.path.join(SITE, 'office.html'), ID, NAME, CONTRACT_URL, OFFICE)
