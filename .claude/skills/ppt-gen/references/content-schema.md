# Content Template Schema v2.0

콘텐츠 템플릿의 YAML 스키마 정의서입니다. 슬라이드 레이아웃을 재사용 가능한 형태로 저장합니다.

## 스키마 개요

```yaml
content_template:     # 기본 메타데이터
design_meta:          # 디자인 품질/의도 분석
canvas:               # 캔버스 정보 (정규화 기준)
shapes:               # 도형 배열 (상세 정보)
icons:                # 아이콘 정보
gaps:                 # 오브젝트 간 여백
spatial_relationships: # 공간 관계 (벡터화)
groups:               # 그룹 정보
thumbnail:            # 썸네일 경로 (필수)
use_for:              # 사용 가이드
keywords:             # 검색 키워드
```

---

## 1. content_template (기본 메타데이터)

```yaml
content_template:
  id: comparison1                      # 고유 ID (영문, 숫자, 하이픈)
  name: "비교 (A vs B)"                 # 표시 이름
  version: "2.0"                       # 스키마 버전
  source: original-file.pptx           # 원본 파일명
  source_slide_index: 5                # 원본 슬라이드 인덱스 (0-based)
  extracted_at: "2026-01-06T14:30:00"  # 추출 시각 (ISO 8601)
```

---

## 2. design_meta (디자인 메타데이터)

LLM이 분석한 디자인 품질과 의도 정보입니다.

```yaml
design_meta:
  quality_score: 9.2              # LLM 평가 점수 (0.0 ~ 10.0)
  design_intent: Comparison       # 주요 분류 (단일)
  design_intents:                 # 복수 분류 (해당되는 모든 의도)
    - Comparison
    - TwoColumn
  visual_balance: symmetric       # symmetric | asymmetric
  information_density: medium     # low | medium | high
```

### 디자인 의도 분류 체계 (40개 카테고리)

| 대분류 | 세부 카테고리 | 설명 |
|--------|---------------|------|
| **Cover** | cover-centered, cover-banner, cover-split, cover-fullimage | 표지 슬라이드 |
| **TOC** | toc-list, toc-grid, toc-visual | 목차 |
| **Section** | section-title, section-number, section-image | 섹션 구분 |
| **Closing** | closing-thankyou, closing-qna, closing-contact | 마무리 |
| **Comparison** | comparison-2col, comparison-table, pros-cons | 비교 |
| **Matrix** | matrix-2x2, matrix-swot, matrix-3x3 | 매트릭스 |
| **Timeline** | timeline-horizontal, timeline-vertical, timeline-milestone | 타임라인 |
| **Roadmap** | roadmap-horizontal, roadmap-phases, roadmap-gantt | 로드맵 |
| **Process** | process-linear, process-circle, process-honeycomb, process-pyramid | 프로세스 |
| **Cycle** | cycle-circular, cycle-loop | 사이클 |
| **Funnel** | funnel-vertical, funnel-horizontal | 퍼널 |
| **Stats** | stats-cards, stats-chart, stats-donut, stats-dotgrid | 통계 |
| **Dashboard** | dashboard-kpi, dashboard-overview, dashboard-metrics | 대시보드 |
| **Table** | table-simple, table-comparison, table-pricing | 표 |
| **Grid** | grid-2col, grid-3col, grid-4col, grid-icon | 그리드 |
| **Feature** | feature-list, feature-icons, feature-benefits | 기능 소개 |
| **Content** | content-image-text, content-quote, content-team, content-profile | 콘텐츠 |
| **Hierarchy** | hierarchy-org, hierarchy-tree, hierarchy-mindmap | 계층 구조 |
| **Agenda** | agenda-numbered, agenda-visual | 아젠다 |
| **Map** | map-world, map-region, map-location | 지도 |

### 자동 분류 생성

기존 분류에 없는 새로운 패턴 발견 시 `{대분류}-{특징}` 형식으로 자동 생성:

```yaml
# 예시
design_intent: process-5step       # 새로 생성된 카테고리
is_new_category: true
category_description: "5단계 프로세스 흐름도"
```

---

## 3. canvas (캔버스 정보)

좌표 정규화의 기준이 되는 캔버스 정보입니다.

```yaml
canvas:
  reference_width: 1980           # 정규화 기준 너비 (px)
  reference_height: 1080          # 정규화 기준 높이 (px)
  original_width_emu: 12192000    # 원본 너비 (EMU)
  original_height_emu: 6858000    # 원본 높이 (EMU)
  aspect_ratio: "16:9"            # 화면 비율
```

---

## 4. shapes (도형 배열)

슬라이드의 모든 도형을 상세히 기술합니다.

```yaml
shapes:
  - id: "shape-0"                 # 고유 ID
    name: "Header Bar"            # 이름 (원본에서 추출)
    type: rectangle               # 도형 유형 (아래 참조)
    z_index: 0                    # 레이어 순서 (0 = 최하단)

    geometry:                     # 위치/크기 정보
      # 콘텐츠 영역 기준 % (권장)
      x: 0%                       # 왼쪽 위치
      y: 0%                       # 상단 위치
      cx: 100%                    # 너비
      cy: 15%                     # 높이
      rotation: 0                 # 회전 각도 (도)

      # 또는 그리드 기반 (선택적)
      # grid: "col-1-12 row-1-1"  # 12컬럼 기준

    style:                        # 스타일 정보
      fill:
        type: solid               # solid | gradient | none
        color: primary            # 시맨틱 색상
        opacity: 1.0              # 0.0 ~ 1.0
      stroke:
        color: none               # 테두리 색상
        width: 0                  # 테두리 두께 (pt)
      shadow:
        enabled: false
        blur: 4                   # 블러 반경
        offset_x: 2               # X 오프셋
        offset_y: 2               # Y 오프셋
        opacity: 0.3              # 그림자 투명도
      rounded_corners: 0          # 모서리 둥글기 (pt)

    text:                         # 텍스트 정보 (있는 경우)
      has_text: true
      placeholder_type: TITLE     # TITLE | BODY | SUBTITLE | etc.
      alignment: center           # left | center | right
      font_size_ratio: 0.022      # 캔버스 높이 대비 비율
      font_weight: bold           # normal | bold
      font_color: light           # 시맨틱 색상
```

### 도형 유형 (type)

| 유형 | 설명 |
|------|------|
| `rectangle` | 사각형 |
| `oval` | 타원/원 |
| `textbox` | 텍스트 상자 |
| `picture` | 이미지 |
| `group` | 그룹 |
| `arrow` | 화살표 |
| `line` | 선 |
| `chevron` | 쉐브론 |
| `callout` | 콜아웃 |
| `connector` | 연결선 |

---

## 5. 좌표 시스템

### 콘텐츠 영역 % 기준 (기본)

타이틀과 여백을 제외한 **콘텐츠 영역**을 100%로 간주합니다.

```
┌─────────────────────────────────────────┐
│  margin_top (5%)                        │
│  ┌───────────────────────────────────┐  │
│  │  TITLE AREA (15%)                 │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │     CONTENT AREA (100% 기준)      │  │
│  │     x: 0-100%, y: 0-100%          │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│  margin_bottom (5%)                     │
└─────────────────────────────────────────┘
     margin_left (3%)    margin_right (3%)
```

### 좌표 변환 공식

```python
# 콘텐츠 영역 정의
content_bounds = {
    "left": 0.03,      # 슬라이드 너비의 3%
    "right": 0.97,     # 슬라이드 너비의 97%
    "top": 0.20,       # 타이틀 영역 아래 (20%)
    "bottom": 0.95     # 하단 여백 위 (95%)
}

# EMU → 콘텐츠 영역 % 변환
content_width = slide_width * 0.94   # (97% - 3%)
content_height = slide_height * 0.75  # (95% - 20%)
content_left = slide_width * 0.03
content_top = slide_height * 0.20

x_percent = (shape_x - content_left) / content_width * 100
y_percent = (shape_y - content_top) / content_height * 100
cx_percent = shape_width / content_width * 100
cy_percent = shape_height / content_height * 100
```

### 12컬럼 그리드 시스템 (대안)

Bootstrap 스타일의 그리드 레이아웃:

```yaml
geometry:
  grid: "col-1-6 row-1-3"   # col-{start}-{span} row-{start}-{span}

# 해석: 1번 컬럼부터 6칸, 1번 행부터 3행
```

| 분할 | 컬럼 설정 |
|------|----------|
| 2분할 | col-6 (50%) |
| 3분할 | col-4 (33.3%) |
| 4분할 | col-3 (25%) |

---

## 6. 시맨틱 색상

테마 독립적인 색상 표현으로 다른 테마에서도 재사용 가능합니다.

| 시맨틱 | Office 테마 색상 | 용도 |
|--------|-----------------|------|
| `primary` | dk2 | 주 강조색 |
| `secondary` | accent1 | 보조 강조색 |
| `accent` | accent1~6 | 포인트 색상 |
| `background` | lt1 | 배경 |
| `dark_text` | dk1 | 어두운 텍스트 |
| `light` | lt1 또는 white | 밝은 요소 |
| `gray` | lt2 | 회색 요소 |

---

## 7. icons (아이콘 정보)

```yaml
icons:
  - id: "icon-0"
    type: font-awesome            # font-awesome | material | custom
    icon_name: "fa-check"         # 아이콘 이름
    position:
      x: 100                      # px (1980 기준)
      y: 300                      # px (1080 기준)
    size: 32                      # 아이콘 크기 (px)
    color: secondary              # 시맨틱 색상
```

---

## 8. gaps (여백 정보)

오브젝트 간 간격을 정의합니다.

```yaml
gaps:
  # 전역 여백 패턴
  global:
    column_gap: 4%          # 열 간 기본 간격
    row_gap: 3%             # 행 간 기본 간격
    item_gap: 2%            # 아이템 간 간격

  # 개별 여백 (shape 간)
  between_shapes:
    - from: "shape-1"
      to: "shape-2"
      direction: horizontal  # horizontal | vertical
      gap: 4%               # 콘텐츠 영역 대비 %

    - from: "shape-0"
      to: "shape-1"
      direction: vertical
      gap: 2%
```

---

## 9. spatial_relationships (공간 관계)

정렬, 분포 등 도형 간 관계를 벡터화합니다.

```yaml
spatial_relationships:
  # 인접 관계
  - from: "shape-1"
    to: "shape-2"
    relationship: adjacent-horizontal  # 수평 인접
    gap: 4%
    alignment: top          # top | center | bottom

  # 균등 분포
  - shapes: ["shape-1", "shape-2", "shape-3"]
    relationship: distributed-horizontal
    total_gap: 8%           # 총 여백

  # 정렬 관계
  - shapes: ["shape-1", "shape-2"]
    relationship: aligned-top
```

### 관계 유형

| 관계 | 설명 |
|------|------|
| `adjacent-horizontal` | 수평 인접 |
| `adjacent-vertical` | 수직 인접 |
| `aligned-top` | 상단 정렬 |
| `aligned-center` | 중앙 정렬 |
| `aligned-bottom` | 하단 정렬 |
| `aligned-left` | 좌측 정렬 |
| `aligned-right` | 우측 정렬 |
| `distributed-horizontal` | 수평 균등 분포 |
| `distributed-vertical` | 수직 균등 분포 |

---

## 10. groups (그룹 정보)

논리적으로 묶인 도형 그룹을 정의합니다.

```yaml
groups:
  - id: "group-left"
    members: ["shape-1", "shape-2", "shape-4"]
    bounding_box:
      x: 0%
      y: 0%
      cx: 48%
      cy: 100%
    internal_gap: 2%        # 그룹 내부 요소 간 간격
```

---

## 11. thumbnail (썸네일)

**필수 항목**입니다. 콘텐츠 추출 시 반드시 생성됩니다.

```yaml
thumbnail: thumbnails/comparison1.png
```

생성 명령:
```bash
python scripts/thumbnail.py input.pptx output/ --slides 5 --single
```

---

## 12. 사용 가이드

```yaml
use_for:                    # 권장 용도
  - "A vs B 비교"
  - "Before/After"
  - "장단점 비교"

keywords:                   # 검색 키워드
  - "비교"
  - "vs"
  - "대비"
  - "양쪽"
```

---

## 전체 예시

```yaml
content_template:
  id: comparison1
  name: "비교 (A vs B)"
  version: "2.0"
  source: marketing-deck.pptx
  source_slide_index: 5
  extracted_at: "2026-01-06T14:30:00"

design_meta:
  quality_score: 9.2
  design_intent: comparison-2col
  design_intents: [comparison-2col, grid-2col]
  visual_balance: symmetric
  information_density: medium

canvas:
  reference_width: 1980
  reference_height: 1080
  original_width_emu: 12192000
  original_height_emu: 6858000
  aspect_ratio: "16:9"

shapes:
  - id: "shape-0"
    name: "Left Panel"
    type: rectangle
    z_index: 0
    geometry:
      x: 0%
      y: 0%
      cx: 48%
      cy: 100%
    style:
      fill:
        type: solid
        color: primary
        opacity: 1.0
      stroke:
        color: none
        width: 0
      shadow:
        enabled: false
      rounded_corners: 0
    text:
      has_text: false

  - id: "shape-1"
    name: "Right Panel"
    type: rectangle
    z_index: 0
    geometry:
      x: 52%
      y: 0%
      cx: 48%
      cy: 100%
    style:
      fill:
        type: solid
        color: secondary
        opacity: 1.0
      stroke:
        color: none
        width: 0
      shadow:
        enabled: false
      rounded_corners: 0

gaps:
  global:
    column_gap: 4%
    row_gap: 3%
  between_shapes:
    - from: "shape-0"
      to: "shape-1"
      direction: horizontal
      gap: 4%

spatial_relationships:
  - from: "shape-0"
    to: "shape-1"
    relationship: adjacent-horizontal
    gap: 4%
    alignment: top

groups:
  - id: "comparison-group"
    members: ["shape-0", "shape-1"]
    bounding_box:
      x: 0%
      y: 0%
      cx: 100%
      cy: 100%

thumbnail: thumbnails/comparison1.png

use_for:
  - "A vs B 비교"
  - "Before/After"

keywords:
  - "비교"
  - "vs"
```
