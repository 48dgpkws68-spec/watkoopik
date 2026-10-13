(function(){
  var b=document.getElementById('burger'),m=document.getElementById('mobileMenu');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);});}

  // zoeken in alle gidsen (index staat in search.json)
  var idx=null;
  function load(cb){if(idx)return cb(idx);fetch((window.ROOT||'')+'search.json').then(function(r){return r.json()}).then(function(j){idx=j;cb(j)}).catch(function(){});}
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
  document.querySelectorAll('[data-search]').forEach(function(inp){
    var box=inp.closest('.search-wrap').querySelector('.search-results');
    inp.addEventListener('input',function(){
      var q=norm(inp.value.trim());
      if(q.length<2){box.classList.remove('show');box.innerHTML='';return;}
      load(function(list){
        var hits=list.filter(function(it){return norm(it.t+' '+it.k).indexOf(q)>-1}).slice(0,8);
        box.innerHTML=hits.length?hits.map(function(h){return '<a href="'+(window.ROOT||'')+h.u+'">'+h.t+'<br><small>'+h.c+'</small></a>'}).join(''):'<a href="'+(window.ROOT||'')+'gidsen.html">Geen directe match. Bekijk alle gidsen</a>';
        box.classList.add('show');
      });
    });
    inp.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=box.querySelector('a');if(a)location.href=a.href;}});
    document.addEventListener('click',function(e){if(!inp.closest('.search-wrap').contains(e.target))box.classList.remove('show');});
  });

  // sticky mobiele koopknop op gidspagina's
  var s=document.getElementById('stickyCta');
  if(s){document.body.classList.add('has-sticky');
    var w=document.querySelector('.winners');
    function chk(){var r=w?w.getBoundingClientRect():null;s.classList.toggle('on',r?r.bottom<0:window.scrollY>600);}
    window.addEventListener('scroll',chk,{passive:true});chk();}

  // uitgaande klikken meten (later analytics)
  document.addEventListener('click',function(e){var a=e.target.closest('a[data-shop]');if(!a)return;try{var k='wk_clicks';var n=parseInt(localStorage.getItem(k)||'0',10)+1;localStorage.setItem(k,String(n));}catch(_){}});
})();
