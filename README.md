# F&J 이벤트(펀앤조이 체육교실) 홈페이지

큰길브리지 계약 KB-20260923-321 (회사형 · 1,100,000원, 2026-11-02 서명). 제작 자료 제출서(2026-11-05)를 그대로 옮겼다.
오픈 희망일 2026-11-20 · 희망 도메인 「F&J EVENT.co.kr」(미정).

## 보기 / 고치기
```
python -m http.server 8821 --directory C:/Users/gilau/Documents/fj-event
python tools/build_site.py      # 페이지 · sitemap · robots · llms.txt 를 다시 만든다
```
글 · 연락처 · 메뉴 · 영상은 `tools/build_site.py` 맨 위에서 고친다. 공지는 `assets/data/notices.json`.
**사진**: `assets/img/p/<코드>.webp` 로 넣고 다시 빌드하면 자리표가 사진으로 바뀐다. 코드: hero · arch · bounce · water · rec · stage (`PHOTOS`).

## 납품 전에 확인할 것 (최원창 대표)
1. **사진 · 로고** — 카톡으로 보내겠다고 한 것(10~30장, 로고 AI/PNG/JPG)이 아직 없다. 지금은 색 자리표 + 임시 글자 로고(`assets/img/logo.svg`). 받으면 교체(색은 「로고색」으로 요청받음 → 지금 노랑/파랑/산호는 임시).
2. **가격** — 제출서의 「음향 · 조명 100~」 등을 **만 원 단위**로 보고 「100만 원~」으로 적었다. 단위가 맞는지 확인.
3. **카카오톡 채널 주소** — 문의 방법에 있었지만 주소가 없다. `KAKAO` 에 넣으면 단추가 생긴다(지금은 문자 상담).
4. **문의 폼** — 서버 연결 전에는 문자 앱으로 내용이 넘어간다. 문의 서버 배포 뒤 `FORM_ENDPOINT` 에 주소.
5. **후기** — 받은 후기가 없어 만들지 않았다(실적 숫자 3개만: 운동회 연 100회 · 물놀이 연 50회 · 경기도교육청 행사).
6. **영상 4개** — 대표 유튜브(@FJEVENT)에서 골랐다(삽입 재생).
7. 오픈 전: `NOINDEX=False`, `BASE` 를 도메인으로, `og.png`(1200×630) 추가.

## 업무 도구 · 사장님 수정 모드 (회사형 계약, 2026-11-08 이식)
```
python tools/port_docs.py     # 큰길이벤트 원본(~/Documents/클로드코드)에서 업무 도구를 이 회사용으로 다시 옮긴다
```
- 옮긴 것: `quote.html`(+`quote-catalog.js` 견적 품목 · 가격은 전부 비워 둠) · `contract.html` · `statement.html` · `schedule.html` · `upload.html` · `office.html`(대표 전용 업무 문서함 · 바닥글 「관리자 모드」로 들어감) · `admin-lock.js` · `apps-script/contract` · `apps-script/gallery`(+공지 액션). `notice-admin.html` 은 `build_site.py` 가 만든다.
- 회사 설정(상호 · 사업자번호 · 연락처 · 색 · 견적 품목)은 `tools/port_docs.py` 맨 위. **결과 HTML 은 손으로 고치지 말고** 거기서 고친 뒤 다시 실행.
- **사장님 직접 수정 모드**: `?edit=열쇠` (`assets/edit.js`, `tools/apply_edits.py` 로 반영). 레포에는 열쇠의 sha256(`build_site.py` 의 `EDIT_HASH`)만 있고, 열쇠 · 대표 암호는 큰길브리지 PC `Desktop\큰길브리지\FJ-수정모드-열쇠.txt` 에만 있다. apply_edits 로 반영한 뒤 build_site.py 를 다시 돌리면 그 수정이 덮어써지니 주의.
- **서버 배포 전**이라 `port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL` 이 비어 있다. 배포(형님 구글 계정) 뒤 `/exec` 주소를 넣고 `port_docs.py` → `build_site.py` 순서로 다시 실행. 배포할 때 계약 서버 스크립트 속성 `BOX_PW` 에 txt 의 대표 암호를 넣어야 관리자 모드가 열린다.
- 대표 직인 PNG 를 `assets/img/stamp-fj.png` 로 넣으면 견적서 · 계약서 · 명세서에 찍힌다(없으면 「(인)」).
- 공지: 서버 연결 전에는 `assets/data/notices.json`, 연결 뒤에는 `notice-admin.html`(photos 가지 `photos/notices.json` 에 쌓이고 공지 페이지가 앞에 붙여 보여 줌 — 레포에 photos 고아 가지를 같이 만들 것).

## 행사 준비 블로그 (/blog/ · 2026-11-08 첫 10편)
```
python tools/build_site.py          # ① 페이지 · sitemap · llms.txt 를 만든다 (블로그 항목을 덮어쓴다)
python tools/blog_shell.py          # ② build_site.py 의 머리 · 꼬리를 _blog/shell.json 으로 옮긴다
node scripts/build-blog.mjs         # ③ /blog/ · rss.xml 을 만들고 sitemap.xml · llms.txt 에 블로그 항목을 이어 붙인다
node scripts/blog-check.mjs         # 글 검사 (새 글은 --new _blog/posts/<파일>)
```
- **실행 순서는 반드시 build_site.py → blog_shell.py → build-blog.mjs.** build_site.py 가 sitemap.xml · llms.txt 를 덮어쓰기 때문이다. 주소 기준(`BASE`) · noindex 여부도 build_site.py 에서 읽는다.
- 글 규칙 · 사용할 수 있는 회사 사실: `_blog/GUIDE.md`. 지역 자료 `regions.json` · 사진 `photos.json` · 출처 `sources.json` · 글 `posts/*.json`. `blog/` 는 매번 지우고 다시 만드니 손으로 고치지 않는다.
- 머리 메뉴에 「블로그」 링크는 아직 없다(build_site.py 의 NAV 에 넣을 것). 블로그 글에는 가격 · 후기 · 학교 이름을 쓰지 않았다(검사기가 막는다).
