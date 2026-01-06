# Template-Based Creation Workflow

기존 템플릿을 사용하여 새 PPT를 생성합니다.

## Triggers

- "동국제강 양식으로"
- "템플릿으로 PPT 만들어줘"
- "회사 양식 사용해줘"

## 3-Type Template System

### 1. Document Templates (documents/)

그룹/회사별 폴더 구조:

```
documents/dongkuk/
├── config.yaml          # 그룹 공통 테마
├── registry.yaml        # 양식 목록
├── assets/              # 계열사별 에셋
│   ├── dongkuk-steel/logo.png
│   └── dongkuk-cm/logo.png
├── 제안서1.yaml
└── 보고서1.yaml
```

### 2. Content Templates (contents/)

슬라이드 패턴:

```
contents/
├── registry.yaml
├── templates/
│   ├── cover1.yaml
│   ├── comparison1.yaml
│   └── timeline1.yaml
└── thumbnails/
```

### 3. Shared Assets (assets/)

공용 이미지/아이콘:

```yaml
# assets/registry.yaml
icons:
  - id: chart-line
    file: icons/chart-line.svg
    tags: ["chart", "data"]
```

## Workflow

### Step 0: Load Template

템플릿/브랜드 요청 시 YAML 먼저 로드:

```
# documents/dongkuk/config.yaml → 테마
# documents/dongkuk/registry.yaml → 양식 목록
```

### Step 1: Extract and Analyze

```bash
# 텍스트 추출
python -m markitdown template.pptx > template-content.md

# 썸네일 그리드 생성
python scripts/thumbnail.py template.pptx
```

### Step 2: Create Inventory

`template-inventory.md` 생성:

```markdown
# Template Inventory Analysis
**Total Slides: [count]**
**슬라이드는 0-indexed (첫 슬라이드 = 0)**

## [Category Name]
- Slide 0: [Layout] - Description
- Slide 1: [Layout] - Description
```

### Step 3: Create Outline

`outline.md` 생성 - 템플릿 매핑 포함:

```python
template_mapping = [
    0,   # Use slide 0 (Title/Cover)
    34,  # Use slide 34 (B1: Title and body)
    50,  # Use slide 50 (E1: Quote)
]
```

**레이아웃 선택 규칙**:
- 2열 레이아웃: 정확히 2개 항목일 때만
- 3열 레이아웃: 정확히 3개 항목일 때만
- 이미지+텍스트: 실제 이미지가 있을 때만
- 인용 레이아웃: 실제 인용문(출처 포함)일 때만

### Step 4: Rearrange Slides

```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
```

- 0-indexed
- 같은 인덱스 여러 번 사용 가능 (복제)

### Step 5: Extract Text Inventory

```bash
python scripts/inventory.py working.pptx text-inventory.json
```

JSON 구조:
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "paragraphs": [{ "text": "...", "bold": true }]
    }
  }
}
```

### Step 6: Generate Replacement

`replacement-text.json` 생성:

```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        { "text": "New Title", "bold": true, "alignment": "CENTER" },
        { "text": "Bullet item", "bullet": true, "level": 0 }
      ]
    }
  }
}
```

**규칙**:
- `paragraphs` 없는 shape는 자동으로 텍스트 삭제
- bullet: true일 때 bullet 심볼 (•, -, *) 포함하지 않기
- level은 bullet: true일 때 필수

### Step 7: Apply Replacements

```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```

## LLM Template Selection Process

1. **문서 템플릿**: 회사/그룹 언급 시
   - config.yaml → 테마 적용
   - registry.yaml → 양식 목록

2. **콘텐츠 템플릿**: 데이터 특성에 맞는 패턴
   - contents/registry.yaml 검색

3. **조합**: 문서 테마 + 양식 + 에셋 + 콘텐츠 패턴

**예시**: "동국제강 제안서" 요청:
- 테마: dongkuk/config.yaml
- 양식: dongkuk/제안서1.yaml
- 로고: dongkuk/assets/dongkuk-steel/logo.png
