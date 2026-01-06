# Content Template Extraction Workflow

단일 슬라이드 또는 다중 슬라이드의 레이아웃 패턴을 추출하여 재사용 가능한 콘텐츠 템플릿으로 저장합니다.

## Triggers

- "콘텐츠 추출해줘"
- "이 슬라이드 저장해줘"
- "레이아웃 추출해줘"
- "이 슬라이드 패턴 저장"
- "템플릿 저장해줘"

## Pre-requisites

1. 원본 PPTX 파일 확인
2. 추출 대상 슬라이드 인덱스 확인 (0-based)
3. `templates/contents/templates/` 디렉토리 내 기존 파일 확인 (번호 충돌 방지)

---

## Workflow

### Phase 1: Analysis (전체 분석)

다중 슬라이드 추출 시 먼저 전체 분석을 수행합니다.

```bash
# PPTX 언팩
python ooxml/scripts/unpack.py input.pptx workspace/unpacked

# 전체 슬라이드 목록 확인
ls ppt/slides/

# 기존 템플릿 확인 (번호 충돌 방지)
ls templates/contents/templates/
```

분석 항목:
- **슬라이드별 design_intent 결정** (40개 카테고리)
- **테마 색상 매핑** (`ppt/theme/theme1.xml`)
- **품질 점수 평가** (0-10)

결과물: `workspace/analysis/{source_name}-analysis.yaml` (전체 분석 결과, 선택적)

---

### Phase 2: Individual Extraction (개별 추출)

**CRITICAL**: 각 슬라이드는 반드시 **개별 YAML 파일**로 저장합니다.

#### Step 2.1: Design Intent 결정

슬라이드 분석 후 40개 카테고리 중 적절한 design_intent 선택:

| 대분류 | 세부 카테고리 |
|--------|---------------|
| Cover | cover-centered, cover-banner, cover-split, cover-fullimage |
| TOC | toc-list, toc-grid, toc-visual |
| Section | section-title, section-number, section-image |
| Closing | closing-thankyou, closing-qna, closing-contact |
| Comparison | comparison-2col, comparison-table, pros-cons |
| Matrix | matrix-2x2, matrix-swot, matrix-3x3 |
| Timeline | timeline-horizontal, timeline-vertical, timeline-milestone |
| Roadmap | roadmap-horizontal, roadmap-phases, roadmap-gantt |
| Process | process-linear, process-circle, process-honeycomb, process-pyramid |
| Cycle | cycle-circular, cycle-loop |
| Funnel | funnel-vertical, funnel-horizontal |
| Stats | stats-cards, stats-chart, stats-donut, stats-dotgrid |
| Dashboard | dashboard-kpi, dashboard-overview, dashboard-metrics |
| Table | table-simple, table-comparison, table-pricing |
| Grid | grid-2col, grid-3col, grid-4col, grid-icon |
| Feature | feature-list, feature-icons, feature-benefits |
| Content | content-image-text, content-quote, content-team, content-profile |
| Hierarchy | hierarchy-org, hierarchy-tree, hierarchy-mindmap |
| Agenda | agenda-numbered, agenda-visual |
| Map | map-world, map-region, map-location |

**자동 분류 생성**: 기존에 없으면 `{대분류}-{특징}` 형식 (예: process-5step-arrow)

#### Step 2.2: 파일명 결정

```
파일명 규칙: {design_intent}{번호}.yaml

예시:
- cover1.yaml (첫 번째 표지 - cover-centered 등 대분류 사용 가능)
- cover-banner1.yaml (첫 번째 배너형 표지)
- cover-banner2.yaml (두 번째 배너형 표지)
- process-honeycomb1.yaml (첫 번째 허니콤 프로세스)
- stats-dotgrid1.yaml (첫 번째 도트그리드 통계)
```

**번호 충돌 방지 로직**:
```python
import os
import re

def get_next_number(design_intent: str, templates_dir: str) -> int:
    """기존 파일에서 다음 번호를 찾습니다."""
    pattern = re.compile(rf'^{re.escape(design_intent)}(\d+)\.yaml$')
    existing_numbers = []

    for filename in os.listdir(templates_dir):
        match = pattern.match(filename)
        if match:
            existing_numbers.append(int(match.group(1)))

    return max(existing_numbers, default=0) + 1

# 사용 예시
next_num = get_next_number("process-honeycomb", "templates/contents/templates/")
filename = f"process-honeycomb{next_num}.yaml"  # process-honeycomb1.yaml
```

#### Step 2.3: Zone 경계 동적 감지

**CRITICAL**: 콘텐츠 추출 전 타이틀/푸터 영역을 동적으로 감지하여 제외합니다.

**슬라이드 Zone 구조**:

```
┌─────────────────────────────────────────┐
│  TITLE ZONE                             │  ← 제외
│  - placeholder_type: TITLE/CENTER_TITLE │
├─────────────────────────────────────────┤
│  ACTION TITLE ZONE                      │  ← 제외
│  - placeholder_type: SUBTITLE           │
│  - Progress Bar, 서브타이틀             │
├─────────────────────────────────────────┤
│                                         │
│  CONTENT ZONE                           │  ← 추출 대상
│  - 실제 콘텐츠 영역                       │
│                                         │
├─────────────────────────────────────────┤
│  BOTTOM ZONE                            │  ← 제외
│  - Footer, 페이지 번호                   │
└─────────────────────────────────────────┘
```

**감지 함수**:

```python
def is_title_shape(shape, slide_height):
    """타이틀/서브타이틀 도형 판별"""
    if shape.placeholder_type in ['TITLE', 'CENTER_TITLE', 'SUBTITLE']:
        return True
    name_lower = shape.name.lower()
    if any(kw in name_lower for kw in ['title', 'subtitle', '제목', '타이틀']):
        return True
    # 위치 기반: 상단 25% 이내 + 높이 15% 미만
    if shape.y < slide_height * 0.25 and shape.cy < slide_height * 0.15:
        return True
    return False

def is_footer_shape(shape, slide_height):
    """푸터/페이지번호 도형 판별"""
    name_lower = shape.name.lower()
    if any(kw in name_lower for kw in ['footer', 'page', 'slide', '페이지', '푸터']):
        return True
    # 위치 기반: 하단 10% 이내
    if shape.y > slide_height * 0.90:
        return True
    return False

def detect_content_zone(shapes, slide_height=1080):
    """Content Zone 경계 동적 감지"""
    # 타이틀 도형들의 하단 경계
    title_shapes = [s for s in shapes if is_title_shape(s, slide_height)]
    if title_shapes:
        title_bottom = max(s.y + s.cy for s in title_shapes)
        content_top = title_bottom + (slide_height * 0.02)  # 2% 여유
    else:
        content_top = slide_height * 0.20  # Fallback: 20%

    # 푸터 도형들의 상단 경계
    footer_shapes = [s for s in shapes if is_footer_shape(s, slide_height)]
    if footer_shapes:
        footer_top = min(s.y for s in footer_shapes)
        content_bottom = footer_top - (slide_height * 0.02)  # 2% 여유
    else:
        content_bottom = slide_height * 0.92  # Fallback: 92%

    return content_top, content_bottom
```

**Fallback 경계값** (감지 실패 시):

| Zone | 시작 | 끝 | 비고 |
|------|------|-----|------|
| Title + Action | 0% | 20% | 상단 제외 |
| Content | 20% | 92% | 추출 대상 |
| Bottom | 92% | 100% | 하단 제외 |

#### Step 2.4: 도형 정보 추출 (Zone 필터링 적용)

**CRITICAL**: 동적 감지된 Content Zone 내의 도형만 추출

```python
# 1. 모든 도형 로드
all_shapes = load_shapes_from_xml(slide_xml)

# 2. Zone 경계 감지
content_top, content_bottom = detect_content_zone(all_shapes, slide_height=1080)
print(f"Content Zone: {content_top/1080*100:.1f}% ~ {content_bottom/1080*100:.1f}%")

# 3. 콘텐츠 영역 내 도형만 필터링 (중심점 기준)
shapes_to_extract = []
excluded_shapes = []

for shape in all_shapes:
    shape_center_y = shape.y + (shape.cy / 2)

    if content_top <= shape_center_y <= content_bottom:
        shapes_to_extract.append(shape)
    else:
        excluded_shapes.append(shape)
        zone = "title" if shape_center_y < content_top else "bottom"
        print(f"Excluded: {shape.name} (y={shape.y/1080*100:.1f}%, zone={zone})")
```

**추출 속성** (콘텐츠 영역 % 기준):

- **geometry**: x, y, cx, cy (%), **original_aspect_ratio** (필수)
- **style**: fill, stroke, shadow, rounded_corners
- **text**: placeholder_type, alignment, **font_size_ratio**, **original_font_size_pt** (필수)
- **z_index**: 레이어 순서
- **type**: rectangle, oval, textbox, picture, group, arrow, line

**원본 비율 필수 (다중 비율 지원용)**:

```python
# EMU → 원본 비율 계산
EMU_PER_INCH = 914400
PX_PER_INCH = 96

shape_width_px = shape_cx_emu / EMU_PER_INCH * PX_PER_INCH
shape_height_px = shape_cy_emu / EMU_PER_INCH * PX_PER_INCH

# 모든 도형에 원본 비율 기록
geometry['original_aspect_ratio'] = round(shape_width_px / shape_height_px, 3)
```

**원본 폰트 크기 필수**:

```python
# XML에서 폰트 크기 추출 (hundred-point 단위)
font_size_pt = font_size_hundredths / 100

# 모든 텍스트에 원본 크기 기록
text['original_font_size_pt'] = font_size_pt
text['font_size_ratio'] = font_size_pt / canvas_height_px  # 비율도 함께
```

**아이콘 크기 필수**: 아이콘이 포함된 경우 반드시 `size` 또는 `size_ratio` 기록

```yaml
# GOOD
- icon: {name: "chart-bar", color: primary, size: 48}
- icon: {name: "chart-bar", color: primary, size_ratio: 0.044}

# BAD (size 누락)
- icon: {name: "chart-bar", color: primary}
```

#### Step 2.5: 테마 색상 → 시맨틱 매핑

`ppt/theme/theme1.xml`에서 색상 로드:

| 테마 색상 | 시맨틱 |
|----------|--------|
| dk1 | dark_text |
| lt1 | background |
| dk2 | primary |
| accent1 | secondary |

#### Step 2.6: 개별 YAML 생성

**저장 경로**: `templates/contents/templates/{design_intent}{번호}.yaml`

```yaml
# {design_intent} 콘텐츠 템플릿 v2.0
# 원본: {source_file}:{slide_index}

content_template:
  id: {design_intent}{번호}
  name: "{한글 이름}"
  version: "2.0"
  source: {source_file}
  source_slide_index: {0-based index}
  extracted_at: "{ISO 8601 timestamp}"

design_meta:
  quality_score: {0.0-10.0}
  design_intent: {design_intent}
  design_intents:
    - {primary_intent}
    - {secondary_intent}  # 해당되는 경우
  visual_balance: {symmetric|asymmetric}
  information_density: {low|medium|high}

canvas:
  reference_width: 1980
  reference_height: 1080
  aspect_ratio: "16:9"

shapes:
  - id: "shape-0"
    name: "Shape Name"
    type: rectangle
    z_index: 0
    geometry:
      x: 0%
      y: 0%
      cx: 48%
      cy: 100%
      original_aspect_ratio: 0.48  # REQUIRED: 원본 비율 (width_px / height_px)
    style:
      fill: {type: solid, color: primary, opacity: 1.0}
      stroke: {color: none, width: 0}
      shadow: {enabled: false}
      rounded_corners: 0
    text:
      has_text: true
      placeholder_type: BODY
      alignment: center
      font_size_ratio: 0.028          # REQUIRED
      original_font_size_pt: 30.24    # REQUIRED: 원본 폰트 크기 (pt)
      font_weight: bold
      font_color: light

# 아이콘이 포함된 경우
icons:
  - id: "icon-0"
    type: font-awesome
    icon_name: "fa-chart-bar"
    position: {x: 100, y: 300}
    size: 32                      # REQUIRED: size 또는 size_ratio 필수
    # size_ratio: 0.03            # 또는 캔버스 높이 대비 비율
    color: primary

gaps:
  global: {column_gap: 4%, row_gap: 3%}
  between_shapes: []

spatial_relationships: []

groups: []

thumbnail: thumbnails/{design_intent}{번호}.png  # REQUIRED

use_for: []
keywords: []
```

---

### Phase 3: Thumbnail Generation - MANDATORY

**CRITICAL**: 썸네일 없이 추출을 완료할 수 없습니다.

#### 스크립트 경로

```bash
# 스크립트 위치 (ppt-gen 스킬 내)
SCRIPT_DIR=".claude/skills/ppt-gen/scripts"

# PYTHONPATH 설정 (inventory.py 등 의존 모듈 포함)
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
```

#### 개별 슬라이드 썸네일 생성

```bash
# 개별 슬라이드 썸네일 생성 (0-based index)
cd .claude/skills/ppt-gen && python scripts/thumbnail.py {source}.pptx templates/contents/thumbnails/ --slides {N} --single

# 파일명 변경 (slide-N.png → {design_intent}{번호}.png)
mv templates/contents/thumbnails/slide-{N}.png templates/contents/thumbnails/{design_intent}{번호}.png
```

#### 다중 슬라이드 추출 시

```bash
# 여러 슬라이드 한 번에 추출
cd .claude/skills/ppt-gen && python scripts/thumbnail.py {input}.pptx templates/contents/thumbnails/ --slides 1,2,4,5,6 --single

# 각각 파일명 변경
mv templates/contents/thumbnails/slide-1.png templates/contents/thumbnails/cover-banner1.png
mv templates/contents/thumbnails/slide-2.png templates/contents/thumbnails/toc-list1.png
mv templates/contents/thumbnails/slide-4.png templates/contents/thumbnails/stats-chart1.png
# ...
```

#### 필수 시스템 의존성

| 도구 | 용도 | 설치 |
|------|------|------|
| LibreOffice (`soffice`) | PPTX → PDF 변환 | `apt install libreoffice` / `brew install --cask libreoffice` |
| Poppler (`pdftoppm`) | PDF → 이미지 변환 | `apt install poppler-utils` / `brew install poppler` |

#### 출력 확인

```bash
# 썸네일 존재 확인 (필수)
test -f templates/contents/thumbnails/{design_intent}{번호}.png && echo "Thumbnail OK" || echo "ERROR: Thumbnail missing!"
```

#### 오류 처리

썸네일 생성 실패 시:
1. **LibreOffice 미설치**: `soffice: command not found` → LibreOffice 설치 필요
2. **Poppler 미설치**: `pdftoppm: command not found` → Poppler 설치 필요
3. **파일 경로 오류**: PPTX 파일 경로가 절대 경로인지 확인

---

### Phase 4: Registry Update (레지스트리 업데이트)

`templates/contents/registry.yaml`에 새 템플릿 추가:

```yaml
templates:
  # ... 기존 항목들

  - id: {design_intent}{번호}
    name: {한글 이름}
    file: templates/{design_intent}{번호}.yaml
    category: {대분류}
    description: "{설명}"
    use_for: ["용도1", "용도2"]
```

---

### Phase 5: Validation (검증)

추출 완료 전 **필수 검증**:

```bash
# 1. YAML 파일 존재 확인
test -f templates/contents/templates/{design_intent}{번호}.yaml && echo "YAML OK"

# 2. 썸네일 존재 확인
test -f templates/contents/thumbnails/{design_intent}{번호}.png && echo "Thumbnail OK"

# 3. YAML 문법 검증
python -c "import yaml; yaml.safe_load(open('templates/contents/templates/{design_intent}{번호}.yaml'))"

# 4. 레지스트리 업데이트 확인
grep "{design_intent}{번호}" templates/contents/registry.yaml && echo "Registry OK"
```

---

## Output Checklist

**추출 완료 시 다음 항목이 모두 존재해야 합니다:**

- [ ] `templates/contents/templates/{design_intent}{번호}.yaml` - YAML 파일
- [ ] `templates/contents/thumbnails/{design_intent}{번호}.png` - 썸네일 (1980x1080)
- [ ] `templates/contents/registry.yaml` 업데이트됨

---

## Multi-Slide Extraction Example

```
입력: deep-green-template.pptx (슬라이드 14개)

처리:
1. 슬라이드 0 (로고) → skip: true
2. 슬라이드 1 → cover-banner1.yaml + cover-banner1.png
3. 슬라이드 2 → toc-list1.yaml + toc-list1.png
4. 슬라이드 3 → section-number1.yaml + section-number1.png
5. 슬라이드 4 → stats-chart1.yaml + stats-chart1.png
6. 슬라이드 5 → stats-dotgrid1.yaml + stats-dotgrid1.png
7. 슬라이드 6 → feature-icons1.yaml + feature-icons1.png
8. 슬라이드 7 → matrix-2x21.yaml + matrix-2x21.png
9. 슬라이드 8 → process-honeycomb1.yaml + process-honeycomb1.png
10. 슬라이드 9 → process-linear1.yaml + process-linear1.png
11. 슬라이드 10 → process-circle1.yaml + process-circle1.png
12. 슬라이드 11 → cycle-circular1.yaml + cycle-circular1.png
13. 슬라이드 12 → content-image-text1.yaml + content-image-text1.png
14. 슬라이드 13 → table-comparison1.yaml + table-comparison1.png

출력 구조:
├── templates/contents/templates/
│   ├── cover-banner1.yaml
│   ├── toc-list1.yaml
│   ├── section-number1.yaml
│   ├── stats-chart1.yaml
│   ├── stats-dotgrid1.yaml
│   ├── feature-icons1.yaml
│   ├── matrix-2x21.yaml
│   ├── process-honeycomb1.yaml
│   ├── process-linear1.yaml
│   ├── process-circle1.yaml
│   ├── cycle-circular1.yaml
│   ├── content-image-text1.yaml
│   └── table-comparison1.yaml
├── templates/contents/thumbnails/
│   ├── cover-banner1.png
│   ├── toc-list1.png
│   └── ... (13개 썸네일)
└── templates/contents/registry.yaml (13개 항목 추가)
```

---

## Parallel Extraction (병렬 추출)

다중 슬라이드를 병렬로 추출하여 속도를 높입니다.

### 서브에이전트 기반 병렬 처리

**사용 서브에이전트**:
- `content-slide-extractor`: 단일 슬라이드 YAML + 썸네일 추출
- `image-style-extractor`: 이미지 스타일 분석 (색상, 타이포그래피)

### 워크플로우

#### 0단계: 스킬 기준 경로 설정

```bash
# ppt-gen 스킬 기준 경로
SKILL_DIR=".claude/skills/ppt-gen"

# 모든 경로는 스킬 디렉토리 기준
TEMPLATES_DIR="$SKILL_DIR/templates/contents/templates"
THUMBNAILS_DIR="$SKILL_DIR/templates/contents/thumbnails"
SCRIPTS_DIR="$SKILL_DIR/scripts"
```

#### 1단계: 메인 에이전트가 전체 분석

```bash
# 1. PPTX 언팩
python .claude/skills/ppt-gen/ooxml/scripts/unpack.py input.pptx workspace/unpacked

# 2. 각 슬라이드의 design_intent 사전 결정
slide_intents = {
    1: "cover-banner",
    2: "toc-list",
    3: "section-number",
    # ...
}

# 3. 기존 파일 확인하여 번호 할당
filenames = {
    1: "cover-banner1",
    2: "toc-list1",
    3: "section-number1",
    # ...
}
```

#### 2단계: 병렬 서브에이전트 실행

```python
# 13개 슬라이드 병렬 추출 (슬라이드 0 제외)
task_ids = []

for slide_index in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
    task_id = Task(
        subagent_type="content-slide-extractor",
        prompt=f"""
pptx_path: deep-green-template.pptx
unpacked_dir: workspace/unpacked
slide_index: {slide_index}
design_intent: {slide_intents[slide_index]}
output_filename: {filenames[slide_index]}
source_aspect_ratio: "16:9"
""",
        run_in_background=True,
        model="haiku"
    )
    task_ids.append(task_id)
```

#### 3단계: 결과 수집 및 검증

```python
# 모든 에이전트 결과 수집
results = []
for task_id in task_ids:
    result = TaskOutput(task_id=task_id, block=True)
    results.append(result)

# 실패한 슬라이드 재시도
failed = [r for r in results if r['status'] == 'error']
if failed:
    # 순차 재처리 또는 에러 보고
    pass

# registry.yaml 일괄 업데이트
update_registry(results)
```

### 병렬 추출 시 주의사항

1. **언팩은 순차적으로**: PPTX 언팩은 먼저 완료 후 병렬 추출 시작
2. **파일명 충돌 방지**: 메인 에이전트가 사전에 모든 파일명 할당
3. **썸네일 생성**: 각 서브에이전트가 개별 썸네일 생성
4. **레지스트리 업데이트**: 병렬 완료 후 메인 에이전트가 일괄 업데이트

### 성능 비교

| 방식 | 14슬라이드 예상 시간 |
|------|---------------------|
| 순차 처리 | ~5분 |
| 병렬 처리 (13 에이전트) | ~30초-1분 |

---

## Reference

상세 스키마: [references/content-schema.md](../references/content-schema.md)
