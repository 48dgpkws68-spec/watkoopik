/* watkoopik pro · beweging (GSAP + ScrollTrigger + Lenis) en interactie */
(function () {
  var root = window.ROOT || "";
  var html = document.documentElement;
  html.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var touch = window.matchMedia("(hover: none)").matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  var LIGHT = document.body.classList.contains("theme-light");
  if (LIGHT) {
    var fxc = document.getElementById("fx"), hero = document.querySelector(".hero");
    if (fxc && hero) { hero.insertBefore(fxc, hero.firstChild); fxc.classList.add("in-hero"); }
    else if (fxc) fxc.remove();
  }
  var small = touch || window.innerWidth < 760;
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- Lenis: soepel scrollen (alleen met muis, niet op touch) ---------- */
  var lenis = null;
  if (window.Lenis && !reduce && !touch) {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    if (hasGsap) {
      lenis.on("scroll", ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
    }
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href"); if (id.length < 2) return;
        var el = document.querySelector(id); if (!el) return;
        e.preventDefault(); lenis.scrollTo(el, { offset: -80 });
      });
    });
  }

  /* ---------- nav, menu, voortgangsbalk ---------- */
  var nav = document.querySelector(".nav");
  var prog = document.querySelector(".progress");
  function onScroll() {
    var y = window.scrollY;
    if (nav) nav.classList.toggle("scrolled", y > 8);
    if (prog) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      prog.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  var burger = document.querySelector(".burger");
  if (burger) burger.addEventListener("click", function () {
    var open = document.body.classList.toggle("menu-open");
    burger.setAttribute("aria-expanded", open);
    if (lenis) open ? lenis.stop() : lenis.start();
  });

  /* ---------- zoeken met suggesties en productfoto's ---------- */
  var idx = null;
  function load(cb) { if (idx) return cb(idx); fetch(root + "search.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; cb(j); }).catch(function () {}); }
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  document.querySelectorAll("[data-search]").forEach(function (form) {
    var inp = form.querySelector("input"); var box = form.parentNode.querySelector(".results"); var sel = -1;
    function render(q) {
      load(function (list) {
        var words = norm(q).split(/\s+/).filter(Boolean);
        var hits = list.map(function (it) {
          var hay = norm(it.t + " " + it.k), s = 0;
          words.forEach(function (w) { if (hay.indexOf(w) > -1) s += (norm(it.t).indexOf(w) > -1 ? 3 : 1); else s -= 10; });
          return { it: it, s: s };
        }).filter(function (x) { return x.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, 7);
        box.innerHTML = hits.length ? hits.map(function (h) {
          return '<a href="' + root + h.it.u + '">' + (h.it.i ? '<img src="' + h.it.i + '" alt="">' : "") + '<span>' + h.it.t + '<small>' + h.it.c + ' · winnaar: ' + h.it.w + '</small></span></a>';
        }).join("") : '<a href="' + root + 'gidsen.html">Geen directe match. Bekijk alle gidsen</a>';
        box.classList.add("show"); sel = -1;
      });
    }
    inp.addEventListener("input", function () { var q = inp.value.trim(); if (q.length < 2) { box.classList.remove("show"); return; } render(q); });
    inp.addEventListener("keydown", function (e) {
      var items = box.querySelectorAll("a"); if (!items.length) return;
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length; items.forEach(function (a, i) { a.classList.toggle("hl", i === sel); }); }
    });
    form.addEventListener("submit", function (e) { e.preventDefault(); var a = box.querySelector("a.hl") || box.querySelector("a"); if (a) location.href = a.href; else if (inp.value.trim().length > 1) render(inp.value.trim()); });
    document.addEventListener("click", function (e) { if (!form.parentNode.contains(e.target)) box.classList.remove("show"); });
  });

  /* ---------- zoekopdracht uit de URL (?q=), voor Google-sitelinks zoekvak ---------- */
  var qp = new URLSearchParams(location.search).get("q");
  if (qp) document.querySelectorAll("[data-search] input").forEach(function (i, n) { if (n === 0 || i.offsetParent) { i.value = qp; i.dispatchEvent(new Event("input")); } });

  /* ---------- spotlight-hover op kaarten ---------- */
  if (!touch) document.querySelectorAll(".spot").forEach(function (el) {
    el.addEventListener("pointermove", function (e) { var r = el.getBoundingClientRect(); el.style.setProperty("--mx", (e.clientX - r.left) + "px"); el.style.setProperty("--my", (e.clientY - r.top) + "px"); });
  });

  /* ---------- magnetische knoppen ---------- */
  if (hasGsap && !touch && !reduce) document.querySelectorAll(".magnet").forEach(function (b) {
    b.addEventListener("pointermove", function (e) { var r = b.getBoundingClientRect(); gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .35, duration: .3, ease: "power3.out" }); });
    b.addEventListener("pointerleave", function () { gsap.to(b, { x: 0, y: 0, duration: .6, ease: "elastic.out(1,.4)" }); });
  });

  /* ---------- WebGL-achtergrond: vloeiende kleuren die per sectie wisselen ---------- */
  var PALETTES = [
    [[0.55,0.40,1.00],[1.00,0.36,0.78],[1.00,0.62,0.30]],
    [[1.00,0.42,0.55],[1.00,0.74,0.26],[0.98,0.32,0.80]],
    [[0.20,0.80,1.00],[0.55,0.45,1.00],[0.30,1.00,0.80]],
    [[1.00,0.84,0.20],[1.00,0.50,0.30],[1.00,0.40,0.70]],
    [[0.30,1.00,0.70],[0.20,0.75,1.00],[0.75,1.00,0.35]],
    [[1.00,0.40,0.85],[0.65,0.45,1.00],[0.30,0.85,1.00]],
    [[1.00,0.60,0.25],[1.00,0.90,0.30],[0.40,1.00,0.75]]
  ];
  var pal = { c: PALETTES[0].map(function (x) { return x.slice(); }) };
  // kleur volgt de scrollpositie continu: elke beweging van je duim verschuift de kleuren
  var scrollMix = 0, speed = 0, lastY = window.scrollY;
  function targetPalette() {
    if (LIGHT) return document.body.classList.contains("theme-green") ? [[0.05,0.45,0.36],[0.10,0.62,0.50],[1.00,0.55,0.20]] : PALETTES[0];
    var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    var f = Math.min(.9999, Math.max(0, window.scrollY / max)) * (PALETTES.length - 1);
    var i = Math.floor(f), k = f - i, A = PALETTES[i], B = PALETTES[Math.min(i + 1, PALETTES.length - 1)];
    k = k * k * (3 - 2 * k);
    return A.map(function (c, j) { return c.map(function (v, n) { return v + (B[j][n] - v) * k; }); });
  }
  window.addEventListener("scroll", function () { var y = window.scrollY; speed = Math.min(6, speed + Math.abs(y - lastY) * .02); lastY = y; }, { passive: true });
  window.__setHue = function () {};
  pal.c = targetPalette().map(function (x) { return x.slice(); });
  var cv = document.getElementById("fx");
  if (cv && !reduce) (function () {
    var gl = cv.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" });
    if (!gl) { cv.style.display = "none"; return; }
    var vs = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
    var fs = "precision mediump float;uniform vec2 r;uniform float t;uniform vec3 a;uniform vec3 b;uniform vec3 c;uniform vec2 m;" +
      "float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}" +
      "float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}" +
      "float fbm(vec2 p){float v=0.,s=.5;for(int i=0;i<5;i++){v+=s*n(p);p*=2.02;s*=.5;}return v;}" +
      "void main(){vec2 uv=gl_FragCoord.xy/r;vec2 p=uv*vec2(r.x/r.y,1.)*1.6;float T=t*.05;" +
      "vec2 q=vec2(fbm(p+T),fbm(p+vec2(5.2,1.3)-T));vec2 w=vec2(fbm(p+3.*q+vec2(1.7,9.2)+T*1.5),fbm(p+3.*q+vec2(8.3,2.8)-T));" +
      "float f=fbm(p+2.5*w);vec3 col=mix(a,b,smoothstep(.2,.8,f));col=mix(col,c,smoothstep(.45,1.,length(w)*.9));" +
      "float glow=.35/(1.+12.*length(uv-m));col+=glow*b;" +
      "float v=smoothstep(1.35,.2,length(uv-.5));col*=.78+.42*f;col=mix(vec3(.05,.03,.10),col,.82*v+.22);gl_FragColor=vec4(col,1.);}";
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }
    var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) { cv.style.display = "none"; return; }
    gl.useProgram(pr);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ["r", "t", "a", "b", "c", "m"].forEach(function (k) { U[k] = gl.getUniformLocation(pr, k); });
    var scale = (touch || window.innerWidth < 760) ? .35 : .5, mx = .5, my = .6, tmx = .5, tmy = .6;
    function size() { var W = LIGHT ? cv.clientWidth : window.innerWidth, H = LIGHT ? cv.clientHeight : window.innerHeight; cv.width = Math.round(W * scale); cv.height = Math.round(H * scale); gl.viewport(0, 0, cv.width, cv.height); }
    size(); window.addEventListener("resize", size);
    window.addEventListener("pointermove", function (e) { tmx = e.clientX / window.innerWidth; tmy = 1 - e.clientY / window.innerHeight; }, { passive: true });
    var t0 = performance.now(), hidden = false, flow = 0;
    document.addEventListener("visibilitychange", function () { hidden = document.hidden; });
    (function loop(now) {
      if (!hidden) {
        mx += (tmx - mx) * .04; my += (tmy - my) * .04;
        var tp = targetPalette();
        for (var j = 0; j < 3; j++) for (var n = 0; n < 3; n++) pal.c[j][n] += (tp[j][n] - pal.c[j][n]) * .06;
        speed *= .94; flow += (1 + speed * 2.2) * 16;
        gl.uniform2f(U.r, cv.width, cv.height); gl.uniform1f(U.t, flow / 1000);
        gl.uniform3fv(U.a, pal.c[0]); gl.uniform3fv(U.b, pal.c[1]); gl.uniform3fv(U.c, pal.c[2]); gl.uniform2f(U.m, mx, my);
        gl.drawArrays(gl.TRIANGLES, 0, 3);
      }
      requestAnimationFrame(loop);
    })(t0);
  })();

  /* ---------- cursorgloed ---------- */
  var glow = document.querySelector(".cursor-glow");
  if (glow && !touch && !LIGHT) {
    document.body.classList.add("has-cursor");
    var gx = 0, gy = 0, cx = 0, cy = 0;
    window.addEventListener("pointermove", function (e) { gx = e.clientX; gy = e.clientY; }, { passive: true });
    (function gl2() { cx += (gx - cx) * .12; cy += (gy - cy) * .12; glow.style.transform = "translate(" + cx + "px," + cy + "px)"; requestAnimationFrame(gl2); })();
  }

  /* ---------- 3D-kanteling op kaarten ---------- */
  if (!touch && !reduce && !LIGHT) document.querySelectorAll(".tilt").forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = "perspective(900px) rotateY(" + (x * 9) + "deg) rotateX(" + (-y * 9) + "deg) translateY(-4px)";
    });
    el.addEventListener("pointerleave", function () { el.style.transition = "transform .6s cubic-bezier(.2,.8,.2,1)"; el.style.transform = ""; setTimeout(function () { el.style.transition = ""; }, 600); });
  });

  /* ---------- zwevende producten volgen de muis ---------- */
  var fls = document.querySelectorAll(".fl");
  if (fls.length && !touch && !reduce) window.addEventListener("pointermove", function (e) {
    var x = e.clientX / window.innerWidth - .5, y = e.clientY / window.innerHeight - .5;
    fls.forEach(function (f) { var d = +f.getAttribute("data-depth") || .5; f.style.translate = (x * 60 * d) + "px " + (y * 40 * d) + "px"; });
  }, { passive: true });

  if (!hasGsap || reduce) { document.querySelectorAll(".rv").forEach(function (e) { e.style.opacity = 1; e.style.transform = "none"; }); initQuiz(); initFilters(); initSticky(); initToc(); return; }

  /* ---------- split-text koppen ---------- */
  if (!small) document.querySelectorAll(".split").forEach(function (el) {
    var html2 = el.innerHTML;
    // woorden in spans, html-tags (zoals <span class="grad">) blijven heel
    var out = html2.replace(/(<[^>]+>)|([^<\s]+)/g, function (m, tag, word) { return tag ? tag : '<span class="w"><span>' + word + "</span></span>"; });
    el.innerHTML = out; el.classList.add("is-split");
    gsap.from(el.querySelectorAll(".w>span"), { yPercent: 110, duration: .9, ease: "power4.out", stagger: .05, delay: .1 });
  });

  /* ---------- reveal bij scrollen ---------- */
  ScrollTrigger.batch(".rv", {
    start: "top 90%",
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: .8, ease: "power3.out", stagger: .07, overwrite: true }); }
  });

  /* ---------- tellers ---------- */
  if (!small) document.querySelectorAll("[data-count]").forEach(function (el) {
    var end = +el.getAttribute("data-count"), o = { v: 0 };
    ScrollTrigger.create({ trigger: el, start: "top 92%", once: true, onEnter: function () {
      gsap.to(o, { v: end, duration: 1.6, ease: "power2.out", onUpdate: function () { el.textContent = Math.round(o.v).toLocaleString("nl-NL"); } });
    } });
  });

  /* ---------- scorebalken ---------- */
  document.querySelectorAll(".bar em").forEach(function (b) {
    gsap.from(b, { scaleX: 0, duration: 1.1, ease: "power3.out", scrollTrigger: { trigger: b, start: "top 92%" } });
  });

  /* ---------- hero parallax ---------- */
  var hb = document.querySelector(".hero-in");
  if (hb && !small) gsap.to(hb, { yPercent: 18, opacity: .3, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });

  initQuiz(); initFilters(); initSticky(); initToc();

  /* ---------- helpers ---------- */
  function initSticky() {
    var s = document.querySelector(".sticky-buy"), pd = document.querySelector(".podium");
    if (!s || !pd) return; document.body.classList.add("has-sticky");
    function chk() { s.classList.toggle("on", pd.getBoundingClientRect().bottom < 0); }
    window.addEventListener("scroll", chk, { passive: true }); chk();
  }
  function initToc() {
    var toc = document.querySelector(".toc"); if (!toc) return;
    if (window.innerWidth > 980) toc.open = true;
    var links = toc.querySelectorAll("a[href^='#']");
    if (!("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) links.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + x.target.id); }); });
    }, { rootMargin: "-40% 0px -55% 0px" });
    links.forEach(function (a) { var t = document.querySelector(a.getAttribute("href")); if (t) io.observe(t); });
  }
  function initFilters() {
    var bar = document.querySelector(".filters"); if (!bar) return;
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      bar.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
      var c = b.getAttribute("data-cat");
      document.querySelectorAll("[data-cat-item]").forEach(function (el) { el.style.display = (c === "alle" || el.getAttribute("data-cat-item") === c) ? "" : "none"; });
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  }
  function initQuiz() {
    var q = document.querySelector(".quiz"); if (!q || !window.QUIZ) return;
    var data = window.QUIZ, state = {}, steps = q.querySelectorAll(".q-step"), bar = q.querySelector(".q-prog i");
    function show(i) { steps.forEach(function (s, j) { s.classList.toggle("on", j === i); }); bar.style.width = (i / (steps.length - 1) * 100) + "%"; }
    q.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-k]");
      if (b) {
        state[b.getAttribute("data-k")] = b.getAttribute("data-v");
        if (b.getAttribute("data-k") === "gids") {
          var g = data[state.gids], opts = q.querySelector("#q-budget");
          opts.innerHTML = g.budgets.map(function (x) { return '<button data-k="budget" data-v="' + x.max + '"><b>' + x.label + '</b><small>' + x.hint + '</small></button>'; }).join("");
        }
        var next = +b.closest(".q-step").getAttribute("data-i") + 1;
        if (next === steps.length - 1) result();
        show(next); return;
      }
      if (e.target.closest(".q-back")) { var cur = +q.querySelector(".q-step.on").getAttribute("data-i"); show(Math.max(0, cur - 1)); }
    });
    function result() {
      var g = data[state.gids], max = +state.budget, prio = state.prio;
      var pool = g.products.filter(function (p) { return p.price <= max; });
      if (!pool.length) pool = g.products.slice().sort(function (a, b) { return a.price - b.price; }).slice(0, 1);
      pool.sort(function (a, b) {
        if (prio === "prijs") return (b.score / b.price) - (a.score / a.price);
        if (prio === "premium") return b.price - a.price || b.score - a.score;
        return b.score - a.score;
      });
      var p = pool[0], alt = pool[1];
      q.querySelector(".q-out").innerHTML =
        '<div class="q-res">' + (p.image ? '<img src="' + p.image + '" alt="">' : "") + '<div><span class="kick">Jouw beste keuze</span><h3 style="font-size:1.4rem">' + p.name + '</h3><p class="muted">' + p.oneliner + '</p><p><b style="font-family:Sora;font-size:1.3rem">€ ' + p.priceTxt + '</b> · score ' + p.score + '/10</p>' +
        '<a class="btn btn-buy" href="' + p.link + '" rel="sponsored nofollow noopener" target="_blank" data-umami-event="bol-klik" data-umami-event-gids="keuzehulp-' + state.gids + '" data-umami-event-product="' + p.name + '">Bekijk bij bol <span class="arr">→</span></a> ' +
        '<a class="btn btn-light" href="' + root + g.url + '">Hele top 10</a>' + (alt ? '<p class="muted" style="margin-top:12px;font-size:.9rem">Ook goed: <b>' + alt.name + '</b> voor € ' + alt.priceTxt + '</p>' : "") + "</div></div>";
    }
    show(0);
  }
})();
