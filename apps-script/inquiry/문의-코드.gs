/**
 * F&J 이벤트(펀앤조이 체육교실) — 홈페이지 견적 문의 접수 서버      버전 2026-11-08a
 *
 * 하는 일
 *   1) 홈페이지 문의 폼(contact.html)이 보낸 내용을 구글 시트에 한 줄로 쌓는다
 *   2) 알림 메일을 보낸다 (받는 사람은 스크립트 속성 NOTIFY_TO, 쉼표로 여러 명)
 *   3) 스팸 막기: 숨은 칸(website)이 차 있으면 버리고, 같은 번호는 10분에 3번까지만 받는다
 *
 * 배포 방법 (형님 구글 계정이 필요해서 직접 하셔야 합니다)
 *   1. script.google.com → 새 프로젝트 → 이 코드를 통째로 붙여넣기 → 프로젝트 이름 「FJ-문의」
 *   2. 왼쪽 톱니(프로젝트 설정) → 스크립트 속성 추가
 *        SHEET_ID  : 접수를 쌓을 구글 시트 주소의 가운데 긴 문자열 (빈 시트 하나 만들어서)
 *        NOTIFY_TO : 알림 받을 메일. 예) cwc9982@naver.com,gilauto325@gmail.com
 *   3. 편집기에서 함수 「시험」을 한 번 실행(권한 허용) → 시트에 줄이 생기고 메일이 오면 정상
 *   4. 배포 → 새 배포 → 유형 「웹 앱」 → 실행 사용자 「나」, 액세스 권한 【모든 사용자】
 *      (「Google 계정이 있는 모든 사용자」는 403 납니다)
 *   5. /exec 로 끝나는 주소를 클대리에게 직접 알려 주세요 (카톡·메일 말고) → 사이트의 FORM_ENDPOINT 에 넣습니다
 *   6. 코드를 고쳤다면 「새 배포」가 아니라 배포 관리 → 연필 → 버전 「새 버전」 (주소가 안 바뀝니다)
 */

var 버전 = '2026-11-08a';
var 시트이름 = '문의';

function doPost(e) {
  try {
    var 내용 = JSON.parse(e.postData.contents);
    if (내용.website) return 응답({ ok: true });            // 숨은 칸이 차 있으면 사람이 아님 — 조용히 버림
    if (!내용.name || !내용.phone) return 응답({ ok: false, error: '이름과 연락처가 필요합니다' });
    if (!횟수확인(내용.phone)) return 응답({ ok: false, error: '잠시 뒤에 다시 보내 주세요' });
    var 결과 = { ok: true, saved: 저장(내용), mailed: 알림(내용) };
    // 시트도 메일도 못 했으면 조용히 성공으로 두지 않는다 (속성이 비어 있는 경우)
    if (!결과.saved && !결과.mailed) return 응답({ ok: false, error: '서버 설정이 끝나지 않았습니다 (SHEET_ID · NOTIFY_TO)' });
    return 응답(결과);
  } catch (err) {
    console.error(err);
    return 응답({ ok: false, error: String(err) });
  }
}

/** 브라우저에서 주소를 바로 열었을 때 (살아있는지 확인용) */
function doGet() {
  var p = PropertiesService.getScriptProperties();
  return 응답({ ok: true, service: 'fj-inquiry', version: 버전, sheet: !!p.getProperty('SHEET_ID'), mail: !!p.getProperty('NOTIFY_TO') });
}

function 응답(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function 횟수확인(phone) {
  var 캐시 = CacheService.getScriptCache();
  var 키 = 'n' + String(phone).replace(/\D/g, '');
  var n = Number(캐시.get(키) || 0);
  if (n >= 3) return false;
  캐시.put(키, String(n + 1), 600);
  return true;
}

function 저장(내용) {
  var id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  if (!id) return false;
  var ss = SpreadsheetApp.openById(id);
  var sh = ss.getSheetByName(시트이름);
  if (!sh) {
    sh = ss.insertSheet(시트이름);
    sh.appendRow(['접수시각', '성함·기관', '연락처', '이메일', '서비스', '문의 내용', '페이지']);
    sh.setFrozenRows(1);
  }
  sh.appendRow([new Date(), 내용.name || '', "'" + (내용.phone || ''), 내용.email || '', 내용.service || '', 내용.message || '', 내용.page || '']);
  return true;
}

function 알림(내용) {
  var to = PropertiesService.getScriptProperties().getProperty('NOTIFY_TO');
  if (!to) return false;
  var 본문 = '홈페이지로 견적 문의가 들어왔습니다.\n\n' +
    '성함·기관 : ' + (내용.name || '') + '\n' +
    '연락처 : ' + (내용.phone || '') + '\n' +
    '서비스 : ' + (내용.service || '') + '\n\n' +
    (내용.message || '') + '\n\n' +
    '접수 시각 : ' + Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm');
  MailApp.sendEmail({ to: to, subject: '[F&J 홈페이지 문의] ' + (내용.name || '이름 없음'), body: 본문 });
  return true;
}

/** 배포 전에 한 번 실행해 보세요 — 시트에 줄이 생기고 NOTIFY_TO 로 메일이 오면 정상 */
function 시험() {
  var 샘플 = { name: '[시험] 홍길동', phone: '010-0000-0000', service: '에어바운스', message: '[시험] 접수 시험입니다.', page: 'test' };
  Logger.log('저장=' + 저장(샘플) + ' 메일=' + 알림(샘플));
}
