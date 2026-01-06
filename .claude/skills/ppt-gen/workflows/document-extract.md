# Document Template Extraction Workflow

전체 문서의 구조와 테마를 분석하여 문서 템플릿(회사/브랜드)으로 저장합니다.

## Triggers

- "문서 양식 추출해줘"
- "이 PPT를 템플릿으로 등록"
- "회사 양식으로 저장"

## Workflow

### 1. Generate Thumbnails

```bash
python scripts/thumbnail.py input.pptx workspace/template-preview
```

### 2. Analyze Theme and Layouts

```bash
# PPTX 언팩
python ooxml/scripts/unpack.py input.pptx workspace/unpacked
```

분석 항목:
- **테마 파일**: `ppt/theme/theme1.xml` → 색상/폰트 추출
- **슬라이드 레이아웃**: 각 슬라이드 카테고리 분류

### 3. Create Group Folder and YAML

`templates/documents/{그룹}/` 폴더 생성:

**config.yaml** (테마 정보):
```yaml
group:
  id: new-company
  name: New Company

theme:
  colors:
    primary: "#002452"
    secondary: "#C51F2A"
  fonts:
    title: "본고딕 Bold"
    body: "본고딕 Normal"

companies:
  - id: new-company
    name: New Company
```

**{양식}.yaml** (레이아웃 정보):
```yaml
template:
  id: 제안서1
  name: 제안서 (기본)
  source: input.pptx

layouts:
  - index: 0
    category: cover
    name: 표지
  - index: 1
    category: toc
    name: 목차
  - index: 2
    category: content_bullets
    name: 본문 (불릿)
```

### 4. Update Registry

`templates/documents/{그룹}/registry.yaml`:

```yaml
templates:
  - id: 제안서1
    name: 제안서 (기본)
    file: 제안서1.yaml
    type: proposal
    description: "표지 + 목차 + 본문(불릿) + 마무리 구성"
```

### 5. User Confirmation

- 생성된 썸네일 표시
- 템플릿 정보 요약 제공

## Auto Layout Classification

| 카테고리 | 감지 조건 |
|----------|----------|
| `cover` | 첫 슬라이드, 큰 제목만 |
| `toc` | 번호+텍스트 반복 패턴 |
| `section` | 제목만, 배경색 있음 |
| `content_bullets` | BODY placeholder + 불릿 |
| `content_free` | 제목만, 넓은 빈 공간 |

## Output Structure

```
templates/documents/{그룹}/
├── config.yaml          # 테마 정보
├── registry.yaml        # 양식 목록
├── assets/              # 에셋 (로고 등)
└── {양식}.yaml          # 각 양식 정의
```
