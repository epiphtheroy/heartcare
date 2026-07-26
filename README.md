# 하트케어내과 홈페이지 — 인수인계 문서

> **다른 AI/개발자가 이 문서만 읽고 중복·누락 없이 이어받도록 정리한 정본.** 작업 전 이 문서를 끝까지 읽으세요.

---

## 0. 한눈에

- **무엇**: 여의도 심장전문 내과 **하트케어내과**(대표원장 **최순욱**) 홍보 원페이지 + 세부페이지. 2026년 **11월** 개원 예정.
- **라이브(배포됨)**: **https://epiphtheroy.github.io/heartcare/** (GitHub Pages)
- **스택**: 빌드 없는 **정적 사이트** — HTML + CSS + Vanilla JS + 실사/SVG. 프레임워크 없음.
- **정본 위치**: `/Users/jerryje/Documents/하트클리닉/homepage/`
- **로컬 실행**: `cd homepage && python3 -m http.server 7000` → http://localhost:7000

---

## 1. 배포 방법 (⚠️ 가장 중요 — 이대로만 하면 됨)

GitHub 레포 **`epiphtheroy/heartcare`** (public) → **GitHub Pages**(main 브랜치 루트)로 자동 서빙.

**인증**: 사용자 제공 GitHub PAT가 `homepage/.env`에 `GH_TOKEN=...`로 저장돼 있음(**`.gitignore`로 격리, 절대 커밋 금지**). git push 시 이 토큰을 env로 로드해서 사용.

**변경 → 배포 절차** (그대로 복붙):
```bash
cd /Users/jerryje/Documents/하트클리닉/homepage
set -a; . ./.env; set +a                       # GH_TOKEN 로드 (매 세션/쉘마다)
# (필요시) python3 tools/gen_exams.py; python3 tools/gen_spaces.py   # ← §3 참고
git add -A
git -c user.email="noreply@anthropic.com" -c user.name="Claude" commit -m "변경 내용"
git push origin main
# Pages 재빌드 ~40~60초. 완료 확인(포그라운드 sleep 금지 → python sleep 사용):
for i in $(seq 1 20); do curl -s "https://epiphtheroy.github.io/heartcare/css/main.css" | grep -q "바뀐문구" && { echo OK; break; }; python3 -c "import time;time.sleep(7)"; done
```

- **토큰 노출 주의**: 명령에 토큰을 직접 쓰지 말고 항상 `$GH_TOKEN`(env)로. 레포가 public이니 `.env`가 커밋되지 않았는지 `git ls-files | grep .env`(→ 0이어야 정상) 확인.
- 토큰 만료/교체 시: 사용자가 github.com/settings/tokens에서 새 PAT(repo 스코프) 발급 → `.env`의 `GH_TOKEN=`만 갱신.

---

## 2. 파일 구조

```
index.html            # 원페이지 전체 (헤더 · 섹션들 · 푸터)
css/main.css          # 디자인 시스템 + 전 컴포넌트 + 세부페이지 + 개념도 (단일 CSS)
js/main.js            # 스크롤스파이·리빌·카운트업·히어로스케일·정밀검사 그리드 렌더
data/exams.json       # 정밀검사 9종 데이터 (그리드 + 세부페이지 공용 소스)  ← §3
data/spaces.json      # 공간 4종 데이터 (세부페이지 소스)                     ← §3
exam/<slug>.html      # 정밀검사 세부페이지 9개 (gen_exams.py로 생성 — 직접 편집 금지)
space/<slug>.html     # 공간 세부페이지 4개 (gen_spaces.py로 생성 — 직접 편집 금지)
tools/gen_exams.py    # exams.json → exam/*.html 생성기
tools/gen_spaces.py   # spaces.json → space/*.html 생성기 (conceptmap import)
tools/conceptmap.py   # 공간 일러스트 개념도 SVG 생성 (세부페이지 인라인 강조용)  ← §4
assets/real/          # 실사 이미지 (히어로·의료진·방송4·공간3·장비9·지도·평면도)
assets/conceptmap.svg # conceptmap.py 산출물 — 현재 index에서 미참조(고아). 삭제 가능
이미지/                # 사용자 원본 업로드(카톡·스크린샷) — 소스 보관용, 배포 제외
.env                  # GH_TOKEN (gitignore됨)
```

**세부페이지(exam/·space/)는 생성물이므로 직접 편집하지 말 것.** `data/*.json` 또는 `tools/gen_*.py`를 고치고 재생성(§3).

---

## 3. 데이터 주도 구조 (⚠️ 재생성 규칙)

### exams.json (정밀검사 9종) — **두 곳에서 소비됨**
필드: `slug, name, badge, image, short, lead, highlight, whoFor[], features[], tags[], compare?`
- `compare` 보유: **holter, bp** (비교표). 형식: `{title, head:[3], rows:[[3]...]}` (마지막 열=본원 강조).
- **메인 #exams 그리드**: `js/main.js`가 런타임에 `fetch("data/exams.json")` 해서 카드 렌더 → `name/badge/image/short/tags` 수정은 **재생성 불필요**(새로고침이면 반영).
- **세부페이지 exam/*.html**: `gen_exams.py`가 생성 → `lead/whoFor/features/highlight/compare` 수정은 **`python3 tools/gen_exams.py` 재실행 필요**.

### spaces.json (공간 4종) — **세부페이지에서만 소비됨**
필드: `slug, name, badge, image, short, lead, points[]`
- **메인 #space 카드 4개는 `index.html`에 정적 HTML**(자동 렌더 아님) → 카드 문구·이미지 변경은 index.html 직접 수정.
- **세부페이지 space/*.html**: `gen_spaces.py` 생성 → `lead/points` 등 수정 시 **`python3 tools/gen_spaces.py` 재실행**.

### 재생성 후엔 반드시 커밋·푸시(§1).

---

## 4. 공간 개념도 (conceptmap.py)

- 알록달록 top-down 일러스트 평면도. **실제 4안 배치 반영**(대기 라운지 중앙, 진료실 북측, 검사 서/남, 접수 중앙하단, 약국 동측).
- `clinic_map_svg(highlight)` → 특정 공간(방)을 빨간 테두리+글로우로 강조, 나머지는 흐림.
- 공간↔방 매핑은 `conceptmap.py`의 **`HIGHLIGHT` dict**에서 수정. 방 좌표·색은 `ROOMS`, `ZONES`.
- 각 **공간 세부페이지**에 해당 공간 강조 버전이 인라인 삽입됨(gen_spaces.py). **메인 페이지에는 개념도 없음**(사용자 요청으로 제거).

---

## 5. 디자인 시스템

- **팔레트**: 화이트 바탕 + **이코노미스트 레드 `#E3120B`** 단일 강조 (심장내과 = 붉은색). CSS `:root` 변수로 전부 정의.
- **폰트 3종**:
  - **로고 워드마크** = **JalnanGothic(여기어때 잘난체 고딕)** — `@font-face`로 로드(`cdn.jsdelivr.net/gh/fontbee/font@main/gccompany/JalnanGothic.woff`). 헤비 각진 디스플레이.
  - **디스플레이(제목)** = Noto Serif KR (Google Fonts)
  - **본문/UI** = Pretendard Variable (jsdelivr)
- **로고**(`.brand`): 인라인 SVG 하트+맥파 문양 + 워드마크 `하트케어<em>내과</em>`(내과=레드) 밀착. 문양 높이 `1.0em`+`translateY(-0.06em)`(글자보다 살짝 크고 위로). 영문 서브라인 없음. 헤더엔 `.brand-branch`(여의도 | 본점 레드칩). 큰 버전 `.brand-lg`(진료분야 헤딩·푸터). **로고 SVG/마크업이 index.html 3곳 + 생성기 LOGO 상수에 중복** → 문양 바꾸면 전부 같이 수정.
- **동적 요소**: 로고 하트비트, 키커 점멸, 키워드 `.kw`(스크롤 시 색 리빌+숨쉬는 밑줄), ECG 드로우, 통계 카운트업, 카드 호버, 탭 스크롤스파이+active 확대, **히어로 이미지 스크롤 스케일**(§6).
- 모든 모션은 `prefers-reduced-motion` 존중(자동 비활성).

---

## 6. 섹션 구성 & 주요 인터랙션 (index.html 순서)

헤더(로고+여의도본점 / 배지"2026. 11 개원" / 오시는길 / 탭네비 8개) →
1. **히어로**: 강연 배너 실사(hero-lecture.jpg) + 2줄 H1 + 부제 + 리드 + CTA(정밀검사/왜하트케어) + 통계.
   - **히어로 스크롤 스케일**(js/main.js): 스크롤 상단부터 시작, 28%에서 최대 **1.15배**, 하단으로 갈수록 ~0.9로 축소. (`scrollY / heroFig.offsetHeight` 기반)
2. **소개(#about)**: 3기둥 카드.
3. **의료진(#doctor)**: 다크 섹션, 최순욱 실사(multiply 블렌드) + 약력 3열 + 방송 5카드(강연+KBS/SBS/TV조선/MBN) + Q&A.
4. **진료분야(#clinics)**: 헤딩 = "365일, 심장 혈관만 생각하는" + 로고. CLINIC 01~03 배지, 아이콘칩·증상태그·체크불릿 카드 9개(모바일 좌우 스크롤).
5. **정밀검사(#exams)**: 강점 스트립 3(당일판독/대학병원급/전문의직접) + JS 렌더 카드 9개(장점 키워드 뱃지 포함). 각 카드 → exam/*.html.
6. **공간(#space)**: 실사 4카드(정적) → space/*.html(설계원칙 + 개념도 강조).
7. **진료안내(#hours)**: 진료시간표.
8. **오시는길(#contact)**: **지도 = 정적 위성 이미지**(assets/real/map.jpg, 네이버 스크린샷) + 핀 오버레이 + 네이버지도 링크. 주소/지하철/주차/문의 카드 4.
9. **왜 하트케어인가(#why)**: 다크, 3논리(vs 큰병원 시간·분절 / vs 일반내과 전문성).
푸터: 365 태그라인 + 로고 + 개원소식 버튼 + 정보.

세부페이지(exam/space)엔 상단 전체 네비 + "← 전체보기" 뒤로가기 + 브레드크럼 모두 있음(네비 유지).

---

## 7. 콘텐츠 · 이미지 출처

- 약력·진료·장비·주소·교통: **seoulheart.com**(하트케어내과 공식). 정밀검사 세부 장점은 seoulheart 장비 상세페이지 5종 반영(당일결과·임상병리실직영·3일패치·무압박반지형·방사선없음 등 — 축소·은폐 금지 원칙).
- 실사: 히어로·방송4·프로필=사용자 카톡(`이미지/`), 의료진·장비9=seoulheart, 지도=사용자 네이버 스크린샷.
- **공간 3장(라운지·접수·상담)= Unsplash 무료 연출컷** → 완공 후 실사 교체 예정. **홀터=패치(holter.png)/24h혈압=반지(bp.jpg)** 정본.
- 구조 참고(카피는 전량 재작성): asanheart.com, wimclinic.com.
- 이미지 최적화: 사진 PNG→JPG·최대 ~1400px 다운스케일 완료(총 ~9MB).

---

## 8. 작업 시 함정(Gotchas) — 모르면 시간 낭비

1. **Edit 툴이 index.html/main.css에서 "File has been modified since read" 로 실패**(린터가 파일을 건드림) → 해당 파일 편집은 **python 스크립트(read+replace+write)** 나 **sed** 로 하면 안정적. (.py/.json/.js는 Edit 대체로 OK)
2. **헤드리스 Chrome QA**: (a) 창 최소폭 500px 클램프 → **모바일(390px) 검수는 iframe 하네스**로. (b) **`#anchor` URL 스크린샷은 자주 백지** → 전체 페이지 렌더 후 `sips -c H W --cropOffset Y 0` 로 크롭. (c) 폰트/이미지/fetch 로드 위해 `--force-prefers-reduced-motion --virtual-time-budget=3000~8000` 사용.
3. **포그라운드 `sleep` 차단** → Pages 재빌드 폴링은 `python3 -c "import time;time.sleep(7)"` 루프.
4. **Vercel MCP 배포는 바이너리 인라인 불가** → 반드시 git 기반 배포(§1). Vercel로 옮기려면 vercel.com에서 이 GitHub 레포 Import.
5. **서브패스 서빙**: Pages가 `/heartcare/` 하위라 **모든 경로는 상대경로**여야 함(현재 그렇게 돼 있음 — 절대 `/` 경로 쓰지 말 것).
6. `assets/real/`의 `logo.png/profile.png/cert-echo.png/clinic-wall.jpg` = 미사용 보관(레포엔 있음). `assets/conceptmap.svg` = 미참조 고아. `css/main.css`의 `.mk-pin/.mk-station/.leaflet-*` = 구 지도(Leaflet) 잔재 dead CSS. 정리해도 무방.

---

## 9. 남은 것 / 다음 후보 (TODO)

- **전화번호**: 개원 시 공개(현재 이메일 heartcareclinic@naver.com만). 확정되면 헤더·문의카드·푸터 갱신.
- **공간 실사**: 완공 후 `space-lounge/reception/consult.jpg`를 실제 사진으로 교체 + `#space`·세부페이지·푸터의 "연출 이미지" 고지문 삭제.
- **지도**: 현재 정적 이미지. 카카오맵 라이브로 바꾸려면 카카오 JS키 발급→`js/main.js`의 "지도" 주석 위치에 SDK 초기화 추가 + `index.html`의 `.map-wrap`을 `<div id="map">`으로.
- **커스텀 도메인**: 도메인 확보 시 GitHub Pages(또는 Vercel) 연결.
- 개원일 확정 시 "2026년 11월"/"2026. 11 개원" 일괄 확인.

## 10. 하지 말 것
- 세부페이지(exam/·space/*.html) 직접 편집(생성물 — §3).
- `.env`/토큰 커밋. 절대경로(`/…`) 링크 사용(서브패스 깨짐).
- 정밀검사 장점 축소·은폐(사용자 명시 원칙).
- 로고 문양 수정 시 일부만 바꾸기(index 3곳+생성기 LOGO 전부 동기).
