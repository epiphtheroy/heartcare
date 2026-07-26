# 하트케어내과 홈페이지 (v2 — Editorial Red)

여의도 심장전문 내과 **하트케어내과** (대표원장 최순욱) 원페이지 사이트.
의존성 없는 정적 사이트 — HTML + CSS + JS + 실사 이미지 · Pretendard/Noto Serif KR(CDN).

## 실행
```bash
cd homepage
python3 -m http.server 7000    # → http://localhost:7000
```

## 디자인 방향
- **팔레트**: 화이트 바탕 + **이코노미스트 레드 `#E3120B`** 단일 강조 (심장내과 = 붉은색)
- **타이포**: Noto Serif KR(디스플레이) + Pretendard(본문)
- **동적 요소**: 로고 하트비트, 키커 점멸, 키워드 색 리빌+숨쉬는 밑줄(`.kw`), ECG 라인 드로우,
  통계 카운트업, 카드 호버 리프트+상단 레드 라인, 탭 스크롤스파이

## 구조
```
index.html            # 원페이지 (소개/의료진/진료분야/정밀검사/공간/진료안내/오시는길/Why)
css/main.css          # 디자인 시스템 v2 + 세부페이지 + 지도 + Why
js/main.js            # 스크롤스파이·리빌·카운트업·검사그리드 렌더
data/exams.json       # 정밀검사 단일 소스(그리드 + 세부페이지)
data/spaces.json      # 공간 단일 소스(그리드 + 세부페이지)
exam/<slug>.html      # 검사 9종 세부페이지 (gen_exams.py)
space/<slug>.html     # 공간 4종 세부페이지 (gen_spaces.py) — 설계원칙 + 실제 평면도
tools/gen_exams.py    # exams.json → 세부페이지: python3 tools/gen_exams.py
tools/gen_spaces.py   # spaces.json → 세부페이지(개념도 강조 포함): python3 tools/gen_spaces.py
tools/conceptmap.py   # 공간 개념도(일러스트 평면도) SVG 생성. clinic_map_svg(highlight)로
                      #   특정 공간 테두리 강조. 실행 시 assets/conceptmap.svg(전체) 출력.
                      #   방↔공간 매핑은 conceptmap.py의 HIGHLIGHT dict에서 수정.
assets/real/          # 실사 (히어로·의료진·방송4·공간3·지도·평면도·로고)
assets/real/equip/    # 정밀검사 장비 실사 9종
이미지/               # 원본 업로드(히어로·방송·프로필·지도 스크린샷) — 소스 보관
```

## 섹션별 특이사항
- **히어로**: 강연 배너(3:2 전체 노출) + 2줄 H1(축소) + 부제 "당신의 심장에게, 평생 주치의를."
- **공간**: 실사 4카드(라운지·접수·진료상담·검사존) → 각 세부페이지에 **설계 원칙 + 실제 4안 평면도**.
  라운지·접수·상담 사진은 Unsplash(무료·상업이용 가능) 연출컷 → 완공 후 실사 교체.
- **지도**: 사용자 제공 **네이버 위성 스크린샷(map.png)** 정적 표시 + 핀 오버레이 + "지도 크게 보기"(네이버지도 링크).
  카카오/구글 라이브 지도로 바꾸려면 `js/main.js`의 지도 자리(주석)에 SDK 초기화 추가.
- **Why**: 하단 다크 섹션 3논리(vs 큰병원 시간·접근성 / vs 큰병원 분절진료 / vs 일반내과 전문성).

## 실사 이미지 맵
| 위치 | 파일 | 출처 |
|---|---|---|
| 히어로 배너 | `assets/real/hero-lecture.png` | 카카오 001 (강연) |
| 의료진 프로필 | `assets/real/doctor-full.png` | seoulheart.com (multiply 블렌드) |
| 방송 5장 | `tv-kbs/sbs/chosun/mbn.png` + hero-lecture(강연) | 카카오 002~005 |
| 정밀검사 9종 | `assets/real/equip/*` | seoulheart.com 진단장비 페이지 |
| 공간 3장 | `space-lounge/reception/consult.jpg` | Unsplash(무료·상업이용) — 완공 후 실사 교체 |
| 공간 세부 평면도 | `assets/real/floorplan.png` | 고도화 4안 평면도(실제 설계) |
| 지도 | `assets/real/map.png` | 사용자 제공 네이버 위성 스크린샷 |

- **홀터=패치(`holter.png`) / 24시간 혈압=반지(`bp.jpg`)** — 원본 스왑 정정 완료.
- 미사용 보관: `logo.png`(실제 CI, 현재 헤더는 인라인 SVG 로고 사용), `profile.png`, `cert-echo.png`, `clinic-wall.jpg`.

## 지도를 라이브로 바꾸려면
현재는 정적 위성 이미지(`map.png`). 카카오/구글 라이브 지도로 교체 시 `js/main.js` 하단
"지도" 주석 위치에 SDK 초기화 추가(카카오는 JavaScript 키 발급·도메인 등록 필요),
`index.html`의 `.map-wrap`을 `<div id="map">` 컨테이너로 되돌리면 됨.

## 콘텐츠 출처
- 약력·진료·장비·주소·교통·주차: seoulheart.com (하트케어내과 공식, 2026-07-26 수집)
- 구조 참고: asanheart.com(섹션 구성만·카피 전량 재작성) · wimclinic.com(원페이지 네비)

## 남은 것 / 주의
- 전화번호: 개원 시 공개(현재 이메일 heartcareclinic@naver.com)
- 공간 실사: 완공 후 `floorplan.png` → 실제 사진 교체, `#space`·푸터의 "계획설계" 고지문 삭제
- 의료광고법: 최상급 표현 배제 카피 유지 권장
- 헤드리스 QA는 창 최소폭 500px 클램프 → 모바일은 iframe(390px) 하네스로 촬영
