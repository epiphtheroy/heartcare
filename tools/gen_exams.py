# -*- coding: utf-8 -*-
"""exams.json → exam/<slug>.html 세부페이지 생성. index와 동일 디자인 시스템 사용."""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exams = json.load(open(os.path.join(ROOT, "data", "exams.json"), encoding="utf-8"))
outdir = os.path.join(ROOT, "exam"); os.makedirs(outdir, exist_ok=True)
E = lambda s: html.escape(s, quote=True)

LOGO = '''<svg class="brand-mark" viewBox="5 0 38 40" aria-hidden="true">
  <path class="heart" d="M24 36.5C24 36.5 6 25.5 6 14C6 8.4 10 5 14.6 5C18.6 5 21.8 7.4 24 10.6C26.2 7.4 29.4 5 33.4 5C38 5 42 8.4 42 14C42 25.5 24 36.5 24 36.5Z"/>
  <path class="pulse" d="M12 20H17L20 13.5L24 27L27 18L29 20H40"/></svg>
<span class="brand-word">하트케어<em>내과</em></span>
<span class="brand-branch"><i>여의도</i><b>본점</b></span>'''

def nav_html(active):
    items = [("about","소개"),("doctor","의료진"),("clinics","진료분야"),("exams","정밀검사"),
             ("space","공간"),("hours","진료안내"),("contact","오시는길"),("why","왜 하트케어인가")]
    links = "".join(f'<a href="../index.html#{k}" class="tab{" active" if k==active else ""}">{v}</a>' for k,v in items)
    return f'<nav class="tab-nav" aria-label="주요 메뉴"><div class="tab-track">{links}</div></nav>'
NAV = nav_html("exams")

def others_html(cur):
    cards = ""
    for x in exams:
        if x["slug"] == cur: continue
        cards += f'''<a class="ed-other" href="{x['slug']}.html"><img src="../{x['image']}" alt="{E(x['name'])}" loading="lazy"><span>{E(x['name'])}</span></a>'''
    return cards

def page(x):
    who = "".join(f"<li>{E(w)}</li>" for w in x["whoFor"])
    feat = "".join(f"<li>{E(f)}</li>" for f in x["features"])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(x['name'])} — 하트케어내과 정밀검사</title>
<meta name="description" content="{E(x['short'])}">
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
      <nav class="subnav"><a href="../index.html">홈</a><span class="sep">/</span><a href="../index.html#exams">정밀검사</a><span class="sep">/</span><b>{E(x['name'])}</b></nav>
      <a class="btn btn-sm btn-primary" href="../index.html#contact">오시는 길</a>
    </div>
  </div>
  {NAV}
</header>

<main>
<section class="sec" style="padding-top:clamp(40px,5vw,64px)">
  <div class="wrap">
    <a class="ed-back" href="../index.html#exams"><span class="arr">←</span> 정밀검사 전체보기</a>
    <div class="ed-hero">
      <figure class="ed-media"><img src="../{x['image']}" alt="{E(x['name'])} 검사 장비"></figure>
      <div>
        <span class="ed-badge">{E(x['badge'])}</span>
        <h1 class="ed-title">{E(x['name'])}</h1>
        <p class="ed-lead">{E(x['lead'])}</p>
        <a class="btn btn-primary" href="../index.html#contact" style="margin-top:28px">진료 문의하기 <span class="arr">→</span></a>
      </div>
    </div>

    <div class="ed-cols">
      <div class="card ed-panel">
        <h3><span class="num">01</span> 이런 분께 권합니다</h3>
        <ul class="ed-list dot">{who}</ul>
      </div>
      <div class="card ed-panel">
        <h3><span class="num">02</span> 검사 특징</h3>
        <ul class="ed-list check">{feat}</ul>
      </div>
    </div>

    <div class="ed-cta">
      <h3>{E(x['name'])}, 원내에서 당일 진행합니다</h3>
      <p>2026년 8월 여의도 개원 · 국회의사당역 도보 1분</p>
      <a class="btn btn-primary" href="../index.html#contact">오시는 길 · 문의 <span class="arr">→</span></a>
    </div>

    <div class="ed-others">
      <h4>다른 정밀검사</h4>
      <div class="ed-others-grid">{others_html(x['slug'])}</div>
    </div>
  </div>
</section>
</main>

<footer class="site-foot">
  <div class="wrap foot-grid">
    <a class="brand on-dark" href="../index.html" aria-label="하트케어내과 홈">{LOGO}</a>
    <p class="foot-info">하트케어내과 · 대표원장 최순욱 · 서울 영등포구 은행로 3 (여의도동) 삼희익스콘벤처타워 2층 · 2026년 8월 개원 예정<br>사업자등록번호 발급 중 · 문의 <a href="mailto:heartcareclinic@naver.com">heartcareclinic@naver.com</a></p>
    <p class="foot-legal">ⓒ 2026 HeartCare Internal Medicine Clinic.</p>
  </div>
</footer>
</body>
</html>'''

for x in exams:
    with open(os.path.join(outdir, x["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(page(x))
print(f"생성: {len(exams)}개 세부페이지 → exam/")
for x in exams: print("  exam/" + x["slug"] + ".html")
