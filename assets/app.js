(function(){
'use strict';
var d=document;
// 메뉴
var mb=d.querySelector('.mbtn'),sh=d.getElementById('sheet');
if(mb&&sh){mb.addEventListener('click',function(){var on=sh.classList.toggle('on');mb.setAttribute('aria-expanded',on);d.body.style.overflow=on?'hidden':'';});
sh.addEventListener('click',function(e){if(e.target.closest('a')){sh.classList.remove('on');mb.setAttribute('aria-expanded',false);d.body.style.overflow='';}});}
// 등장 — IntersectionObserver 가 안 오는 화면에서도 보이게 스크롤 검사 병행
var rv=[].slice.call(d.querySelectorAll('.rv'));
function chk(){var h=innerHeight;rv=rv.filter(function(el){var r=el.getBoundingClientRect();if(r.top<h*0.94&&r.bottom>0){el.classList.add('in');return false;}return true;});}
chk();addEventListener('scroll',chk,{passive:true});addEventListener('resize',chk);setTimeout(chk,300);
// 유튜브: 누르면 그 자리에서 재생 (개인정보 보호 도메인)
d.addEventListener('click',function(e){var b=e.target.closest('[data-yt]');if(!b)return;
var f=d.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='영상 재생';
b.innerHTML='';b.appendChild(f);b.removeAttribute('data-yt');});
// 견적 문의 폼
var fm=d.getElementById('form');
if(fm){
var q=new URLSearchParams(location.search).get('s');if(q&&fm.service){[].some.call(fm.service.options,function(o){if(o.value===q){fm.service.value=q;return true;}});}
var msg=fm.querySelector('.fmsg');
function say(t,c){msg.textContent=t;msg.className='fmsg '+(c||'');}
fm.addEventListener('submit',function(e){
e.preventDefault();
if(fm.website.value)return;
if(!fm.name.value.trim()||!fm.phone.value.trim()){say('성함과 연락처를 적어 주세요.','err');return;}
if(!/[0-9]{9,}/.test(fm.phone.value.replace(/\D/g,''))){say('연락처를 다시 확인해 주세요.','err');return;}
if(!fm.agree.checked){say('개인정보 이용 동의에 체크해 주세요.','err');return;}
var svc=fm.service.options[fm.service.selectedIndex].text;
var text='[F&J 이벤트 견적 문의]\n성함/기관: '+fm.name.value+'\n연락처: '+fm.phone.value+'\n서비스: '+svc+'\n날짜: '+(fm.date.value||'미정')+'\n인원: '+(fm.people.value||'-')+'\n장소: '+(fm.place.value||'-')+'\n내용: '+(fm.msg.value||'-');
var ep=fm.getAttribute('data-endpoint');
if(ep){
say('보내는 중입니다…');
fetch(ep,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({name:fm.name.value,phone:fm.phone.value,email:'',service:'홈페이지 견적 문의 · '+svc,message:text,page:location.href,website:fm.website.value})})
.then(function(r){return r.json();}).then(function(j){if(j&&j.ok){say('문의가 접수되었습니다. 곧 연락드리겠습니다.','ok');fm.reset();}else throw 0;})
.catch(function(){say('전송에 실패했습니다. 전화 '+fm.getAttribute('data-tel')+' 로 연락 주세요.','err');});
}else{
// 서버가 연결되기 전: 문자 앱으로 내용을 넘긴다
say('문자 앱이 열립니다. 내용을 확인하고 보내 주세요.','ok');
location.href='sms:'+fm.getAttribute('data-tel')+'?body='+encodeURIComponent(text);
}
});
}
})();
