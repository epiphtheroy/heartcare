# -*- coding: utf-8 -*-
"""spaces.json → space/<slug>.html. 실사 + 설계 원칙 + 실제 평면도."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conceptmap import clinic_map_svg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spaces = json.load(open(os.path.join(ROOT, "data", "spaces.json"), encoding="utf-8"))
outdir = os.path.join(ROOT, "space"); os.makedirs(outdir, exist_ok=True)
E = lambda s: html.escape(s, quote=True)

LOGO = '''<svg class="brand-mark" viewBox="0 0 48 40" aria-hidden="true">
  <path class="heart" d="M24 36.5C24 36.5 6 25.5 6 14C6 8.4 10 5 14.6 5C18.6 5 21.8 7.4 24 10.6C26.2 7.4 29.4 5 33.4 5C38 5 42 8.4 42 14C42 25.5 24 36.5 24 36.5Z"/>
  <path class="pulse" d="M12 20H17L20 13.5L24 27L27 18L29 20H40"/></svg>
<span class="brand-word">하트케어<em>내과</em></span>
<span class="brand-branch"><i>여의도</i><b>본점</b></span>'''

def nav_html(active):
    items = [("about","소개"),("doctor","의료진"),("clinics","진료분야"),("exams","정밀검사"),
             ("space","공간"),("hours","진료안내"),("contact","오시는길"),("why","왜 하트케어인가")]
    links = "".join(f'<a href="../index.html#{k}" class="tab{" active" if k==active else ""}">{v}</a>' for k,v in items)
    return f'<nav class="tab-nav" aria-label="주요 메뉴"><div class="tab-track">{links}</div></nav>'
NAV = nav_html("space")

def others_html(cur):
    out = ""
    for s in spaces:
        if s["slug"] == cur: continue
        out += f'<a class="ed-other" href="{s["slug"]}.html"><img src="../{s["image"]}" alt="{E(s["name"])}" loading="lazy"><span>{E(s["name"])}</span></a>'
    return out

def page(s):
    pts = "".join(f"<li>{E(p)}</li>" for p in s["points"])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(s['name'])} — 하트케어내과 공간 설계</title>
<meta name="description" content="{E(s['short'])}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;600;700&display=swap">
<link rel="stylesheet" href="../css/main.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Cpath d='M20 34C20 34 5 24.5 5 14.5C5 9.2 9 6 13 6C16.2 6 18.6 8 20 10.4C21.4 8 23.8 6 27 6C31 6 35 9.2 35 14.5C35 24.5 20 34 20 34Z' fill='%23E3120B'/%3E%3Cpath d='M8 19H14L16.5 13L20 25L22.5 17.5L24 19H32' fill='none' stroke='%23fff' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
</head>
<body>
<div class="topline"></div>
<header class="site-head">
  <div class="head-bar">
    <a class="brand" href="../index.html" aria-label="하트케어내과 홈">{LOGO}</a>
    <div class="head-cta">
      <nav class="subnav"><a href="../index.html">홈</a><span class="sep">/</span><a href="../index.html#space">공간</a><span class="sep">/</span><b>{E(s['name'])}</b></nav>
      <a class="btn btn-sm btn-primary" href="../index.html#contact">오시는 길</a>
    </div>
  </div>
  {NAV}
</header>

<main>
<section class="sec" style="padding-top:clamp(40px,5vw,64px)">
  <div class="wrap">
    <a class="ed-back" href="../index.html#space"><span class="arr">←</span> 공간 전체보기</a>
    <div class="ed-hero">
      <figure class="ed-media"><img src="../{s['image']}" alt="{E(s['name'])}"></figure>
      <div>
        <span class="ed-badge">{E(s['badge'])}</span>
        <h1 class="ed-title">{E(s['name'])}</h1>
        <p class="ed-lead">{E(s['lead'])}</p>
        <a class="btn btn-primary" href="../index.html#contact" style="margin-top:28px">오시는 길 · 문의 <span class="arr">→</span></a>
      </div>
    </div>

    <div class="ed-cols">
      <div class="card ed-panel">
        <h3><span class="num">◆</span> 설계 원칙</h3>
        <ul class="ed-list check">{pts}</ul>
      </div>
      <figure class="card ed-panel cmap-panel">
        <figcaption class="cmap-cap">공간 개념도 · <b>{E(s['name'])}</b> 위치</figcaption>
        <div class="cmap">{clinic_map_svg(s['slug'])}</div>
      </figure>
    </div>
    <p class="space-note" style="margin-top:18px">위 사진은 설계 방향을 보여주는 연출 이미지이며, 개념도는 실제 공간 배치를 이해하기 쉽게 나타낸 그림입니다. 완공 후 실제 공간 사진으로 교체됩니다.</p>

    <div class="ed-cta">
      <h3>진료 동선까지 설계한 공간에서 뵙겠습니다</h3>
      <p>2026년 8월 여의도 개원 · 국회의사당역 도보 1분</p>
      <a class="btn btn-primary" href="../index.html#contact">오시는 길 · 문의 <span class="arr">→</span></a>
    </div>

    <div class="ed-others">
      <h4>다른 공간</h4>
      <div class="ed-others-grid">{others_html(s['slug'])}</div>
    </div>
  </div>
</section>
</main>

<footer class="site-foot">
  <div class="wrap foot-grid">
    <a class="brand on-dark" href="../index.html" aria-label="하트케어내과 홈">{LOGO}</a>
    <p class="foot-info">하트케어내과 · 대표원장 최순욱 · 서울 영등포구 은행로 3 (여의도동) 삼희익스콘벤처타워 2층 · 2026년 8월 개원 예정<br>사업자등록번호 발급 중 · 문의 <a href="mailto:heartcareclinic@naver.com">heartcareclinic@naver.com</a></p>
    <p class="foot-legal">공간 이미지는 설계 방향 연출 이미지이며, 실제와 다를 수 있습니다. ⓒ 2026 HeartCare Internal Medicine Clinic.</p>
  </div>
</footer>
</body>
</html>'''

for s in spaces:
    with open(os.path.join(outdir, s["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page(s))
print(f"생성: {len(spaces)}개 공간 세부페이지 → space/")
for s in spaces: print("  space/" + s["slug"] + ".html")
