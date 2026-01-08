# Content Extraction Rules

콘텐츠 템플릿 추출 시 사용하는 세부 규칙 정의.

---

## 1. Zone Detection 규칙

### 슬라이드 영역 구조

```
┌─────────────────────────────────────────┐
│  TITLE ZONE (0-20%)                     │  ← 제외
│  - placeholder_type: TITLE, CENTER_TITLE │
│  - 메인 타이틀, 서브타이틀                 │
├─────────────────────────────────────────┤
│                                         │
│  CONTENT ZONE (20-92%)                  │  ← 추출 대상
│  - 실제 콘텐츠 영역                       │
│  - shapes[], icons[] 추출               │
│                                         │
├─────────────────────────────────────────┤
│  FOOTER ZONE (92-100%)                  │  ← 제외
│  - 페이지 번호, 저작권 표시               │
└─────────────────────────────────────────┘
```

### 영역 감지 기준

| 영역 | 감지 조건 | Fallback |
|------|----------|----------|
| Title | placeholder_type in [TITLE, CENTER_TITLE, SUBTITLE] | 상단 0-20% |
| Title | name contains 'title', '제목', '타이틀' | |
| Title | y < 25% AND height < 15% | |
| Footer | name contains 'footer', 'page', '페이지', '푸터' | 하단 92-100% |
| Footer | y > 90% | |
| Content | 타이틀 하단 ~ 푸터 상단 | 20-92% |

### 좌표 변환

콘텐츠 영역을 100%로 정규화:

```python
# Content Zone 경계
content_top = 0.20 * canvas_height    # 20%
content_bottom = 0.92 * canvas_height # 92%
content_height = content_bottom - content_top

# 도형 좌표 → Content Zone % 변환
shape_y_percent = (shape_y - content_top) / content_height * 100
```

---

## 2. 도형 추출 규칙

### geometry 추출

```yaml
geometry:
  x: 25%                           # 콘텐츠 영역 기준 %
  y: 10%
  cx: 50%                          # 너비
  cy: 80%                          # 높이
  original_aspect_ratio: 0.625     # 필수: width_px / height_px
```

### style 추출

```yaml
style:
  fill:
    type: solid                    # solid | gradient | none
    color: primary                 # 시맨틱 토큰 우선
    opacity: 1.0

  stroke:
    color: dark_text               # 테두리 색상
    width: 2                       # 두께 (pt)

  shadow:
    enabled: true
    blur: 4
    offset_x: 2
    offset_y: 3
    opacity: 0.15

  rounded_corners: 8               # 모서리 둥글기 (pt)
```

### text 추출

```yaml
text:
  has_text: true
  content: "텍스트 내용"
  placeholder_type: BODY           # TITLE | BODY | SUBTITLE
  alignment: center                # left | center | right
  font_size_ratio: 0.028           # 필수: font_size / canvas_height
  original_font_size_pt: 30.24     # 필수: 원본 폰트 크기
  font_weight: bold                # normal | bold
  font_color: light                # 시맨틱 토큰
```

### icon 추출

```yaml
# 독립 아이콘 (icons[] 배열)
icons:
  - id: "icon-0"
    icon_name: "fa-chart-bar"
    position: {x: 100, y: 300}
    size: 32                       # 필수: size 또는 size_ratio
    color: primary

# 인라인 아이콘 (shapes 내)
- icon:
    name: "chart-bar"
    color: primary
    size: 48                       # 필수
```

---

## 3. SVG 추출 조건

### 복잡 도형 판단 기준

다음 조건에 해당하면 `type: svg` 사용:

| 조건 | 예시 |
|------|------|
| 방사형 세그먼트 (3개+) | cycle-6segment, radial chart |
| 벌집형 레이아웃 | honeycomb process |
| 곡선 화살표/커넥터 | curved arrow cycle |
| 비정형 다각형 | custom polygons |
| 연속된 곡선 경로 | flow diagrams |
| 겹치는 타원/원 | Venn diagrams |

### SVG 생성 가이드

1. **전체 슬라이드 SVG**: 복잡한 다이어그램은 `svg_inline`에 전체 SVG 작성
2. **기준점 설정**: 다이어그램 중심을 명시적으로 설정
3. **Path 명령어**: M(이동), L(직선), C(베지어 곡선), Q(2차 곡선), Z(닫기)
4. **디자인 토큰**: fill, stroke에 시맨틱 색상 사용

### svg_inline 예시

```yaml
svg_inline: |
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540">
    <defs>
      <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#7B68EE"/>
        <stop offset="100%" stop-color="#9370DB"/>
      </linearGradient>
      <filter id="shadow">
        <feDropShadow dx="2" dy="3" stdDeviation="4" flood-opacity="0.15"/>
      </filter>
    </defs>

    <!-- Background -->
    <rect width="960" height="540" fill="#F8F9FA"/>

    <!-- Circular Arrow -->
    <g filter="url(#shadow)">
      <path d="M 340,230 Q 340,150 480,150 Q 620,150 620,230"
            stroke="#7B8FD4" stroke-width="22" fill="none"/>
      <polygon points="608,215 635,245 605,250" fill="#7B8FD4"/>
    </g>
  </svg>
```

---

## 4. 프롬프트 역추론 규칙

### expected_prompt 생성

추출된 shapes 구조를 분석하여 사용자가 요청할 법한 프롬프트를 역추론:

```yaml
expected_prompt: |
  {슬라이드 유형} 슬라이드를 만들어줘.
  - {요소1}: {위치/스타일/용도}
  - {요소2}: {위치/스타일/용도}
  - {전체 레이아웃 특징}
```

### 요소별 변환 규칙

| 도형 타입 | 프롬프트 표현 |
|----------|--------------|
| `rounded-rectangle` (상단) | "상단에 라운드 형태의 라벨/배지" |
| `textbox` (TITLE) | "중앙에 큰 제목 텍스트" |
| `textbox` (BODY) | "본문 설명 텍스트" |
| `group` (N열) | "N개의 카드/열로 구성된 그리드" |
| `icon` | "아이콘과 함께 표시" |
| `line` | "구분선" |
| `picture` | "이미지/사진 영역" |
| `oval` (원형) | "원형 도형/단계 표시" |
| `arrow` | "화살표로 연결/흐름 표현" |
| `svg` (cycle) | "순환 다이어그램/사이클" |
| `svg` (venn) | "벤 다이어그램/겹치는 영역" |

### prompt_keywords 추출

```yaml
prompt_keywords:
  - "{category에서 파생}"      # comparison → "비교"
  - "{design_intent에서 파생}" # grid-4col → "4열", "그리드"
  - "{shapes.type에서 파생}"   # icon → "아이콘"
  - "{레이아웃 분석}"          # 대칭 → "대칭"
  # 5-7개 권장
```
