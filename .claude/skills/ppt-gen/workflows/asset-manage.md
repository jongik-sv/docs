# Asset Management Workflow

에셋(이미지/아이콘)을 저장하고 검색합니다.

## Saving Assets

### Triggers

- "이 아이콘 저장해줘" (SVG 생성 후)
- "다운받은 로고 저장해줘"

### Workflow

1. **Save Asset File**:
   - 아이콘: `templates/assets/icons/{id}.svg`
   - 이미지: `templates/assets/images/{id}.png`

2. **Update Registry** (`templates/assets/registry.yaml`):

```yaml
icons:
  - id: new-icon
    name: 새 아이콘
    file: icons/new-icon.svg
    source: generated    # generated | downloaded | brand
    tags: ["tag1", "tag2"]
    created: 2026-01-06
```

3. **Generate Thumbnail** (optional):
   - `templates/assets/thumbnails/{id}.jpg`

### Source Types

| source | 설명 | 예시 |
|--------|------|------|
| `generated` | Claude가 직접 생성한 SVG/이미지 | 아이콘, 다이어그램 |
| `downloaded` | 웹에서 다운로드 | 배경 이미지, 스톡 사진 |
| `brand` | 브랜드 공식 에셋 (Brandfetch 등) | 회사 로고 |

---

## Searching Assets

### Triggers

- "차트 관련 아이콘 찾아줘"
- "저장된 로고 보여줘"

### Workflow

1. **Search Registry** (`templates/assets/registry.yaml`):
   - `tags` 배열에서 키워드 매칭
   - `name` 필드에서 검색
   - `source` 타입으로 필터링

2. **Display Results**:
   - 매칭된 에셋 목록
   - 썸네일 이미지 (있는 경우)
   - 파일 경로

3. **Apply to PPT** (optional):
   - html2pptx 워크플로우에서 에셋 참조
   - 이미지 삽입 시 파일 경로 사용

### Search Examples

```bash
# 태그로 검색
tags: ["chart"] → chart-line.svg, chart-bar.svg

# 소스로 필터링
source: brand → dongkuk-logo.png, company-icon.svg

# 이름으로 검색
name: "화살표" → arrow-right.svg, arrow-down.svg
```

## Asset Directory Structure

```
templates/assets/
├── registry.yaml       # 에셋 레지스트리
├── icons/             # SVG 아이콘
│   ├── chart-line.svg
│   └── arrow-right.svg
├── images/            # 이미지 파일
│   ├── tech-bg.png
│   └── office-photo.jpg
└── thumbnails/        # 썸네일 (자동 생성)
    └── tech-bg.jpg
```

## Company Logos

회사 로고는 documents 폴더에 저장:

```
templates/documents/{그룹}/assets/{계열사}/logo.png
```

예: `templates/documents/dongkuk/assets/dongkuk-steel/logo.png`
