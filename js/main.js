/* 하트케어내과 — 인터랙션: 스크롤스파이 · 리빌 · 카운트업 · 검사그리드 · 지도 */
(function () {
  "use strict";
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── 헤더 스크롤 상태 ── */
  const head = document.getElementById("siteHead");
  const onScroll = () => head.classList.toggle("scrolled", scrollY > 8);
  onScroll(); addEventListener("scroll", onScroll, { passive: true });

  /* ── 리빌 옵저버 (.in) ── */
  const revs = document.querySelectorAll(".reveal");
  if (reduced) revs.forEach((e) => e.classList.add("in"));
  else {
    const ro = new IntersectionObserver(
      (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); ro.unobserve(e.target); } }),
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    revs.forEach((e) => ro.observe(e));
  }

  /* ── 카운트업 (hero-proof의 선두 숫자) ── */
  function countUp(node, target) {
    if (reduced) { node.textContent = target; return; }
    const dur = 1100, t0 = performance.now();
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      node.textContent = Math.round(target * e);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
  const proof = document.querySelector(".hero-proof");
  if (proof) {
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => {
        if (!e.isIntersecting) return;
        proof.querySelectorAll("strong").forEach((s) => {
          const n = s.firstChild;
          if (n && n.nodeType === 3 && /^\d+$/.test(n.textContent.trim())) {
            const target = parseInt(n.textContent, 10);
            n.textContent = "0"; countUp(n, target);
          }
        });
        io.disconnect();
      });
    }, { threshold: 0.4 });
    io.observe(proof);
  }

  /* ── 정밀검사 그리드 렌더 ── */
  const grid = document.getElementById("examGrid");
  if (grid) {
    fetch("data/exams.json").then((r) => r.json()).then((exams) => {
      grid.innerHTML = exams.map((x, i) => `
        <a class="card exam-card reveal${i % 3 ? " d" + (i % 3) : ""}" href="exam/${x.slug}.html" aria-label="${x.name} 자세히 보기">
          <div class="exam-media"><span class="exam-badge">${x.badge}</span>
            <img src="${x.image}" alt="${x.name} 검사 장비" loading="lazy"></div>
          <div class="exam-body">
            <h3>${x.name}</h3><p>${x.short}</p>
            <span class="exam-more">자세히 보기 <span class="arr">→</span></span>
          </div>
        </a>`).join("");
      // 새로 삽입된 카드도 리빌 관찰
      const cards = grid.querySelectorAll(".reveal");
      if (reduced) cards.forEach((e) => e.classList.add("in"));
      else {
        const ro2 = new IntersectionObserver(
          (es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); ro2.unobserve(e.target); } }),
          { rootMargin: "0px 0px -6% 0px", threshold: 0.05 });
        cards.forEach((e) => ro2.observe(e));
      }
    }).catch(() => { grid.innerHTML = '<p style="color:var(--ink-weak)">검사 정보를 불러오지 못했습니다.</p>'; });
  }

  /* ── 스크롤스파이 탭 ── */
  const tabs = [...document.querySelectorAll(".tab[data-spy]")];
  const track = document.getElementById("tabTrack");
  const secs = tabs.map((t) => document.querySelector(t.getAttribute("href"))).filter(Boolean);
  let active = null;
  function setActive(tab) {
    if (tab === active) return; active = tab;
    tabs.forEach((t) => { const on = t === tab; t.classList.toggle("active", on);
      on ? t.setAttribute("aria-current", "true") : t.removeAttribute("aria-current"); });
    if (tab && track) {
      const tr = track.getBoundingClientRect(), tb = tab.getBoundingClientRect();
      if (tb.left < tr.left + 12 || tb.right > tr.right - 12)
        track.scrollTo({ left: tab.offsetLeft - (track.clientWidth - tab.offsetWidth) / 2, behavior: "smooth" });
    }
  }
  const spy = new IntersectionObserver((es) => {
    const vis = es.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (vis.length) setActive(tabs.find((t) => t.getAttribute("href") === "#" + vis[0].target.id) || null);
  }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
  secs.forEach((s) => spy.observe(s));
  addEventListener("scroll", () => { if (scrollY < 220) setActive(null); }, { passive: true });

  /* 지도: 현재는 정적 위성 이미지(map.png, index.html에 직접 삽입).
     카카오 JS키 발급 후 라이브 지도로 교체 예정 — 그때 이 위치에 SDK 초기화 코드 추가. */

  /* ── 히어로 이미지 스크롤 스케일 (은은하게 커졌다가 사라질 때 작아짐) ── */
  const heroFig = document.querySelector(".hero-figure");
  const heroImg = heroFig && heroFig.querySelector("img");
  if (heroImg && !reduced) {
    let ticking = false;
    const paint = () => {
      ticking = false;
      const r = heroFig.getBoundingClientRect();
      const vh = innerHeight || document.documentElement.clientHeight;
      const p = Math.min(1, Math.max(0, -r.top / (r.height + vh * 0.5)));
      const scale = 1 + 0.08 * Math.sin(p * Math.PI) - 0.045 * p; // 1 → 1.06 → 0.96
      heroImg.style.transform = "scale(" + scale.toFixed(4) + ")";
    };
    const onScrollHero = () => { if (!ticking) { ticking = true; requestAnimationFrame(paint); } };
    addEventListener("scroll", onScrollHero, { passive: true });
    addEventListener("resize", onScrollHero, { passive: true });
    paint();
  }

})();
