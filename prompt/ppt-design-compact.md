## PPT Design (Compact)

고품질 PPTX 생성을 위한 완전 독립형 가이드. Apple/Stripe 스타일 디자인.

### 설정
- AskUserQuestion으로 발표 대상/핵심 섹션 확인
- 기본: light 테마, --ultrathink 모드
- 템플릿: PPT기본양식.pptx

---

### 레이아웃

| ID | 용도 | placeholders |
|----|------|-------------|
| 1 | 표지 | title, subtitle |
| 2 | 목차 | toc_items: [{number, title, page}] |
| 3 | 본문(불릿) | main_title, action_title, body: [{level, text}] |
| 4 | 본문(자유) | main_title, action_title + custom_elements |
| 5 | 본문(넓은) | main_title, body (action_title 없음) |

**선택 기준**: 불릿→3, 차트/다이어그램/카드→4, 넓은 본문→5

---

### JSON 구조

```json
{
  "presentation": {
    "title": "제목",
    "theme": "light",
    "template_path": "PPT기본양식.pptx",
    "color_scheme": {
      "primary": "#002452",
      "secondary": "#C51F2A",
      "accent": ["#4B6580", "#E9B86E", "#2E7D32"],
      "background": "#FFFFFF",
      "text": "#333333"
    },
    "slides": [...]
  }
}
```

---

### custom_elements 스키마

#### chart
```json
{"type":"chart","chart_type":"bar|line|pie|donut|area|radar",
 "data":{"labels":["A","B"],"series":[{"name":"S1","values":[10,20],"color":"#002452"}],
 "show_legend":true,"show_data_labels":true}}
```

#### table
```json
{"type":"table","data":{"headers":["H1","H2"],"rows":[["R1C1","R1C2"]],
 "header_style":{"background":"#002452","color":"#FFFFFF"}}}
```

#### icon_box_grid
```json
{"type":"icon_box_grid","data":{"columns":3|4,
 "items":[{"icon":"Material아이콘명","title":"제목","desc":"설명","color":"#002452"}]}}
```

#### kpi_cards
```json
{"type":"kpi_cards","data":{"columns":3|4,
 "items":[{"icon":"trending_up","label":"라벨","value":"85%","sub_value":"전월+5%","trend":"up|down"}]}}
```

#### process_flow
```json
{"type":"process_flow","data":{"direction":"horizontal|vertical",
 "nodes":[{"id":"n1","label":"단계1","description":"설명","shape":"circle|rectangle|diamond"}],
 "edges":[{"from":"n1","to":"n2","label":"다음"}]}}
```

#### org_chart
```json
{"type":"org_chart","data":{"root":{"role":"CEO","name":"홍길동","department":"경영진",
 "children":[{"role":"CTO","name":"김철수","children":[...]}]}}}
```

#### gantt_timeline
```json
{"type":"gantt_timeline","data":{"start_date":"2025-01","end_date":"2025-12",
 "phases":[{"name":"분석","start":"2025-01-01","end":"2025-02-28","color":"#002452"}],
 "milestones":[{"name":"M1","date":"2025-01-15"}]}}
```

#### before_after_comparison
```json
{"type":"before_after_comparison","data":{
 "before":{"title":"As-Is","items":[{"icon":"warning","text":"문제점"}]},
 "after":{"title":"To-Be","items":[{"icon":"check_circle","text":"개선점"}]},
 "metrics":[{"label":"효율","before":"60%","after":"90%","improvement":"+50%"}]}}
```

#### diagram
```json
{"type":"diagram","diagram_type":"architecture|network|venn|hierarchy|cycle",
 "data":{"layers":[{"name":"Frontend","items":["Vue.js"],"color":"#42B883"}],
 "nodes":[{"id":"n1","label":"노드","icon":"server"}],
 "connections":[{"from":"n1","to":"n2","style":"solid|dashed"}]}}
```

#### risk_matrix
```json
{"type":"risk_matrix","data":{
 "axes":{"x":{"label":"발생확률","levels":["낮음","중간","높음"]},
        "y":{"label":"영향도","levels":["낮음","중간","높음"]}},
 "risks":[{"name":"위험1","x":2,"y":2,"mitigation":"대응방안","owner":"담당자"}]}}
```

#### dual_section
```json
{"type":"dual_section","data":{"layout":"50:50|40:60|60:40",
 "left":{"title":"왼쪽","items":[...]},
 "right":{"title":"오른쪽","items":[...]}}}
```

#### screen_gallery
```json
{"type":"screen_gallery","data":{"layout":"horizontal_3|horizontal_3_wide",
 "screens":[{"image_path":"/path/img.png","label":"라벨","description":"설명"}]}}
```

#### illustration (AI 이미지 필요)
```json
{"type":"illustration","data":{"position":"center|left|right","size":"full_width|half"}}
```

---

### 시각화 변환 규칙

| 원본 | → 변환 |
|-----|--------|
| 숫자 비교 | chart (bar/grouped_bar) |
| 추이/변화 | chart (line/area) |
| 비율/구성 | chart (pie/donut) |
| As-Is/To-Be | before_after_comparison |
| 순차 단계 | process_flow |
| 시간 기반 | gantt_timeline |
| KPI 수치 | kpi_cards |
| 기능 나열 | icon_box_grid |
| 조직/계층 | org_chart / diagram(hierarchy) |
| 위험 분석 | risk_matrix |
| 좌우 비교 | dual_section |
| 시스템 구조 | diagram (architecture) |

**필수**: 3줄 이상 불릿 → 시각 요소 변환. ASCII Art → 전문 다이어그램.

---

### 디자인 규칙

**타이포그래피**
- 메인 제목: 36-44pt Bold
- 액션 타이틀: 28-32pt Regular
- 본문: 24-28pt, 줄간격 1.3-1.5배
- 폰트 2종 이내, Sans-serif (본고딕, Pretendard)

**색상 (Light)**
| 용도 | 색상 |
|-----|------|
| Primary | #002452 (네이비) - 신뢰, 전문성 |
| Secondary | #C51F2A (레드) - 강조, CTA |
| Accent | #4B6580, #E9B86E, #2E7D32 |
| Background | #FFFFFF |
| Text | #333333 (기본), #666666 (보조) |

**색상 (Dark)**
| 용도 | 색상 |
|-----|------|
| Primary | #4A90D9 |
| Secondary | #FF6B6B |
| Background | #1A1A2E |
| Text | #E8E8E8 |

**레이아웃**
- 여백: 최소 5% 마진
- 요소 간격: 24px 또는 32px
- 슬라이드당 핵심 아이디어 1개
- 불릿 최대 4개

**차트 규칙**
- Bar Y축: 0에서 시작
- Pie: 5개 이하 항목
- 3D 차트 금지
- 데이터 직접 레이블링 권장

**접근성**
- 텍스트 대비율: 24pt 미만 4.5:1, 이상 3:1
- 색상만으로 정보 구분 금지 (패턴/아이콘 병행)

---

### design_prompt 구조

```json
{
  "design_prompt": {
    "concept": "디자인 컨셉 한 문장",
    "layout": {"grid": "4열 균등", "spacing": "24px"},
    "card_style": {"background": "#FFFFFF", "border": "좌측 4px accent", "border_radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.08)"},
    "icon_style": {"size": "48px", "style": "Material Icons Outlined"},
    "typography": {"title": "Bold 16pt #002452", "desc": "Regular 12pt #666666"}
  }
}
```

---

### image_generation_prompt (AI 이미지 필요 시만)

**사용 조건**
- illustration 타입 사용 시
- 카드 채움률 < 50% → card_image_prompt
- 페이지 여백 > 40% → fill_image_prompt

**불필요한 경우**: chart, table, icon_box_grid, process_flow, org_chart, gantt_timeline, screen_gallery(이미지 있음)

```json
{
  "image_generation_prompt": {
    "main_visual": {
      "prompt": "영문 프롬프트, with Korean text labels",
      "style": "flat design|isometric|photorealistic",
      "size": "1920x1080",
      "negative_prompt": "3D, English text"
    }
  }
}
```

---

### 프롬프트 선택 가이드

| 상황 | design_prompt | image_generation_prompt |
|-----|---------------|------------------------|
| chart/table/카드/flow | O 필수 | X 불필요 |
| screen_gallery(이미지有) | O 필수 | X 불필요 |
| illustration | O 필수 | O 필수 |
| 카드 채움률<50% | O 필수 | card_image_prompt |
| 페이지 여백>40% | O 필수 | fill_image_prompt |

---

### 완전한 슬라이드 예시

```json
{
  "slide_number": 3,
  "layout_id": 4,
  "placeholders": {
    "main_title": "1. 핵심 기능",
    "action_title": "4가지 핵심 기능으로 업무 효율을 극대화합니다."
  },
  "custom_elements": [{
    "type": "icon_box_grid",
    "data": {
      "columns": 4,
      "items": [
        {"icon": "qr_code", "title": "QR 스캔", "desc": "현장 스캔으로 즉시 신고"},
        {"icon": "sync", "title": "실시간 추적", "desc": "전 과정 모니터링"},
        {"icon": "analytics", "title": "데이터 분석", "desc": "통계 대시보드"},
        {"icon": "notifications", "title": "자동 알림", "desc": "카카오톡 연동"}
      ]
    }
  }],
  "design_prompt": {
    "concept": "Premium Feature Cards",
    "layout": {"grid": "4열 균등", "card_size": "200x180px", "spacing": "24px"},
    "card_style": {"background": "#FFFFFF", "border": "좌측 4px accent bar", "border_radius": "8px", "shadow": "0 4px 12px rgba(0,0,0,0.08)"},
    "icon_style": {"size": "48px", "style": "Material Icons Outlined"},
    "typography": {"title": "Bold 16pt #002452", "desc": "Regular 12pt #666666"}
  }
}
```

---

### 워크플로우

```
1. AskUserQuestion → 발표 대상, 핵심 섹션 확인
2. JSON 생성 → 슬라이드 구조화, custom_elements 정의
3. design_prompt 작성 → 각 슬라이드 스타일 지정
4. PPTX 렌더링 → python-pptx로 변환
```

---

### 품질 체크리스트

- [ ] 슬라이드당 핵심 메시지 1개
- [ ] 3줄 이상 불릿 → 시각 요소 변환
- [ ] action_title: 1-2문장 핵심 요약
- [ ] 색상 일관성 (primary/secondary/accent)
- [ ] 여백 최소 5% 유지
- [ ] 폰트 2종 이내
