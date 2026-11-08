/*
 * F&J 이벤트 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
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
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0, 총액: +s.t || 0, 부가세: s.x === 'p' ? '포함' : '별도' };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}
