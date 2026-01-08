# HTML to PowerPoint Workflow

템플릿 없이 새 PPT를 생성합니다. HTML을 PowerPoint로 변환합니다.

> **v3.0 Update**: 테마와 컨텐츠가 분리되었습니다. PPT 생성 시 먼저 테마를 선택합니다.

## Triggers

- "PPT 만들어줘"
- "프레젠테이션 생성해줘"
- "슬라이드 만들어줘"

## Theme Selection (MANDATORY - 테마 선택)

**PPT 생성 시작 전 반드시 테마를 선택해야 합니다.**

### Step T.1: 테마 목록 표시

사용자에게 다음과 같이 테마 목록을 보여줍니다:

```markdown
## 🎨 테마 선택

사용 가능한 테마 목록입니다:

| # | 테마 | 설명 | 주요 색상 |
|---|------|------|----------|
| 1 | **Deep Green** | 자연스럽고 깔끔한 딥그린 테마 | 🟢 #1E5128 / 🟩 #4E9F3D |
| 2 | **Brand New** | 신선하고 깔끔한 스카이블루 테마 | 🔵 #7BA4BC / 🩷 #F5E1DC |
| 3 | **Default** | 중립적인 기본 블루 테마 | 💙 #2563EB / 🩵 #DBEAFE |

> 원하는 테마 번호를 선택하거나, 직접 색상을 지정할 수 있습니다.
> 예: "1번 테마" 또는 "파란색 계열로"
```

### Step T.2: 사용자 응답 처리

**옵션 A: 번호 선택** (1, 2, 3)
```python
theme_id = ["deepgreen", "brandnew", "default"][user_choice - 1]
theme = load_theme(f"C:/project/docs/templates/themes/{theme_id}.yaml")
```

**옵션 B: 커스텀 색상 지정**
사용자가 직접 색상을 지정하면 임시 테마 생성:
```yaml
theme:
  id: custom
  name: "Custom Theme"

colors:
  primary: "{사용자 지정 색상}"
  secondary: "{자동 계산 - 밝은 버전}"
  accent: "{자동 계산 - 보색}"
  background: "#FFFFFF"
  dark_text: "#1F2937"
  light: "#FFFFFF"
```

### Step T.3: 테마 확인

선택된 테마를 확인합니다:
```markdown
✅ **선택된 테마**: Deep Green
- Primary: #1E5128 (진한 녹색)
- Secondary: #4E9F3D (밝은 녹색)
- Accent: #D8E9A8 (연두색)

이 테마로 진행할까요? (Y/n)
```

### Step T.4: 디자인 토큰 해석

선택된 테마의 색상을 컨텐츠 템플릿에 적용합니다:

```python
def resolve_design_tokens(template: dict, theme: dict) -> dict:
    """디자인 토큰을 테마 색상으로 치환"""
    colors = theme['colors']

    def resolve_value(value):
        if isinstance(value, str) and value in colors:
            return colors[value]
        return value

    def walk_and_resolve(obj):
        if isinstance(obj, dict):
            return {k: walk_and_resolve(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [walk_and_resolve(item) for item in obj]
        else:
            return resolve_value(obj)

    return walk_and_resolve(template)
```

**적용 예시**:
```yaml
# 템플릿 원본 (디자인 토큰)
style:
  fill:
    color: primary    # ← 토큰
  text:
    font_color: light # ← 토큰

# 테마 적용 후 (실제 색상)
style:
  fill:
    color: "#1E5128"  # ← Deep Green primary
  text:
    font_color: "#FFFFFF"  # ← light
```

---

## Design Principles

**CRITICAL**: PPT 생성 전 디자인 분석 필수:

1. **주제 고려**: 프레젠테이션 주제, 톤, 분위기
2. **브랜딩 확인**: 회사/조직 언급 시 브랜드 색상 고려
3. **팔레트 매칭**: 주제에 맞는 색상 선택
4. **접근법 설명**: 코드 작성 전 디자인 선택 설명

### Requirements

- 코드 작성 전 디자인 접근법 설명
- 웹 안전 폰트만 사용: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- 명확한 시각적 계층 구조
- 가독성 보장: 충분한 대비, 적절한 텍스트 크기
- 일관성 유지: 패턴, 간격, 시각 언어 반복

### Color Palette Selection

**창의적 색상 선택**:
- 기본값을 넘어 생각하기
- 다양한 각도 고려: 주제, 산업, 분위기, 타겟 오디언스
- 3-5개 색상 구성 (주색 + 보조색 + 강조색)
- 대비 확보: 배경과 텍스트 가독성

**예시 팔레트** (참고용):

| 이름 | 색상 |
|------|------|
| Classic Blue | #1C2833, #2E4053, #AAB7B8, #F4F6F6 |
| Teal & Coral | #5EA8A7, #277884, #FE4447, #FFFFFF |
| Warm Blush | #A49393, #EED6D3, #E8B4B8, #FAF7F2 |
| Black & Gold | #BF9A4A, #000000, #F4F6F6 |
| Forest Green | #191A19, #4E9F3D, #1E5128, #FFFFFF |

## Workflow

### 0. Content Template Search (MANDATORY - DO NOT SKIP)

**중요**: 이 단계를 건너뛰면 안 됩니다. 매칭되는 템플릿이 없는 슬라이드만 직접 디자인합니다.

#### Step 0.1: 슬라이드 목록 작성

콘텐츠를 분석하여 필요한 슬라이드 목록을 먼저 작성합니다:

```markdown
| # | 슬라이드 유형 | 콘텐츠 특성 | 매칭 키워드 |
|---|-------------|------------|-----------|
| 1 | 표지 | 제목, 날짜, 작성자 | cover, 표지 |
| 2 | 목차 | 섹션 리스트 | toc, 목차, 아젠다 |
| 3 | 비교표 | A vs B | comparison, 비교 |
| ... | ... | ... | ... |
```

#### Step 0.2: 레지스트리 로드 및 매칭

```
Read C:/project/docs/templates/contents/registry.yaml
```

> **v3.0**: 템플릿 경로가 `C:/project/docs/templates/`로 변경되었습니다.

**매칭 알고리즘** (우선순위 순서):

1. **use_for 매칭**: 배열에 키워드 포함 여부 (가장 정확)
   - 예: "A vs B 비교" → `use_for: ["A vs B 비교"]` 매칭
2. **prompt_keywords 매칭** (NEW): 사용자 프롬프트에서 키워드 추출하여 매칭
   - 예: "4개 기능 아이콘 그리드" → `prompt_keywords: ["4열", "아이콘", "그리드"]` 매칭
   - 매칭 점수 = 일치 키워드 수 / 전체 키워드 수
3. **expected_prompt 유사도 매칭** (NEW): 의미적 유사도 비교
   - 사용자 요청과 `expected_prompt` 텍스트 비교
   - 슬라이드 요소(아이콘, 열, 그리드 등) 언급 시 가중치
4. **category 매칭**: 대분류 일치
   - 예: cover, toc, comparison, timeline, process, stat-cards
5. **design_intent 매칭**: 세부 레이아웃 일치
   - 예: cover-centered, toc-3col, stats-dotgrid, matrix-2x2
6. **keywords 매칭**: 유사 키워드 검색

**프롬프트 기반 매칭 예시**:

```markdown
사용자 요청: "4개의 핵심 기능을 아이콘과 함께 보여주는 슬라이드"

매칭 분석:
| 템플릿 ID | prompt_keywords | 매칭 키워드 | 점수 |
|----------|-----------------|------------|------|
| deepgreen-grid4col1 | ["기능", "4열", "아이콘", "그리드"] | 기능, 아이콘, 4 | 0.75 |
| feature-grid1 | ["기능", "특징", "그리드", "아이콘"] | 기능, 아이콘 | 0.50 |
| deepgreen-stats1 | ["통계", "퍼센트", "KPI"] | - | 0.00 |

→ deepgreen-grid4col1 선택 (최고 점수)
```

**expected_prompt 참조 예시**:

```yaml
# deepgreen-grid4col1의 expected_prompt
expected_prompt: |
  기능 소개 슬라이드를 만들어줘.
  - 4개의 카드를 가로로 균등 배치
  - 각 카드: 상단에 라운드 배경 아이콘
  - 아이콘 아래에 제목 텍스트
  - 제목 아래에 설명 텍스트
  - 균등한 간격의 그리드 레이아웃

# 사용자 요청과 비교하여 구조적 유사성 확인
```

#### Step 0.3: 매칭 결과 테이블 작성 (필수)

**반드시** 매칭 결과를 테이블로 정리합니다:

```markdown
| # | 슬라이드 | 매칭 템플릿 | 매칭 근거 |
|---|---------|-----------|----------|
| 1 | 표지 | deepgreen-cover1 | use_for: ["표지"] |
| 2 | 목차 | deepgreen-toc1 | category: toc |
| 3 | 섹션 구분 | deepgreen-section1 | category: section |
| 4 | 기대효과 (30%, 99%) | deepgreen-stats1 | use_for: ["퍼센트", "지표"] |
| 5 | 3가지 전략 | deepgreen-grid4col1 | design_intent: grid-4col-icon |
| 6 | 프로세스 | deepgreen-process1 | category: process |
| 7 | 일정 | timeline1 | use_for: ["일정", "마일스톤"] |
| 8 | 비교표 | ❌ 없음 | - |
```

#### Step 0.4: 템플릿 YAML 로드 및 HTML 생성

**매칭된 템플릿이 있는 경우**:

1. `templates/contents/templates/{id}.yaml` 읽기
2. `shapes[]` 구조에서 **shape_source 타입 확인** (v3.1)
3. shape_source 타입별 처리 (아래 참조)
4. % 단위를 pt로 변환 (720pt x 405pt 기준)
5. HTML/CSS로 변환 또는 OOXML 직접 삽입

---

#### Step 0.4.1: Shape Source 기반 렌더링 (v3.1 NEW)

템플릿의 각 shape는 **shape_source** 필드에 따라 다르게 처리됩니다:

**Shape Source 타입별 처리**:

| shape_source | 처리 방식 | 설명 |
|--------------|----------|------|
| `ooxml` | OOXML fragment 직접 사용 | 좌표/색상만 치환 후 slide.xml에 삽입 |
| `svg` | SVG → OOXML 변환 | `<a:custGeom>` path로 변환 |
| `reference` | 참조 대상 로드 | Object 파일에서 OOXML 복사 |
| `html` | HTML → 이미지 변환 | 스크린샷 후 이미지로 삽입 |
| `description` | LLM 생성 또는 HTML 변환 | 자연어 설명 기반 생성 |

**1. OOXML 타입 처리** (`shape_source: ooxml`):

```python
def render_ooxml_shape(shape, theme, target_canvas):
    """OOXML fragment를 직접 재사용"""
    xml = shape['ooxml']['fragment']

    # 1. 좌표 스케일링 (EMU 단위)
    original_emu = shape['ooxml']['emu']
    scale_x = target_canvas['width_emu'] / 12192000  # 원본 16:9 기준
    scale_y = target_canvas['height_emu'] / 6858000

    xml = scale_emu_coordinates(xml, original_emu, scale_x, scale_y)

    # 2. 테마 색상 치환
    if theme.get('apply_colors') and shape.get('style'):
        original_colors = shape['ooxml'].get('colors', {})
        for color_type, original_hex in original_colors.items():
            if original_hex and shape['style'].get('fill', {}).get('color'):
                token = shape['style']['fill']['color']
                new_hex = theme['colors'].get(token, original_hex)
                xml = xml.replace(original_hex.replace('#', ''), new_hex.replace('#', ''))

    return xml

# slide.xml에 직접 삽입
def insert_shape_to_slide(slide_xml, shape_xml):
    """<p:spTree>에 shape 추가"""
    sp_tree = slide_xml.find('.//p:spTree', NS)
    shape_element = etree.fromstring(shape_xml)
    sp_tree.append(shape_element)
```

**2. Reference 타입 처리** (`shape_source: reference`):

```python
def render_reference_shape(shape, theme, target_canvas):
    """Object 파일에서 참조 로드"""
    ref = shape['reference']

    # Object 파일 로드
    object_path = f"templates/contents/{ref['object']}"
    object_yaml = load_yaml(object_path)

    # 컴포넌트들의 OOXML 수집
    result_xml = []
    for component in object_yaml['object']['components']:
        if component.get('shape_source') == 'ooxml':
            xml = component['ooxml']['fragment']

            # 오버라이드 적용 (있는 경우)
            if ref.get('override'):
                xml = apply_overrides(xml, ref['override'], component['id'])

            result_xml.append(xml)

    return result_xml
```

**3. Description 타입 처리** (`shape_source: description`):

```python
def render_description_shape(shape, theme, target_canvas):
    """자연어 설명을 HTML로 변환"""
    desc = shape['description']['text']
    hints = shape['description'].get('hints', {})

    # geometry와 hints를 기반으로 HTML 생성
    geometry = shape['geometry']
    style = shape.get('style', {})

    html = f"""
    <div style="
        position: absolute;
        left: {geometry['x']};
        top: {geometry['y']};
        width: {geometry['cx']};
        height: {geometry['cy']};
        background: {resolve_color(style.get('fill', {}).get('color'), theme)};
        border-radius: {style.get('rounded_corners', 0)}pt;
    ">
        <!-- 설명 기반 콘텐츠 -->
    </div>
    """

    return html
```

**렌더링 흐름도**:

```
템플릿 로드
  │
  ▼
┌─────────────────────────────────────┐
│ shape_source 타입 확인               │
└─────────────────────────────────────┘
  │
  ├── ooxml ──────► OOXML fragment 직접 사용
  │                  ├── 좌표 스케일링
  │                  └── 색상 토큰 치환
  │
  ├── reference ──► Object 파일 로드
  │                  ├── 컴포넌트 OOXML 수집
  │                  └── 오버라이드 적용
  │
  ├── svg ────────► SVG → OOXML 변환
  │                  └── <a:custGeom> 생성
  │
  ├── html ───────► HTML 렌더링 → 이미지
  │                  └── 이미지로 삽입
  │
  └── description ► HTML/CSS 생성
                     └── html2pptx 처리
```

---

**기존 방식 (shape_source가 없는 경우)**:

shape_source 필드가 없는 레거시 템플릿은 기존 방식대로 처리합니다:

1. **이미지 필드** 확인: `type: picture`인 경우 `image.description` 읽기
2. **배경** 확인: `background.type: image`인 경우 `background.image.description` 읽기
3. geometry와 style을 HTML/CSS로 변환

**이미지 설명 활용** (picture 타입):

템플릿의 이미지 설명을 참고하여 적절한 이미지를 선택하거나 생성합니다.

```yaml
# 템플릿 YAML
shapes:
  - id: "hero-image"
    type: picture
    geometry: {x: 50%, y: 0%, cx: 50%, cy: 100%}
    image:
      description: "도시 야경 사진, 고층 빌딩과 조명이 반짝이는 모습"
      purpose: hero
      fit: cover
```

→ HTML 생성 시 이미지 설명에 맞는 이미지를 배치하거나, 설명을 참고하여 유사한 분위기의 이미지 검색/생성

**배경 이미지 활용**:

```yaml
# 템플릿 YAML
background:
  type: image
  image:
    description: "어두운 그라데이션 배경, 미세한 기하학적 패턴"
    fit: cover
    opacity: 0.3
```

→ HTML에서 배경 스타일링 시 설명에 맞는 이미지 또는 유사한 효과 적용

**geometry 변환 공식** (16:9 기준):
- x(pt) = x(%) × 7.2
- y(pt) = y(%) × 4.05
- width(pt) = cx(%) × 7.2
- height(pt) = cy(%) × 4.05

**예시** - deepgreen-cover1.yaml shapes → HTML:

```yaml
# YAML
- id: "label-box"
  geometry: { x: 25%, y: 12%, cx: 50%, cy: 8% }
  style: { fill: { color: primary }, rounded_corners: 25 }
```

```html
<!-- HTML 변환 -->
<div style="position: absolute; left: 180pt; top: 49pt; width: 360pt; height: 32pt;
            background: #1E5128; border-radius: 25pt;">
  <p>라벨 텍스트</p>
</div>
```

#### Step 0.5: 매칭 없는 슬라이드만 직접 디자인

**매칭 결과 테이블에서 ❌ 표시된 슬라이드만** Step 1 (Design Principles)로 진행합니다.

**금지**: 매칭 가능한 템플릿이 있는데 직접 디자인하는 것

---

### 0.6 Asset Recommendation (아이콘/이미지 추천)

템플릿 매칭 후, 슬라이드에 필요한 아이콘과 이미지를 자동 추천합니다.

#### Step 0.6.1: 에셋 필요 파악

매칭된 템플릿의 shapes에서 `type: icon` 또는 `type: picture` 플레이스홀더 확인:

```markdown
| # | Slide | Template | Asset Placeholders |
|---|-------|----------|-------------------|
| 4 | 4대 핵심기능 | grid-4col-icon1 | 4x icon |
| 5 | 제품 소개 | image-text1 | 1x picture |
```

#### Step 0.6.2: 아이콘 선택 (우선순위)

**1단계: react-icons 검색**

콘텐츠 키워드로 `templates/assets/icon-mappings.yaml` 매칭:

```yaml
# icon-mappings.yaml 참조
보안 → fa/FaShieldAlt
속도 → fa/FaBolt
데이터 → fa/FaDatabase
AI → fa/FaBrain
```

**2단계: SVG 직접 생성 (대안)**

react-icons에서 적합한 아이콘을 찾지 못한 경우 간단한 SVG 생성.

**아이콘 래스터라이즈** (테마 색상 적용):

```bash
node scripts/rasterize-icon.js fa/FaShieldAlt "#1E5128" 256 shield.png
node scripts/rasterize-icon.js fa/FaBolt "#1E5128" 256 bolt.png
```

#### Step 0.6.3: 이미지 선택

**1단계: registry.yaml 검색**

기존 에셋에서 태그/키워드 매칭:

```bash
# asset-manager.py 검색
python scripts/asset-manager.py search --tag "AI" --tag "technology"
```

**2단계: 웹 크롤링 (필요 시)**

```bash
python scripts/asset-manager.py crawl "https://example.com/images" --tag "hero"
```

**3단계: 이미지 생성 프롬프트 출력**

매칭되는 이미지가 없으면 외부 서비스용 프롬프트 생성:

```bash
node scripts/image-prompt-generator.js --subject "AI 기술 네트워크" --purpose hero --industry tech
```

출력:
```
Prompt: cinematic wide shot of AI technology network, professional photography,
        dramatic lighting, high contrast, futuristic, digital, blue and purple tones,
        8k resolution, highly detailed

Negative Prompt: text, watermark, logo, low quality, blurry, cartoon, anime
Aspect Ratio: 16:9 (1920x1080)
```

> **Note**: 프롬프트만 생성됨. 이미지 생성은 DALL-E, Midjourney 등 외부 서비스에서 수동 진행.
> (MCP 통한 이미지 생성 모델 연동 미구현)

#### Step 0.6.4: 에셋 추천 테이블 출력 (필수)

**반드시** 에셋 추천 결과를 테이블로 정리:

```markdown
| # | Slide | Type | Keyword | Asset | Source |
|---|-------|------|---------|-------|--------|
| 4-1 | 핵심기능 | icon | 보안 | FaShieldAlt | react-icons |
| 4-2 | 핵심기능 | icon | 속도 | FaBolt | react-icons |
| 4-3 | 핵심기능 | icon | 데이터 | FaDatabase | react-icons |
| 4-4 | 핵심기능 | icon | 자동화 | FaCogs | react-icons |
| 5 | 제품소개 | picture | - | ❌ 프롬프트 생성 | image-prompt |
```

#### Step 0.6.5: HTML에 에셋 삽입

**아이콘 삽입**:
```html
<div class="icon-container">
  <img src="file:///C:/project/docs/workspace/icons/shield.png"
       style="width: 40pt; height: 40pt;">
</div>
```

**이미지 삽입**:
```html
<div class="image-area">
  <img src="file:///C:/project/docs/templates/assets/images/hero-ai.png"
       style="width: 100%; height: 100%; object-fit: cover;">
</div>
```

---

### 1. MANDATORY - Read Full Guide

**반드시** 상세 가이드 전체를 읽으세요:

```
Read .claude/skills/ppt-gen/html2pptx.md (전체 파일)
```

이 가이드에는 다음이 포함됩니다:
- HTML 슬라이드 생성 규칙
- html2pptx.js 라이브러리 사용법
- PptxGenJS API (차트, 테이블, 이미지)
- 색상 규칙 (# 제외)

### 2. Create HTML Slides

각 슬라이드별 HTML 파일 생성:
- 16:9: `width: 720pt; height: 405pt`
- 텍스트는 반드시 `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` 태그 내
- `class="placeholder"`: 차트/테이블 영역
- 그라디언트/아이콘은 PNG로 먼저 래스터라이즈

### 3. Convert to PowerPoint

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';

const { slide, placeholders } = await html2pptx('slide1.html', pptx);

// 차트 추가 (placeholder 영역에)
if (placeholders.length > 0) {
    slide.addChart(pptx.charts.BAR, chartData, placeholders[0]);
}

await pptx.writeFile('output.pptx');
```

### 4. Visual Validation

```bash
python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4
```

썸네일 이미지 검토:
- **텍스트 잘림**: 헤더, 도형, 슬라이드 가장자리에 의한 잘림
- **텍스트 겹침**: 다른 텍스트나 도형과 겹침
- **위치 문제**: 슬라이드 경계나 다른 요소와 너무 가까움
- **대비 문제**: 배경과 텍스트 대비 부족

문제 발견 시 HTML 수정 후 재생성.

## Layout Tips

차트/테이블 포함 슬라이드:
- **2열 레이아웃 (권장)**: 전체 너비 헤더 + 아래 2열 (텍스트 | 차트)
- **전체 슬라이드 레이아웃**: 차트/테이블이 슬라이드 전체 차지
- **절대 세로 스택 금지**: 텍스트 아래 차트/테이블 배치 금지

## Visual Design Options

### Geometric Patterns
- 대각선 섹션 구분선
- 비대칭 열 너비 (30/70, 40/60)
- 90도/270도 회전 텍스트 헤더
- 원형/육각형 이미지 프레임

### Border Treatments
- 한쪽 면만 두꺼운 테두리 (10-20pt)
- 코너 브라켓
- 헤더 밑줄 강조 (3-5pt)

### Typography
- 극단적 크기 대비 (72pt 헤드라인 vs 11pt 본문)
- 대문자 헤더 + 넓은 자간
- Courier New: 데이터/기술 콘텐츠

## Dependencies

이미 설치된 라이브러리:
- pptxgenjs, playwright, sharp
- react-icons, react, react-dom
