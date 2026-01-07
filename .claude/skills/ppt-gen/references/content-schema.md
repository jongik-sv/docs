# Content Template Schema v2.0

콘텐츠 템플릿의 YAML 스키마 정의서입니다. 슬라이드 레이아웃을 재사용 가능한 형태로 저장합니다.

## 스키마 개요

```yaml
content_template:     # 기본 메타데이터
design_meta:          # 디자인 품질/의도 분석
canvas:               # 캔버스 정보 (정규화 기준)
background:           # 슬라이드 배경 (NEW v2.2)
shapes:               # 도형 배열 (상세 정보)
icons:                # 아이콘 정보
gaps:                 # 오브젝트 간 여백
spatial_relationships: # 공간 관계 (벡터화)
groups:               # 그룹 정보
thumbnail:            # 썸네일 경로 (필수)
use_for:              # 사용 가이드
keywords:             # 검색 키워드
expected_prompt:      # 역추론 프롬프트 (NEW v2.1)
prompt_keywords:      # 프롬프트 매칭 키워드 (NEW v2.1)
```

---

## 1. content_template (기본 메타데이터)

```yaml
content_template:
  id: comparison1                      # 고유 ID (영문, 숫자, 하이픈)
  name: "비교 (A vs B)"                 # 표시 이름
  version: "2.0"                       # 스키마 버전
  source: original-file.pptx           # 원본 파일명 (PPT 추출 시)
  source_slide_index: 5                # 원본 슬라이드 인덱스 (0-based)
  source_url: null                     # 원본 URL (웹 추출 시, 선택)
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

## 3.1 slide_zones (슬라이드 영역 정의)

콘텐츠 추출 시 **제외할 영역**을 동적으로 감지합니다. 타이틀, 서브타이틀, 푸터 영역은 문서 템플릿에서 결정되므로 콘텐츠 템플릿에서 제외합니다.

### Zone 구조

```
┌─────────────────────────────────────────┐
│  TITLE ZONE                             │  ← 제외 (동적 감지)
│  - 메인 타이틀 (placeholder: TITLE)      │
├─────────────────────────────────────────┤
│  ACTION TITLE ZONE                      │  ← 제외 (동적 감지)
│  - 서브타이틀, Progress Bar              │
├─────────────────────────────────────────┤
│                                         │
│  CONTENT ZONE                           │  ← 추출 대상
│  - 실제 콘텐츠 영역                       │
│                                         │
├─────────────────────────────────────────┤
│  BOTTOM ZONE                            │  ← 제외 (동적 감지)
│  - Footer, 페이지 번호                   │
└─────────────────────────────────────────┘
```

### 동적 감지 기준

| 영역 | 감지 조건 | Fallback |
|------|----------|----------|
| Title | `placeholder_type in [TITLE, CENTER_TITLE]` OR `name contains 'title'` | 0-10% |
| Action Title | `placeholder_type == SUBTITLE` OR `y < 25% with small height` | 10-20% |
| Content | 타이틀 하단 ~ 푸터 상단 (동적 계산) | 20-92% |
| Bottom | `name contains 'footer/page'` OR `y > 90%` | 92-100% |

### 감지 로직

```python
def is_title_shape(shape, slide_height):
    """타이틀/서브타이틀 도형 판별"""
    # 1. placeholder 타입으로 판별 (가장 정확)
    if shape.placeholder_type in ['TITLE', 'CENTER_TITLE', 'SUBTITLE']:
        return True
    # 2. 이름으로 판별
    name_lower = shape.name.lower()
    if any(kw in name_lower for kw in ['title', 'subtitle', '제목', '타이틀']):
        return True
    # 3. 위치로 판별 (상단 25% 이내 + 높이 15% 미만)
    if shape.y < slide_height * 0.25 and shape.cy < slide_height * 0.15:
        return True
    return False

def is_footer_shape(shape, slide_height):
    """푸터/페이지번호 도형 판별"""
    # 1. 이름으로 판별
    name_lower = shape.name.lower()
    if any(kw in name_lower for kw in ['footer', 'page', 'slide', '페이지', '푸터']):
        return True
    # 2. 위치로 판별 (하단 10% 이내)
    if shape.y > slide_height * 0.90:
        return True
    return False

def detect_content_zone(shapes, slide_height=1080):
    """Content Zone 경계 동적 감지"""
    # 타이틀 도형 찾기
    title_shapes = [s for s in shapes if is_title_shape(s, slide_height)]
    if title_shapes:
        title_bottom = max(s.y + s.cy for s in title_shapes)
        content_top = title_bottom + (slide_height * 0.02)  # 2% 여유
    else:
        content_top = slide_height * 0.20  # Fallback 20%

    # 푸터 도형 찾기
    footer_shapes = [s for s in shapes if is_footer_shape(s, slide_height)]
    if footer_shapes:
        footer_top = min(s.y for s in footer_shapes)
        content_bottom = footer_top - (slide_height * 0.02)  # 2% 여유
    else:
        content_bottom = slide_height * 0.92  # Fallback 92%

    return content_top, content_bottom
```

### 수동 오버라이드 (선택)

특정 슬라이드에서 동적 감지 대신 고정값 사용:

```yaml
zone_overrides:
  content_top: 25%      # 동적 감지 무시, 25% 고정
  content_bottom: 90%   # 동적 감지 무시, 90% 고정
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
      original_aspect_ratio: 6.67 # 원본 비율 (cx_px / cy_px) - 다중 비율 지원용

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
      original_font_size_pt: 24   # 원본 폰트 크기 (pt) - 다중 비율 지원용
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

### picture 타입 추가 필드

이미지 도형에는 설명과 용도를 포함합니다.

```yaml
shapes:
  - id: "image-0"
    name: "Hero Image"
    type: picture
    geometry:
      x: 50%
      y: 0%
      cx: 50%
      cy: 100%

    # 이미지 관련 필드 (picture 타입 전용)
    image:
      source: "path/to/image.jpg"           # 이미지 경로 (선택)
      description: "도시 야경 사진, 고층 빌딩과 조명"  # 이미지 설명 (필수)
      purpose: hero                         # 용도: hero | background | icon | diagram | photo
      alt_text: "서울 도심 야경"              # 접근성용 대체 텍스트 (선택)
      fit: cover                            # 이미지 맞춤: cover | contain | fill | none
      opacity: 1.0                          # 투명도 (0.0~1.0)
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| source | string | No | 이미지 파일 경로 |
| **description** | string | **YES** | 이미지 내용 설명 (LLM이 이해할 수 있는 자연어) |
| purpose | string | No | 용도 분류 (hero, background, icon, diagram, photo) |
| alt_text | string | No | 접근성용 대체 텍스트 |
| fit | string | No | 맞춤 방식 (기본: cover) |
| opacity | number | No | 투명도 (기본: 1.0) |

### image.purpose 분류

| 값 | 설명 | 예시 |
|------|------|------|
| `hero` | 슬라이드 메인 비주얼 | 전면 배경, 큰 이미지 |
| `background` | 배경 이미지 | 흐린 배경, 오버레이 이미지 |
| `icon` | 아이콘성 이미지 | 로고, 심볼 |
| `diagram` | 다이어그램/차트 | 설명 그래픽, 인포그래픽 |
| `photo` | 일반 사진 | 제품 사진, 인물 사진 |

---

## 4.1 background (슬라이드 배경)

슬라이드 전체 배경을 정의합니다. 배경 이미지 사용 시 설명이 필수입니다.

```yaml
background:
  type: image                              # solid | gradient | image

  # type: solid
  color: primary                           # 시맨틱 색상

  # type: gradient
  gradient:
    type: linear                           # linear | radial
    angle: 90                              # 각도 (linear)
    stops:
      - {position: 0%, color: primary}
      - {position: 100%, color: secondary}

  # type: image (배경 이미지)
  image:
    source: "backgrounds/cityscape.jpg"    # 이미지 경로 (선택)
    description: "어두운 도시 야경, 블러 처리된 빌딩 불빛"  # 이미지 설명 (필수)
    fit: cover                             # cover | contain | tile
    opacity: 0.3                           # 투명도 (오버레이용)
    overlay_color: dark_text               # 오버레이 색상 (선택)
    overlay_opacity: 0.5                   # 오버레이 투명도 (선택)
```

### background.image 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| source | string | No | 배경 이미지 파일 경로 |
| **description** | string | **YES** | 배경 이미지 설명 (LLM 생성 시 참조) |
| fit | string | No | 맞춤 방식 (기본: cover) |
| opacity | number | No | 이미지 투명도 (0.0~1.0) |
| overlay_color | string | No | 이미지 위 오버레이 색상 |
| overlay_opacity | number | No | 오버레이 투명도 |

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

### 다중 비율 지원 (Multi-Aspect Ratio)

16:9로 추출한 템플릿을 4:3으로 생성할 때 도형과 폰트 비율 왜곡을 방지합니다.

#### 문제점

% 좌표만 사용하면 비율 변환 시 왜곡 발생:

```
원본 (16:9): 원 → cx: 10%, cy: 10%
├── 16:9로 생성: 원 유지 ✓
└── 4:3로 생성: 타원으로 왜곡 ✗ (4:3 높이가 더 높음)
```

#### 해결책: original_aspect_ratio

모든 도형에 **원본 비율**을 함께 저장:

```yaml
geometry:
  x: 25%
  y: 10%
  cx: 8%
  cy: 14.2%                     # 16:9 기준 %
  original_aspect_ratio: 1.0    # 원본 비율 (width_px / height_px)
                                # 원 = 1.0, 정사각형 = 1.0, 가로 직사각형 > 1.0
```

#### 추출 시 계산 로직

```python
# EMU에서 픽셀로 변환
EMU_PER_INCH = 914400
PX_PER_INCH = 96

shape_width_px = shape_cx_emu / EMU_PER_INCH * PX_PER_INCH
shape_height_px = shape_cy_emu / EMU_PER_INCH * PX_PER_INCH

# 원본 비율 계산
original_aspect_ratio = round(shape_width_px / shape_height_px, 3)
```

#### 생성 시 비율 보정 로직

```python
def calculate_geometry(shape, source_ratio, target_ratio):
    """
    source_ratio: 원본 슬라이드 비율 (16:9 = 1.778)
    target_ratio: 타겟 슬라이드 비율 (4:3 = 1.333)
    """
    geo = shape['geometry']
    original_ar = geo.get('original_aspect_ratio')

    if original_ar:
        # 비율 보정 계수
        ratio_factor = target_ratio / source_ratio  # 4:3 / 16:9 = 0.75

        # 방법 1: cy 조정 (cx 유지)
        target_cy = geo['cy'] * ratio_factor

        # 방법 2: original_aspect_ratio로 직접 계산
        # cx 유지하고 cy를 비율에 맞게 재계산
```

### 폰트 크기 보정 (Font Size Preservation)

`font_size_ratio`만 사용하면 높이 변화에 따라 폰트도 축소:

| 비율 | 높이 | font_size_ratio 0.028 | 결과 |
|------|------|----------------------|------|
| 16:9 | 1080px | 1080 × 0.028 | 30.24pt |
| 4:3 | 810px | 810 × 0.028 | 22.68pt (**25% 축소!**) |

#### 해결책: original_font_size_pt

절대 폰트 크기를 함께 저장:

```yaml
text:
  font_size_ratio: 0.028           # 상대값 (기존 호환)
  original_font_size_pt: 30.24     # 절대값 (신규)
```

#### 생성 시 폰트 크기 결정 로직

```python
def calculate_font_size(text_config, target_height, preserve_absolute=True):
    """
    preserve_absolute=True: 절대값 유지 (권장)
    preserve_absolute=False: 비율 기반 스케일링
    """
    original_pt = text_config.get('original_font_size_pt')
    ratio = text_config.get('font_size_ratio')

    if preserve_absolute and original_pt:
        return original_pt  # 절대값 유지
    elif ratio:
        return target_height * ratio  # 비율 기반
```

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

슬라이드의 독립 아이콘을 정의합니다.

### 필수 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | string | YES | 고유 ID |
| type | string | YES | font-awesome, material, custom |
| icon_name | string | YES | 아이콘 이름 |
| position | object | YES | x, y 좌표 (px, 1980x1080 기준) |
| size | number | **YES*** | 아이콘 크기 (px) |
| size_ratio | number | **YES*** | 캔버스 높이 대비 비율 (0.0~1.0) |
| color | string | YES | 시맨틱 색상 |

\* `size` 또는 `size_ratio` 중 하나는 반드시 지정해야 합니다.

### 선택 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| opacity | number | 투명도 (0.0~1.0, 기본: 1.0) |

```yaml
icons:
  - id: "icon-0"
    type: font-awesome            # font-awesome | material | custom
    icon_name: "fa-chart-bar"     # 아이콘 이름
    position:
      x: 100                      # px (1980 기준)
      y: 300                      # px (1080 기준)
    size: 32                      # REQUIRED: 아이콘 크기 (px)
    # 또는
    size_ratio: 0.03              # 캔버스 높이 대비 비율 (1080 * 0.03 = 32px)
    color: primary                # 시맨틱 색상
    opacity: 1.0                  # 선택
```

### 크기 가이드라인

| 용도 | size (px) | size_ratio | 예시 |
|------|-----------|------------|------|
| 소형 (텍스트 옆) | 16-24 | 0.015-0.022 | 리스트 아이템 아이콘 |
| 중형 (카드 내) | 32-48 | 0.03-0.044 | 피처 카드 아이콘 |
| 대형 (강조) | 64-96 | 0.06-0.09 | 섹션 아이콘 |
| 초대형 (메인) | 128+ | 0.12+ | 메인 비주얼 아이콘 |

---

## 7.1 인라인 아이콘 (shapes 내)

shapes 배열 내에서 아이콘을 포함하는 경우의 스키마입니다.

```yaml
shapes:
  - id: "icon_card_1"
    type: group
    geometry: {x: "5%", y: "20%", cx: "20%", cy: "70%"}
    children:
      - circle_bg: {color: primary, opacity: 0.15}
      - circle_border: {color: primary, width: 3}
      - icon:
          name: "chart-bar"           # REQUIRED: 아이콘 이름
          color: primary              # REQUIRED: 시맨틱 색상
          size: 48                    # REQUIRED: px 단위
          # 또는
          size_ratio: 0.044           # 캔버스 높이 대비 (1080 * 0.044 = 47.5px)
      - title: "제목을 입력하세요."
      - description: "설명 텍스트"
```

### 인라인 아이콘 필수 필드

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name | string | YES | 아이콘 이름 (접두사 없이) |
| color | string | YES | 시맨틱 색상 |
| size | number | **YES*** | 크기 (px) |
| size_ratio | number | **YES*** | 캔버스 높이 대비 비율 |

\* `size` 또는 `size_ratio` 중 하나 필수

### 예시: 올바른 사용 vs 잘못된 사용

```yaml
# BAD - size 정보 없음 (추출 시 거부됨)
- icon: {name: "chart-bar", color: primary}

# GOOD - size 명시
- icon: {name: "chart-bar", color: primary, size: 48}

# GOOD - size_ratio 명시
- icon: {name: "chart-bar", color: primary, size_ratio: 0.044}

# GOOD - 둘 다 명시 (size 우선 적용)
- icon: {name: "chart-bar", color: primary, size: 48, size_ratio: 0.044}
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

# 배경 이미지 예시 (선택)
background:
  type: solid
  color: background
  # type: image인 경우
  # image:
  #   source: "backgrounds/abstract-blue.jpg"
  #   description: "추상적인 파란색 그라데이션 배경, 부드러운 곡선 패턴"
  #   fit: cover
  #   opacity: 0.15
  #   overlay_color: dark_text
  #   overlay_opacity: 0.3

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

expected_prompt: |
  A vs B 비교 슬라이드를 만들어줘.
  - 좌측에 A 항목 (배경색 구분)
  - 우측에 B 항목
  - 중앙에 구분선
  - 각 항목에 제목과 설명
  - 대칭 레이아웃

prompt_keywords:
  - "비교"
  - "vs"
  - "대비"
  - "Before"
  - "After"
  - "As-Is"
  - "To-Be"
```

---

## 13. expected_prompt (역추론 프롬프트) - NEW v2.1

슬라이드 레이아웃을 생성하는 자연어 프롬프트를 역추론하여 저장합니다.

### 목적

1. **템플릿 매칭**: 사용자 요청과 템플릿을 의미적으로 매칭
2. **역참조**: 템플릿이 어떤 요청에 적합한지 문서화
3. **검색 개선**: 키워드 기반 검색 보완

### 스키마

```yaml
expected_prompt: |                    # YAML 블록 스칼라 (|) 사용
  {슬라이드 유형} 슬라이드를 만들어줘.
  - {요소1 설명}
  - {요소2 설명}
  - ...
  - {레이아웃 특징}
```

### 작성 규칙

1. **첫 줄**: `{슬라이드 유형} 슬라이드를 만들어줘.`
2. **요소 설명**: 상단→하단 순서로 각 구성요소 설명
3. **레이아웃 특징**: 대칭, 그리드, 흐름 등 전체 특성

### 요소별 변환 규칙

| 도형 타입 | 프롬프트 표현 |
|----------|--------------|
| `rounded-rectangle` | "라운드 형태의 박스/라벨" |
| `textbox` (TITLE) | "큰 제목 텍스트" |
| `textbox` (BODY) | "설명 텍스트" |
| `group` (N개) | "N개의 카드/열로 구성" |
| `icon` | "아이콘 표시" |
| `dotgrid` | "도트그리드로 퍼센트 표시" |
| `picture` | "이미지/사진 영역" |
| `oval` | "원형 도형" |
| `arrow` | "화살표로 연결" |

### 예시

```yaml
# deepgreen-grid4col1
expected_prompt: |
  기능 소개 슬라이드를 만들어줘.
  - 4개의 카드를 가로로 균등 배치
  - 각 카드: 상단에 라운드 배경 아이콘
  - 아이콘 아래에 제목 텍스트
  - 제목 아래에 설명 텍스트
  - 균등한 간격의 그리드 레이아웃

# deepgreen-process1
expected_prompt: |
  프로세스 슬라이드를 만들어줘.
  - 4단계 원형 프로세스
  - 각 단계는 원 안에 번호 (01, 02, 03, 04)
  - 원 아래에 제목과 설명
  - 화살표로 단계 연결
  - 가로 흐름 레이아웃
```

---

## 14. prompt_keywords (프롬프트 매칭 키워드) - NEW v2.1

템플릿 매칭에 사용되는 키워드 배열입니다.

### 스키마

```yaml
prompt_keywords:
  - "{키워드1}"
  - "{키워드2}"
  - "{키워드3}"
  # 5-7개 권장
```

### 추출 규칙

| 소스 | 추출 방법 |
|------|----------|
| `category` | cover → "표지", toc → "목차" |
| `design_intent` | grid-4col → "4열", "그리드" |
| `shapes[].type` | icon → "아이콘", dotgrid → "도트" |
| `use_for` | 배열 그대로 포함 |
| 레이아웃 분석 | 대칭 → "대칭", N열 → "N열" |

### 매칭 알고리즘

```python
def match_template(user_prompt, templates):
    """사용자 프롬프트와 템플릿 매칭"""
    scores = []
    user_keywords = extract_keywords(user_prompt)

    for template in templates:
        # 1. prompt_keywords 매칭 (0.0 ~ 1.0)
        keyword_matches = len(set(user_keywords) & set(template['prompt_keywords']))
        keyword_score = keyword_matches / len(template['prompt_keywords'])

        # 2. use_for 매칭 (가중치 1.5)
        use_for_matches = sum(1 for u in template['use_for'] if u in user_prompt)
        use_for_score = use_for_matches * 1.5

        # 3. expected_prompt 유사도 (0.0 ~ 1.0)
        prompt_similarity = compute_similarity(user_prompt, template['expected_prompt'])

        total_score = keyword_score + use_for_score + prompt_similarity
        scores.append((template['id'], total_score))

    return sorted(scores, key=lambda x: -x[1])
```

### 예시

```yaml
# deepgreen-cover1
prompt_keywords:
  - "표지"
  - "타이틀"
  - "발표자"
  - "프로젝트"
  - "중앙정렬"
  - "라벨"

# deepgreen-stats1
prompt_keywords:
  - "통계"
  - "퍼센트"
  - "KPI"
  - "지표"
  - "도트"
  - "비율"
```
