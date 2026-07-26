# -*- coding: utf-8 -*-
"""하트케어내과 공간 개념도(일러스트 평면도) SVG 생성.
알록달록·친근한 top-down 병원 지도. highlight로 특정 공간(그룹)을 테두리 강조.
그룹: consult(진료·상담) exam(정밀검사) lounge(대기) reception(접수) treatment(수액) staff lab misc
"""
FONT = "'Apple SD Gothic Neo','Malgun Gothic',sans-serif"
ZONES = {
    "consult":   ("#DCE7F7", "#6E86B8", "#3B6FB0"),
    "exam":      ("#D2ECE5", "#5FA99B", "#3E8C7C"),
    "treatment": ("#DDEBCF", "#82AE66", "#5E8C46"),
    "lounge":    ("#F7ECD6", "#D8BD86", "#B48A3C"),
    "reception": ("#FBE0DD", "#E4938C", "#D06A62"),
    "staff":     ("#E7E9EC", "#A9AFB8", "#7A7E85"),
    "lab":       ("#E3EDF0", "#7FB0BE", "#4F8494"),
    "misc":      ("#EFEBE3", "#C9BBA0", "#9A917C"),
    "pharmacy":  ("#EDEBF2", "#B4AEC8", "#8079A0"),
}
CANVAS = (1040, 600)
# 실제 4안 배치 반영: 북측(위)=진료실 연속, 중앙=대기 라운지(대), 서/남서=검사 클러스터,
# 동측=수액·약국(별도), 중앙하단=접수·주출입구. (label, x, y, w, h, zone, icon)
ROOMS = [
    # 북측(창가) 진료·상담 + 임상병리 + 직원휴게(북서 코너)
    ("직원휴게실", 44, 54, 150, 122, "staff", "staff"),
    ("진료실 3", 204, 54, 150, 122, "consult", "consult"),
    ("진료실 2", 364, 54, 150, 122, "consult", "consult"),
    ("진료실 1", 524, 54, 150, 122, "consult", "consult"),
    ("임상병리실", 684, 54, 140, 122, "lab", "lab"),
    ("상담실", 834, 54, 162, 122, "consult", "consult"),
    # 중앙: 대기 라운지(대) — 캔버스 중앙. 서측: 심초음파(무창). 동측: 수액·약국
    ("심초음파실", 44, 190, 236, 170, "exam", "bed"),
    ("대기 라운지", 300, 190, 440, 170, "lounge", "lounge"),
    ("주사·수액실", 760, 190, 132, 170, "treatment", "iv"),
    ("약국", 904, 190, 92, 170, "pharmacy", "rx"),
    # 남측: 검사(X-ray·심전도, 서남) + 접수 데스크(중앙, 주출입구 앞) + 편의·화장실
    ("X-ray실", 44, 374, 150, 128, "exam", "xray"),
    ("심전도실", 204, 374, 150, 128, "exam", "ecg"),
    ("접수·수납 데스크", 380, 374, 280, 128, "reception", "desk"),
    ("편의코너", 676, 374, 150, 128, "misc", "kiosk"),
    ("화장실", 836, 374, 160, 128, "misc", "wc"),
]
# 공간 슬러그 → 강조 그룹/방라벨
HIGHLIGHT = {
    "lounge":    {"labels": {"대기 라운지"}},
    "reception": {"labels": {"접수·수납 데스크"}},
    "consult":   {"labels": {"진료실 1", "진료실 2", "진료실 3", "상담실"}},
    "exam-zone": {"labels": {"심초음파실", "X-ray실", "심전도실"}},
}

def _icon(kind, cx, cy, c):
    o = ""
    if kind == "consult":  # 데스크+모니터+의자
        o += f'<rect x="{cx-26}" y="{cy-6}" width="52" height="16" rx="4" fill="{c}" opacity=".85"/>'
        o += f'<rect x="{cx-14}" y="{cy-22}" width="28" height="14" rx="3" fill="{c}"/>'
        o += f'<circle cx="{cx}" cy="{cy+22}" r="9" fill="none" stroke="{c}" stroke-width="3"/>'
    elif kind == "bed":  # 검사베드+모니터
        o += f'<rect x="{cx-30}" y="{cy-2}" width="60" height="22" rx="6" fill="{c}" opacity=".85"/>'
        o += f'<rect x="{cx-30}" y="{cy-10}" width="20" height="12" rx="3" fill="{c}"/>'
        o += f'<rect x="{cx+14}" y="{cy-26}" width="22" height="15" rx="3" fill="none" stroke="{c}" stroke-width="2.5"/>'
    elif kind == "xray":  # X-ray 암+테이블
        o += f'<rect x="{cx-28}" y="{cy+8}" width="56" height="12" rx="4" fill="{c}" opacity=".85"/>'
        o += f'<path d="M{cx-18},{cy+8} V{cy-22} h30" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round"/>'
        o += f'<rect x="{cx+6}" y="{cy-26}" width="18" height="14" rx="3" fill="{c}"/>'
    elif kind == "ecg":  # 심전도 파형
        o += f'<rect x="{cx-26}" y="{cy-16}" width="52" height="34" rx="6" fill="none" stroke="{c}" stroke-width="2.5"/>'
        o += f'<path d="M{cx-20},{cy} h8 l4,-11 l6,20 l4,-9 h12" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
    elif kind == "lab":  # 시험관
        for i,dx in enumerate((-14,0,14)):
            o += f'<rect x="{cx+dx-4}" y="{cy-18}" width="8" height="34" rx="4" fill="none" stroke="{c}" stroke-width="2.2"/>'
            o += f'<rect x="{cx+dx-4}" y="{cy+2}" width="8" height="14" rx="4" fill="{c}" opacity=".8"/>'
    elif kind == "iv":  # 수액 베드 2 + 폴대
        o += f'<rect x="{cx-40}" y="{cy-2}" width="34" height="18" rx="5" fill="{c}" opacity=".85"/>'
        o += f'<rect x="{cx+8}" y="{cy-2}" width="34" height="18" rx="5" fill="{c}" opacity=".85"/>'
        o += f'<path d="M{cx},{cy-26} v14" stroke="{c}" stroke-width="2.5"/><circle cx="{cx}" cy="{cy-28}" r="3.5" fill="{c}"/>'
    elif kind == "desk":  # 접수 카운터 + 하트
        o += f'<rect x="{cx-34}" y="{cy-4}" width="68" height="20" rx="6" fill="{c}" opacity=".85"/>'
        o += f'<path d="M{cx},{cy-10} c0,-6 -9,-9 -9,-2 c0,4 9,10 9,10 c0,0 9,-6 9,-10 c0,-7 -9,-4 -9,2 Z" fill="{c}"/>'
    elif kind == "lounge":  # 소파 2 + 테이블 + 화분
        o += f'<rect x="{cx-64}" y="{cy-6}" width="46" height="20" rx="8" fill="{c}" opacity=".8"/>'
        o += f'<rect x="{cx+18}" y="{cy-6}" width="46" height="20" rx="8" fill="{c}" opacity=".8"/>'
        o += f'<circle cx="{cx}" cy="{cy+4}" r="11" fill="none" stroke="{c}" stroke-width="2.5"/>'
        o += f'<path d="M{cx-52},{cy-24} q-3,-14 6,-20 M{cx-46},{cy-24} q2,-12 -3,-18" fill="none" stroke="#5E8C46" stroke-width="2.5" stroke-linecap="round"/>'
        o += f'<circle cx="{cx+52}" cy="{cy-18}" r="7" fill="#8FBF6E"/>'
    elif kind == "staff":  # 커피
        o += f'<rect x="{cx-14}" y="{cy-8}" width="24" height="20" rx="4" fill="none" stroke="{c}" stroke-width="2.5"/>'
        o += f'<path d="M{cx+10},{cy-4} h6 a5,5 0 0 1 0,10 h-6" fill="none" stroke="{c}" stroke-width="2.5"/>'
        o += f'<path d="M{cx-6},{cy-18} q4,-4 0,-8 M{cx+2},{cy-18} q4,-4 0,-8" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
    elif kind == "kiosk":  # 키오스크
        o += f'<rect x="{cx-13}" y="{cy-20}" width="26" height="34" rx="4" fill="none" stroke="{c}" stroke-width="2.5"/>'
        o += f'<rect x="{cx-8}" y="{cy-15}" width="16" height="14" rx="2" fill="{c}" opacity=".7"/>'
    elif kind == "rx":  # 약국 십자
        o += f'<rect x="{cx-15}" y="{cy-15}" width="30" height="30" rx="7" fill="none" stroke="{c}" stroke-width="2.6"/>'
        o += f'<path d="M{cx},{cy-8} v16 M{cx-8},{cy} h16" stroke="{c}" stroke-width="3.4" stroke-linecap="round"/>'
    elif kind == "wc":  # 화장실
        o += f'<circle cx="{cx-9}" cy="{cy-14}" r="4.5" fill="{c}"/><path d="M{cx-9},{cy-8} v14 M{cx-15},{cy-2} h12 M{cx-9},{cy+6} l-4,10 M{cx-9},{cy+6} l4,10" stroke="{c}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
        o += f'<circle cx="{cx+10}" cy="{cy-14}" r="4.5" fill="{c}"/><path d="M{cx+10},{cy-8} l-6,14 h12 Z M{cx+10},{cy+6} v10" stroke="{c}" stroke-width="2.4" fill="{c}" fill-opacity=".2" stroke-linejoin="round"/>'
    return o

def clinic_map_svg(highlight=None, w=CANVAS[0], h=CANVAS[1]):
    hl = HIGHLIGHT.get(highlight, {}).get("labels", set()) if highlight else set()
    dim = bool(hl)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="하트케어내과 공간 개념도">']
    s.append('<defs>'
             '<filter id="cmShadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1a1c20" flood-opacity="0.10"/></filter>'
             '<filter id="cmGlow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="0" stdDeviation="7" flood-color="#E3120B" flood-opacity="0.45"/></filter>'
             '</defs>')
    # 배경 + 건물 바닥
    s.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#FCFBF9"/>')
    s.append(f'<rect x="24" y="24" width="{w-48}" height="{h-48}" rx="26" fill="#F5F1EA" stroke="#E7E1D6" stroke-width="2"/>')
    # 미세 바닥 도트
    dots = ""
    for gx in range(60, w-40, 60):
        for gy in range(60, h-40, 60):
            dots += f'<circle cx="{gx}" cy="{gy}" r="1.3" fill="#D9D2C4" opacity=".5"/>'
    s.append(dots)
    # 입구
    s.append(f'<rect x="{w//2-46}" y="{h-30}" width="92" height="12" rx="6" fill="#E3120B"/>')
    s.append(f'<text x="{w//2}" y="{h-8}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="800" fill="#C00E12">주 출입구</text>')
    s.append(f'<path d="M{w//2},{h-44} v-14" stroke="#C00E12" stroke-width="2.5" marker-end="url(#ah)"/>')
    s.append('<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto"><path d="M1,1 L4,6 L7,1" fill="none" stroke="#C00E12" stroke-width="1.6"/></marker></defs>')

    for label, x, y, ww, hh, zone, icon in ROOMS:
        fill, stroke, ic = ZONES[zone]
        active = label in hl
        op = 1.0 if (active or not dim) else 0.42
        g = [f'<g opacity="{op}">']
        if active:
            g.append(f'<rect x="{x-6}" y="{y-6}" width="{ww+12}" height="{hh+12}" rx="18" fill="#E3120B" opacity="0.10"/>')
            g.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="14" fill="{fill}" stroke="#E3120B" stroke-width="4" filter="url(#cmGlow)"/>')
        else:
            g.append(f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#cmShadow)"/>')
        g.append(f'<rect x="{x+4}" y="{y+4}" width="{ww-8}" height="{hh-8}" rx="10" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity=".7"/>')
        g.append(_icon(icon, x+ww/2, y+hh/2-4, ic))
        lb_color = "#C00E12" if active else "#33373E"
        lb_weight = "800" if active else "700"
        g.append(f'<text x="{x+ww/2}" y="{y+hh-14}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="{lb_weight}" fill="{lb_color}">{label}</text>')
        g.append('</g>')
        s.append("".join(g))

    # 창문 힌트(북·서측 상단/좌측 얇은 하늘색 띠)
    s.append(f'<rect x="30" y="26" width="{w-60}" height="5" rx="2.5" fill="#8FD3E8" opacity=".7"/>')
    s.append(f'<rect x="26" y="30" width="5" height="{h-140}" rx="2.5" fill="#8FD3E8" opacity=".7"/>')
    s.append('</svg>')
    return "".join(s)

if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.join(root, "assets"), exist_ok=True)
    with open(os.path.join(root, "assets", "conceptmap.svg"), "w", encoding="utf-8") as f:
        f.write(clinic_map_svg(None))
    print("wrote assets/conceptmap.svg")
