/**
 * F&J 이벤트 블로그 — _blog/posts/*.json 을 홈페이지 글로 만든다
 * ──────────────────────────────────────────────────────────
 *   /blog/               글 목록 (최신순, 24개씩 → /blog/page/2/)
 *   /blog/<지역>/        지역별 모음 (예: /blog/ansan/)
 *   /blog/<글주소>/      글 하나
 *   /rss.xml             블로그 RSS
 *   sitemap.xml · llms.txt 의 블로그 부분도 같이 갱신한다
 *
 * 원본은 _blog/ 에 둔다. 밑줄로 시작하는 폴더는 GitHub Pages(Jekyll)가 공개하지 않는다.
 * blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (HD기획 scripts/build-blog.mjs 를 F&J 이벤트에 맞게 옮긴 것)
 *
 * 이 사이트는 주소 앞에 경로가 붙을 수 있다(brizymedia.github.io/fj-event/ → 나중에 도메인). 그래서 사이트 안 링크는
 * 모두 상대 경로로 만든다. 절대 주소(canonical · og · JSON-LD · sitemap)의 기준은 tools/build_site.py 의 BASE 이다.
 *
 * 순서:  python tools/build_site.py  →  python tools/blog_shell.py  →  node scripts/build-blog.mjs
 *        (build_site.py 가 sitemap.xml · llms.txt 를 덮어쓰므로 블로그 빌드는 항상 그 뒤에)
 * 글 형식 · 규칙: _blog/GUIDE.md   ·   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const 쪽당 = 24;

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 사이트 안 주소(/로 시작)를 현재 쪽 깊이에 맞춘 상대 주소로. 한글 글 주소는 퍼센트 인코딩. */
export function 상대(u, 위) {
  const m = String(u).match(/^([^?#]*)([?#].*)?$/);
  const 경로 = m[1], 꼬리 = m[2] || '';
  const 조각 = 경로.replace(/^\//, '').split('/').map((s) => encodeURIComponent(decodeURIComponent(s))).join('/');
  return (위 + 조각 || './') + 꼬리;
}

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다. */
export function 인라인(글, 위 = '') {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${상대(u, 위)}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
}
export const 글자만 = (글) => String(글 ?? '').replace(/\*\*(.+?)\*\*/g, '$1').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
export const 날짜글 = (d) => { const m = String(d || '').match(/^(\d{4})-(\d{2})-(\d{2})$/); return m ? `${m[1]}년 ${+m[2]}월 ${+m[3]}일` : String(d || ''); };
export const 글주소 = (slug) => `/blog/${encodeURIComponent(slug)}/`;

export function 껍데기(ROOT) {
  const f = resolve(ROOT, '_blog', 'shell.json');
  if (!existsSync(f)) throw new Error('_blog/shell.json 이 없다 — 먼저 python tools/blog_shell.py');
  return JSON.parse(readFileSync(f, 'utf8'));
}

export function 지역표(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'regions.json'), 'utf8'));
  const 표 = new Map(j.지역.map((r) => [r.slug, r]));
  표.set('common', { slug: 'common', 이름: '경기 남부 공통', 도: '경기도', 시군: '경기 남부', 서비스페이지: '', 이동: '', 비중: 0 });
  return 표;
}

/** photos.json 의 묶음을 사진 한 장씩 풀어 경로 → 정보 로 */
export function 사진목록(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'photos.json'), 'utf8'));
  const 표 = new Map();
  j.묶음.forEach((g, i) => { (g.path || []).forEach((p) => 표.set(p, { ...g, path: p, 묶음번호: i })); });
  return 표;
}

export function 글읽기(ROOT) {
  const 폴더 = resolve(ROOT, '_blog', 'posts');
  if (!existsSync(폴더)) return [];
  return readdirSync(폴더).filter((f) => f.endsWith('.json')).map((f) => {
    const p = JSON.parse(readFileSync(resolve(폴더, f), 'utf8'));
    Object.defineProperty(p, '_파일', { value: f, enumerable: false });
    return p;
  }).sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : a.slug < b.slug ? -1 : 1));
}

/** 본문 글자 — 읽는 시간·검사·중복 비교에 쓴다 */
export function 본문글(p) {
  const 조각 = [p.lead, ...(p.points || [])];
  for (const s of p.sections || []) {
    조각.push(s.h2);
    for (const b of s.blocks || []) {
      if (b.p) 조각.push(b.p);
      if (b.tip) 조각.push(b.tip);
      if (b.ul) 조각.push(...b.ul);
      if (b.ol) 조각.push(...b.ol);
      if (b.table) 조각.push(...(b.table.head || []), ...(b.table.rows || []).flat());
    }
  }
  for (const f of p.faq || []) 조각.push(f.q, f.a);
  return 조각.map(글자만).join('\n');
}

export function 글이미지들(p) {
  const 목록 = p.cover ? [p.cover] : [];
  for (const s of p.sections || []) for (const b of s.blocks || []) if (b.img) 목록.push(b.img);
  return 목록;
}

export function buildBlog(옵션 = {}) {
  const ROOT = 옵션.ROOT;
  const 셸 = 껍데기(ROOT);
  const SITE = 셸.base.replace(/\/$/, '');
  const BRAND = 셸.name;
  const TEL = 셸.tel;
  const 색인 = !셸.noindex;
  const 사진주소 = (path) => SITE + String(path).split('/').map(encodeURIComponent).join('/');   // 절대 주소(og · JSON-LD 용)
  const 지역 = 지역표(ROOT);
  const posts = 글읽기(ROOT);
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;
  /* 머리 · 꼬리(build_site.py 에서 가져온 것)의 상대 주소를 이 쪽 깊이에 맞춘다 */
  const 깊이맞춤 = (html, 위) => html.replace(/(href|src)="(?!https?:|tel:|mailto:|sms:|#|\/)([^"]*)"/g, (m, a, v) => `${a}="${위}${v}"`);

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => {
    const d = resolve(ROOT, 폴더);
    mkdirSync(d, { recursive: true });
    writeFileSync(resolve(d, 'index.html'), html, 'utf8');
  };

  const 머리 = ({ 제목, 설명, 경로, 이미지, 종류 = 'website', 더넣기 = '', 위, 색인허용 = true }) => `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(제목)}</title>
<meta name="description" content="${esc(설명)}">
<meta name="robots" content="${색인 && 색인허용 ? 'index,follow,max-image-preview:large' : 'noindex,nofollow'}">
<meta name="theme-color" content="#FFFBF0">
<link rel="canonical" href="${SITE}${경로}">
<link rel="icon" type="image/svg+xml" href="${위}assets/img/favicon.svg">
<link rel="alternate" type="application/rss+xml" title="${BRAND} 행사 준비 블로그" href="${위}rss.xml">
<meta property="og:type" content="${종류}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="${BRAND}">
<meta property="og:title" content="${esc(제목)}"><meta property="og:description" content="${esc(설명)}"><meta property="og:url" content="${SITE}${경로}"><meta property="og:image" content="${esc(이미지)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&family=Gothic+A1:wght@400;500;700;800&display=swap">
<link rel="stylesheet" href="${위}assets/style.css?v=${셸.ver}">
<link rel="stylesheet" href="${위}assets/blog.css?v=${셸.ver}">
${더넣기}
</head>
<body>
${깊이맞춤(셸.header, 위)}
<main id="main">`;

  const 꼬리 = (위) => `</main>
${깊이맞춤(셸.footer, 위)}
</body>
</html>
`;

  const 상담 = (위) => `<aside class="bcta">
    <div><h3>행사 날짜가 정해지셨나요?</h3><p>날짜 · 장소 · 인원만 알려 주세요. 구성과 비용을 정리해 드립니다.</p></div>
    <div class="bcta-r"><a class="num" href="tel:${셸.telRaw}">${TEL}</a><div class="btns"><a class="btn sun sm" href="${위}contact.html#form">견적 문의하기</a><a class="btn white sm" href="sms:${셸.telRaw}">문자로 문의</a></div></div>
  </aside>`;

  const 카드 = (p, 위) => {
    const r = 지역.get(p.region);
    return `<a class="bcard" href="${상대(글주소(p.slug), 위)}">
      <img src="${위}${esc(p.cover.path.replace(/^\//, ''))}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="560">
      <div class="in"><div class="r">${esc(r ? r.이름 : '')} · ${esc(날짜글(p.date))}</div><div class="t">${esc(p.title)}</div><div class="s">${esc(p.description)}</div></div>
    </a>`;
  };

  const 개수 = new Map();
  posts.forEach((p) => 개수.set(p.region, (개수.get(p.region) || 0) + 1));
  const 칩 = (현재, 위) => `<nav class="bchips" aria-label="지역별 글">
    <a href="${위}blog/"${현재 === '' ? ' aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${[...지역.values()].filter((r) => 개수.get(r.slug)).map((r) =>
      `<a href="${위}blog/${r.slug}/"${현재 === r.slug ? ' aria-current="page"' : ''}>${esc(r.이름)}<small>${개수.get(r.slug)}</small></a>`).join('\n    ')}
  </nav>`;

  /* ── 글 페이지 ── */
  const 이미지html = (im, 표지, 위) => `<figure class="bfig${표지 ? ' cover' : ''}">
    <img src="${위}${esc(im.path.replace(/^\//, ''))}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="${표지 ? 1200 : 960}" height="${표지 ? 675 : 720}">
    <figcaption>${인라인(im.caption, 위)}</figcaption>
  </figure>`;
  const 블록 = (b, 위) => {
    if (b.p) return `<p>${인라인(b.p, 위)}</p>`;
    if (b.tip) return `<div class="btip">${인라인(b.tip, 위)}</div>`;
    if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x, 위)}</li>`).join('')}</ul>`;
    if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x, 위)}</li>`).join('')}</ol>`;
    if (b.table) return `<div class="btbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h, 위)}</th>`).join('')}</tr></thead><tbody>${
      b.table.rows.map((row) => `<tr>${row.map((c) => `<td>${인라인(c, 위)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    if (b.img) return 이미지html(b.img, false, 위);
    return '';
  };

  const 위글 = '../../';   // /blog/<글>/ · /blog/<지역>/ · /blog/page/N/
  for (const p of posts) {
    const 위 = 위글;
    const r = 지역.get(p.region) || { 이름: '', 서비스페이지: '' };
    const 지역글 = p.region !== 'common';
    const 경로 = 글주소(p.slug);
    const 분 = Math.max(1, Math.round(본문글(p).length / 500));
    const 관련 = [...posts.filter((o) => o !== p && o.region === p.region),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic === p.topic),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic !== p.topic)].slice(0, 3);

    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: (지역글 ? r.이름 : '경기 남부 공통') + ' 행사 준비', item: `${SITE}/blog/${p.region}/` },
        { '@type': 'ListItem', position: 4, name: p.title, item: SITE + 경로 } ] },
      { '@type': 'BlogPosting', '@id': SITE + 경로, headline: p.title, description: p.description,
        image: 글이미지들(p).map((im) => 사진주소(im.path)),
        datePublished: p.date, dateModified: p.updated || p.date, inLanguage: 'ko',
        keywords: [p.keyword.main, ...(p.keyword.sub || [])].join(', '),
        author: { '@type': 'Organization', name: BRAND, url: SITE + '/' },
        publisher: { '@id': SITE + '/#business' },
        mainEntityOfPage: { '@type': 'WebPage', '@id': SITE + 경로 },
        ...(지역글 ? { spatialCoverage: { '@type': 'Place', name: `${r.도} ${r.시군}` } } : {}) },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };

    const html = 머리({ 제목: `${p.title} | ${BRAND}`, 설명: p.description, 경로, 이미지: 사진주소(p.cover.path), 종류: 'article', 위,
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}` }) + `
<div class="bcrumb"><a href="${위}">홈</a> › <a href="${위}blog/">블로그</a> › <a href="${위}blog/${p.region}/">${esc(r.이름)}</a></div>
<article class="bart">
  <p class="beyebrow">${esc(지역글 ? r.이름 + ' 행사 준비' : '경기 남부 행사 준비')} · ${esc(날짜글(p.date))}</p>
  <h1>${esc(p.title)}</h1>
  <div class="bmeta"><a href="${위}blog/${p.region}/">${esc(r.이름)} 글 모음</a><span>읽는 시간 약 ${분}분</span></div>
  <p class="blead">${인라인(p.lead, 위)}</p>
  ${이미지html(p.cover, true, 위)}
  <div class="bpoints"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x, 위)}</li>`).join('')}</ul></div>
  <nav class="btoc" aria-label="목차"><b>목차</b><ol>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ol></nav>
  <div class="bbody">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map((b) => 블록(b, 위)).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="bfaq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a, 위)}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="bsrc"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
  ${상담(위)}
</article>
${관련.length ? `<section class="bmore"><h2>같이 보면 좋은 글</h2><div class="bcards">${관련.map((o) => 카드(o, 위)).join('\n')}</div></section>` : ''}
` + 꼬리(위);
    쓰기(`blog/${p.slug}`, html);
  }

  /* ── 목록 (/blog/, /blog/page/N/) ── */
  const 대표이미지 = posts[0] ? 사진주소(posts[0].cover.path) : 셸.og;
  const 쪽수 = Math.max(1, Math.ceil(posts.length / 쪽당));
  for (let n = 1; n <= 쪽수; n++) {
    const 위 = n === 1 ? '../' : '../../../';
    const 조각 = posts.slice((n - 1) * 쪽당, n * 쪽당);
    const 경로 = n === 1 ? '/blog/' : `/blog/page/${n}/`;
    const 쪽나눔 = 쪽수 > 1 ? `<nav class="bpager" aria-label="쪽 이동">${Array.from({ length: 쪽수 }, (_, i) => i + 1).map((k) =>
      k === n ? `<span aria-current="page">${k}</span>` : `<a href="${위}blog/${k === 1 ? '' : `page/${k}/`}">${k}</a>`).join('')}</nav>` : '';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' } ] },
      { '@type': 'Blog', '@id': SITE + '/blog/', name: `${BRAND} 행사 준비 블로그`, inLanguage: 'ko', publisher: { '@id': SITE + '/#business' },
        blogPost: 조각.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date, image: 사진주소(p.cover.path) })) } ] };
    const html = 머리({
      제목: n === 1 ? `행사 준비 블로그 — 운동회 · 에어바운스 · 물놀이 · 유아체육 | ${BRAND}` : `행사 준비 블로그 ${n}쪽 | ${BRAND}`,
      설명: '어린이집 · 유치원 · 초등학교 운동회와 체육대회, 에어바운스, 워터슬라이드와 수영장, 체험놀이, 발표회, 송년회를 준비하는 담당자를 위한 글. 경기 남부 현장 기준으로 정리합니다.',
      경로, 이미지: 대표이미지, 더넣기: 제이슨(ld), 위 }) + `
<div class="bcrumb wide"><a href="${위}">홈</a> › 블로그${n > 1 ? ` › ${n}쪽` : ''}</div>
<div class="bwrap">
  <p class="beyebrow">Blog · Event Guide</p>
  <h1>행사 준비 블로그</h1>
  <p class="blead" style="max-width:760px">운동회, 에어바운스, 물놀이, 체험놀이, 발표회를 맡은 원장님 · 선생님 · 담당자가 먼저 확인할 것들을 현장 기준으로 정리합니다.</p>
  ${칩('', 위)}
  ${posts.length ? `<div class="bcards">${조각.map((p) => 카드(p, 위)).join('\n')}</div>` : '<div class="bempty">첫 글을 준비하고 있습니다.</div>'}
  ${쪽나눔}
  ${상담(위)}
</div>
` + 꼬리(위);
    쓰기(n === 1 ? 'blog' : `blog/page/${n}`, html);
  }

  /* ── 지역 모음 (/blog/<지역>/) ── */
  const 허브 = [];
  for (const r of 지역.values()) {
    const 목록 = posts.filter((p) => p.region === r.slug);
    if (!목록.length) continue;            // 글이 없는 지역은 모음 페이지를 만들지 않는다
    const 위 = 위글;
    const 경로 = `/blog/${r.slug}/`;
    const 허브제목 = r.slug === 'common' ? '경기 남부 행사 준비 공통 정보' : `${r.이름} 행사 준비 정보`;
    const 소개 = r.slug === 'common'
      ? '지역과 상관없이 행사 준비에 두루 쓰이는 글입니다.'
      : `${esc(r.이름)}에서 행사를 준비하는 담당자를 위한 글입니다. ${esc(r.이동)}.`;
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: 허브제목, item: SITE + 경로 } ] },
      { '@type': 'CollectionPage', '@id': SITE + 경로, name: 허브제목, inLanguage: 'ko',
        hasPart: 목록.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug) })) } ] };
    const html = 머리({
      제목: `${허브제목} — 운동회 · 에어바운스 · 물놀이 | ${BRAND}`,
      설명: r.slug === 'common' ? '지역과 상관없이 행사 준비에 두루 필요한 내용. 어린이날 · 유아체육 · 발표회 · 송년회 준비를 현장 기준으로 정리한 글 모음입니다.' : `${r.이름}에서 행사를 준비할 때 확인할 것들. 운동회 · 에어바운스 · 물놀이 · 체험놀이 준비를 현장 기준으로 정리한 글 모음입니다.`,
      경로, 이미지: 사진주소(목록[0].cover.path), 더넣기: 제이슨(ld), 위 }) + `
<div class="bcrumb wide"><a href="${위}">홈</a> › <a href="${위}blog/">블로그</a> › ${esc(r.이름)}</div>
<div class="bwrap">
  <p class="beyebrow">${r.slug === 'common' ? 'Guide' : esc(`${r.도} ${r.시군}`)}</p>
  <h1>${esc(허브제목)}</h1>
  <p class="blead" style="max-width:760px">${소개}</p>
  ${칩(r.slug, 위)}
  <div class="bcards">${목록.map((p) => 카드(p, 위)).join('\n')}</div>
  ${상담(위)}
</div>
` + 꼬리(위);
    쓰기(`blog/${r.slug}`, html);
    허브.push({ loc: 경로, lastmod: 목록[0].updated || 목록[0].date });
  }

  /* ── sitemap.xml — 기존 항목은 두고 /blog/ 부분만 바꾼다 ── */
  const 블로그주소 = posts.length ? [
    { loc: '/blog/', lastmod: posts[0].updated || posts[0].date },
    ...허브,
    ...posts.map((p) => ({ loc: 글주소(p.slug), lastmod: p.updated || p.date })),
  ] : [];
  const sm = resolve(ROOT, 'sitemap.xml');
  if (existsSync(sm)) {
    let xml = readFileSync(sm, 'utf8');
    xml = xml.replace(/\s*<url><loc>[^<]*\/blog\/[^<]*<\/loc>[^]*?<\/url>/g, '');
    const 추가 = 블로그주소.map((u) => `  <url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>\n`).join('');
    xml = xml.replace(/<\/urlset>\s*$/, 추가 + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 정보)\n- [행사 준비 블로그](${SITE}/blog/): 운동회 · 에어바운스 · 물놀이 · 유아체육 · 체험놀이 준비 체크리스트\n` +
      posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    /* 「## 블로그」부터 다음 「## 」 절 앞(없으면 끝)까지 바꾼다 */
    const 시작 = t.search(/^## 블로그/m);
    if (시작 < 0) t = t.trimEnd() + '\n\n' + 절;
    else {
      const 뒤 = t.slice(시작 + 1);
      const 다음 = 뒤.search(/^## /m);
      t = t.slice(0, 시작) + 절 + (다음 >= 0 ? '\n' + 뒤.slice(다음) : '');
    }
    writeFileSync(ll, t, 'utf8');
  }

  /* ── rss.xml ── */
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>${esc(BRAND)} 행사 준비 블로그</title><link>${SITE}/blog/</link><description>운동회 · 에어바운스 · 물놀이 · 유아체육을 준비하는 담당자를 위한 글</description><language>ko</language>
${posts.slice(0, 50).map((p) => `<item><title>${esc(p.title)}</title><link>${SITE}${글주소(p.slug)}</link><guid>${SITE}${글주소(p.slug)}</guid><description>${esc(p.description)}</description><pubDate>${new Date(p.date + 'T09:00:00+09:00').toUTCString()}</pubDate></item>`).join('\n')}
</channel></rss>
`;
  writeFileSync(resolve(ROOT, 'rss.xml'), rss, 'utf8');

  return { posts, 블로그주소 };
}

/* 혼자 실행할 때 */
const 이파일 = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(process.argv[1]) === 이파일) {
  const ROOT = resolve(dirname(이파일), '..');
  const { posts, 블로그주소 } = buildBlog({ ROOT });
  console.log(`blog/: 글 ${posts.length}개 · sitemap 항목 ${블로그주소.length}개 · rss.xml · llms.txt 갱신`);
}
