# JSON 기반 PPT 생성 명령어

입력된 JSON 파일을 기반으로 PPT기본양식.pptx 템플릿을 사용하여 고품질 프레젠테이션을 생성합니다.

## 사용법

```
/generate-ppt-from-json <json_file_path>
```

## 필수 참조 파일

- **템플릿**: `.claude/includes/PPT기본양식.pptx`
- **분석보고서**: `.claude/includes/PPT기본양식_분석보고서.md`

---

## 1. 슬라이드 맵핑 규칙

JSON의 `slide_number`와 PPT의 슬라이드 마스터는 1:1 대응:
- `slide_number: 1` → PPT Slide마스터 layout 1
- `slide_number: N` → PPT Slide마스터 layout N

---

## 2. JSON → Placeholder 맵핑 (idx 기반)

**중요**: `shape_id`는 슬라이드마다 동적으로 할당되어 불안정합니다.
`placeholder_format.idx`를 사용하여 안정적으로 접근합니다.

### 전체 맵핑 테이블

| Layout | JSON 필드 | Placeholder idx | 타입 | 설명 |
|--------|-----------|-----------------|------|------|
| 1 | `title` | **TITLE type** | title | 표지 제목 |
| 1 | `subtitle` | **idx=13** | body | 부제목/작성자 |
| 2 | `toc_items[].number` | **idx=17** | body | 번호 열 (줄바꿈 구분) |
| 2 | `toc_items[].title` | **idx=13** | body | 목차 제목 열 |
| 2 | `toc_items[].pages` | **idx=14** | body | 페이지 번호 열 |
| 3,4,5 | `main_title` | **idx=19** | body | 메인 제목 |
| 3,4 | `action_title` | **TITLE type** | title | 액션 타이틀 |
| 3,5 | `body` | **idx=18** | body | 본문 내용 |

### 공통 요소 (모든 내지)
| 요소 | Placeholder idx | 타입 |
|------|-----------------|------|
| 슬라이드 번호 | idx=4 | sldNum |
| 바닥글 | idx=3 | ftr |

---

## 3. 생성 워크플로우

### Step 1: 이미지 생성 (SVG → PNG)

`image_generation_prompt`를 사용하여 SVG 이미지 생성 후 PNG 변환:

```python
import cairosvg

# 1-1. image_generation_prompt로 SVG 코드 생성
svg_content = generate_svg_from_prompt(slide['image_generation_prompt'])

# 1-2. SVG 파일 저장
svg_path = f"temp/slide_{slide_number}_image.svg"
with open(svg_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

# 1-3. SVG → PNG 변환
png_path = f"temp/slide_{slide_number}_image.png"
cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2.0)
```

### Step 2: 템플릿 복사 및 슬라이드 생성

**중요**: 템플릿을 복사하고 기존 슬라이드를 모두 삭제한 후 새 슬라이드 추가

```python
from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER
import shutil
import os

# 2-1. 템플릿 복사 (원본 보존)
template_path = '.claude/includes/PPT기본양식.pptx'
output_path = f"temp/{presentation['title']}.pptx"
os.makedirs('temp', exist_ok=True)
shutil.copy(template_path, output_path)

# 2-2. 복사본 열기
prs = Presentation(output_path)

# 2-3. 기존 슬라이드 모두 삭제
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# 2-4. 헬퍼 함수 정의
def get_placeholder_by_idx(slide, idx):
    """placeholder idx로 shape 찾기"""
    for shape in slide.shapes:
        if shape.is_placeholder:
            ph = shape.placeholder_format
            if ph.idx == idx:
                return shape
    return None

def get_title_placeholder(slide):
    """TITLE 타입 placeholder 찾기"""
    for shape in slide.shapes:
        if shape.is_placeholder:
            ph = shape.placeholder_format
            if ph.type == PP_PLACEHOLDER.TITLE:
                return shape
    return None

# 2-5. JSON 순서대로 새 슬라이드 추가 및 값 대입
for slide_data in presentation['slides']:
    layout_id = slide_data['layout_id']
    layout = prs.slide_layouts[layout_id - 1]  # 0-indexed
    new_slide = prs.slides.add_slide(layout)
    placeholders = slide_data.get('placeholders', {})

    # Layout별 분기 처리
    if layout_id == 1:  # 표지
        # title - TITLE 타입으로 접근
        title_shape = get_title_placeholder(new_slide)
        if title_shape and placeholders.get('title'):
            title_shape.text_frame.text = placeholders['title']

        # subtitle - idx=13
        subtitle_shape = get_placeholder_by_idx(new_slide, 13)
        if subtitle_shape and placeholders.get('subtitle'):
            subtitle_shape.text_frame.text = placeholders['subtitle']

    elif layout_id == 2:  # 목차
        toc_items = placeholders.get('toc_items', [])

        # 번호 열 (idx=17) - 줄바꿈으로 구분
        num_shape = get_placeholder_by_idx(new_slide, 17)
        if num_shape and toc_items:
            num_shape.text_frame.text = '\n'.join([item['number'] for item in toc_items])

        # 목차 제목 열 (idx=13)
        title_shape = get_placeholder_by_idx(new_slide, 13)
        if title_shape and toc_items:
            title_shape.text_frame.text = '\n'.join([item['title'] for item in toc_items])

        # 페이지 번호 열 (idx=14)
        page_shape = get_placeholder_by_idx(new_slide, 14)
        if page_shape and toc_items:
            page_shape.text_frame.text = '\n'.join([item['pages'] for item in toc_items])

    elif layout_id in [3, 4, 5]:  # 내지 슬라이드
        # main_title (idx=19)
        main_title_shape = get_placeholder_by_idx(new_slide, 19)
        if main_title_shape and placeholders.get('main_title'):
            main_title_shape.text_frame.text = placeholders['main_title']

        # action_title - TITLE 타입 (Layout 3, 4만)
        if layout_id in [3, 4]:
            action_shape = get_title_placeholder(new_slide)
            if action_shape and placeholders.get('action_title'):
                action_shape.text_frame.text = placeholders['action_title']

        # body (idx=18) - Layout 3, 5만
        if layout_id in [3, 5]:
            body_shape = get_placeholder_by_idx(new_slide, 18)
            if body_shape and placeholders.get('body'):
                body_shape.text_frame.text = placeholders['body']
```

### Step 3: 컨텐츠 영역 HTML 생성

`design_prompt`를 기반으로 **PPT 크기에 맞춘** 컨텐츠 영역 HTML 생성:

```python
# 3-0. PPT 컨텐츠 영역 크기 상수 (인치 → 픽셀 @ 96dpi)
CONTENT_WIDTH_PX = 983   # 10.24인치 × 96dpi
CONTENT_HEIGHT_PX = 494  # 5.14인치 × 96dpi

# 3-1. design_prompt로 HTML 생성 (크기 제약 포함)
html_content = generate_html_from_design_prompt(
    design_prompt=slide['design_prompt'],
    custom_elements=slide.get('custom_elements', []),
    color_scheme=presentation['color_scheme'],
    canvas_width=CONTENT_WIDTH_PX,    # PPT 크기 전달
    canvas_height=CONTENT_HEIGHT_PX
)

# 3-2. HTML 파일 저장
html_path = f"temp/slide_{slide_number}_content.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
```

**HTML 생성 가이드라인**:
```
HTML 생성 시 다음 크기 제약을 적용하세요:
- 캔버스 크기: 983px × 494px (PPT 컨텐츠 영역과 1:1 대응)
- 4열 그리드 카드: 약 230px 너비
- 3열 그리드 카드: 약 310px 너비
- 2열 분할: 각 약 480px 너비
- 모든 요소는 캔버스 경계 내에 배치
- 여백: 좌우 16px, 상하 12px 권장
```

### Step 4: HTML → PPT 오브젝트 삽입

생성된 HTML을 PPT 네이티브 오브젝트(Shape)로 변환하여 삽입:

```python
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# 4-1. HTML 파싱하여 PPT Shape으로 변환
def html_to_ppt_shapes(slide, html_path, design_prompt):
    """HTML 구조를 PPT 네이티브 오브젝트로 변환"""

    # 컨텐츠 영역 기준점 (PPT기본양식 분석 기준)
    # Layout 4 기준: x=270064 EMU, Action Title 하단 y≈1,431,130 EMU
    content_left = Emu(270064)      # ≈ 0.30 inches
    content_top = Emu(1431130)      # ≈ 1.57 inches (Action Title 하단)
    content_width = Emu(9362886)    # ≈ 10.24 inches
    content_height = Emu(4700000)   # ≈ 5.14 inches (바닥글 영역 제외)

    # design_prompt 기반 오브젝트 생성
    layout_info = design_prompt.get('layout', {})
    card_style = design_prompt.get('card_style', {})

    # 예: 카드 그리드 생성
    if layout_info.get('grid'):
        columns = int(layout_info['grid'].split('열')[0])
        card_width = content_width / columns - Inches(0.2)

        for i, item in enumerate(custom_elements):
            col = i % columns
            row = i // columns

            left = content_left + col * (card_width + Inches(0.2))
            top = content_top + row * Inches(1.8)

            # 카드 배경 Shape
            card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                left, top, card_width, Inches(1.6)
            )
            card.fill.solid()
            card.fill.fore_color.rgb = RGBColor(255, 255, 255)
            card.line.color.rgb = RGBColor(0, 36, 82)  # 네이비

            # 카드 내 텍스트
            tf = card.text_frame
            tf.text = item.get('title', '')

# 4-2. 컨텐츠 오브젝트 생성
html_to_ppt_shapes(new_slide, html_path, slide['design_prompt'])

# 4-3. Step 1에서 생성한 이미지 삽입 (필요시)
if png_path:
    # 이미지는 컨텐츠 영역 내 적절한 위치에 배치
    new_slide.shapes.add_picture(
        png_path,
        Inches(0.75), Inches(1.6),
        width=Inches(9.3)
    )
```

**오브젝트 타입별 변환:**

| HTML 요소 | PPT Shape |
|-----------|-----------|
| `<div class="card">` | `MSO_SHAPE.ROUNDED_RECTANGLE` |
| `<table>` | `slide.shapes.add_table()` |
| `<svg>`, `<img>` | `slide.shapes.add_picture()` |
| `<p>`, `<h1>` | `slide.shapes.add_textbox()` |
| `<ul>`, `<li>` | TextFrame with bullet points |

### Step 5: 임시 파일 정리

생성 완료 후 임시 파일 삭제:

```python
import os
import glob

# 5-1. PPT 저장
output_filename = f"{presentation['title']}_{presentation['date']}.pptx"
prs.save(output_filename)

# 5-2. 임시 파일 삭제
temp_files = glob.glob("temp/slide_*.*")
for f in temp_files:
    os.remove(f)

# 5-3. temp 폴더 삭제 (비어있을 경우)
if os.path.exists("temp") and not os.listdir("temp"):
    os.rmdir("temp")

print(f"✅ PPT 생성 완료: {output_filename}")
```

---

## 4. 디자인 원칙

### 콘텐츠 정렬
- **중앙 정렬 필수**: 콘텐츠가 한쪽으로 쏠리면 안됨
- 슬라이드 중앙(y: 50%)에 수직 배치
- 좌우 균등 마진 유지

### 색상 팔레트 (동국제강 브랜드)
| 색상 | HEX | 용도 |
|------|-----|------|
| 네이비 | `#002452` | 메인 컬러, 제목 |
| 레드 | `#C51F2A` | 강조, CTA |
| 청회색 | `#4B6580` | 보조 |
| 금색 | `#E9B86E` | 프리미엄 |
| 그린 | `#2E7D32` | 긍정, 성과 |

### 타이포그래피
| 요소 | 폰트 | 크기 |
|------|------|------|
| Main Title | 본고딕 Medium | 19pt |
| Action Title | 본고딕 Medium | 17pt |
| 본문 | 본고딕 Normal | 16pt |
| 캡션 | 본고딕 Normal | 14pt |

---

## 5. Custom Elements 처리

### design_prompt 활용
```json
{
  "design_prompt": {
    "concept": "디자인 컨셉",
    "layout": { "grid": "4열 균등 배치" },
    "card_style": { "background": "#FFFFFF" },
    "typography": { "title": "Bold, 16pt" }
  }
}
```

### image_generation_prompt 활용
- AI 이미지 생성 도구로 아이콘/다이어그램 생성
- 생성된 이미지를 슬라이드에 삽입
- 브랜드 컬러 일관성 유지

---

## 6. 출력

- **파일명**: `{presentation.title}_{date}.pptx`
- **저장 위치**: 현재 디렉토리 또는 지정 경로
- **품질 검증**: 플레이스홀더 값 누락 확인

---

## 예시 실행

```bash
# JSON 파일로 PPT 생성
/generate-ppt-from-json project-plan.json

# 결과: 스마트_물류관리_시스템_구축_프로젝트_수행계획서_2025.01.03.pptx
```
