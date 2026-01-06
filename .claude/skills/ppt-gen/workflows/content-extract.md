# Content Template Extraction Workflow

단일 슬라이드의 레이아웃 패턴을 추출하여 재사용 가능한 콘텐츠 템플릿으로 저장합니다.

## Triggers

- "콘텐츠 추출해줘"
- "이 슬라이드 저장해줘"
- "레이아웃 추출해줘"
- "이 슬라이드 패턴 저장"

## Workflow

### 1. Select and Analyze Slide

```bash
# PPTX 언팩
python ooxml/scripts/unpack.py input.pptx workspace/unpacked

# 슬라이드 XML 읽기
Read ppt/slides/slide{N}.xml
```

### 2. Extract Shape Information

콘텐츠 영역 % 기준으로 추출:

- **geometry**: x, y, cx, cy (%)
- **style**: fill, stroke, shadow, rounded_corners
- **text**: placeholder_type, alignment, font_size_ratio
- **z_index**: 레이어 순서
- **type**: rectangle, oval, textbox, picture, group, arrow, line

### 3. Theme Color → Semantic Mapping

`ppt/theme/theme1.xml`에서 색상 로드:

| 테마 색상 | 시맨틱 |
|----------|--------|
| dk1 | dark_text |
| lt1 | background |
| dk2 | primary |
| accent1 | secondary |

### 4. Design Analysis (LLM)

분석 항목:
- **design_intent**: 40개 카테고리 중 선택
- **quality_score**: 0-10
- **gaps**: 오브젝트 간 여백
- **spatial_relationships**: 정렬, 분포 정보

### 5. Generate Thumbnail (Required)

```bash
python scripts/thumbnail.py input.pptx output/ --slides {N} --single
```

저장: `templates/contents/thumbnails/{id}.png`

### 6. Save YAML and Update Registry

- `templates/contents/templates/{id}.yaml` 생성
- `templates/contents/registry.yaml` 업데이트

## Design Intent Categories (40)

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

## Output Schema (v2.0)

```yaml
content_template:
  id: comparison-2col-example
  name: "2열 비교"
  version: "2.0"
  source: input.pptx
  source_slide_index: 5

design_meta:
  quality_score: 9.2
  design_intent: comparison-2col
  visual_balance: symmetric
  information_density: medium

canvas:
  reference_width: 1980
  reference_height: 1080
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
      fill: { type: solid, color: primary, opacity: 0.1 }
      shadow: { enabled: false }
    text: { has_text: false }

gaps:
  global: { column_gap: 4%, row_gap: 3% }
  between_shapes:
    - { from: "shape-0", to: "shape-1", direction: horizontal, gap: 4% }

spatial_relationships:
  - { from: "shape-0", to: "shape-1", relationship: adjacent-horizontal, alignment: top }

thumbnail: thumbnails/comparison-2col-example.png
use_for: ["A vs B 비교", "Before/After"]
keywords: ["비교", "vs"]
```

## Reference

상세 스키마: [references/content-schema.md](../references/content-schema.md)
