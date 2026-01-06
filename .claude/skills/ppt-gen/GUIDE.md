# PPT Generation Service - 학습 가이드

AI 기반 PowerPoint 자동 생성 스킬의 전체 기능을 이해하고 활용하기 위한 종합 가이드입니다.

---

## 목차

1. [서비스 개요](#1-서비스-개요)
2. [아키텍처 이해](#2-아키텍처-이해)
3. [워크플로우 가이드](#3-워크플로우-가이드)
4. [템플릿 시스템](#4-템플릿-시스템)
5. [스크립트 상세 가이드](#5-스크립트-상세-가이드)
6. [디자인 시스템](#6-디자인-시스템)
7. [실습 튜토리얼](#7-실습-튜토리얼)
8. [베스트 프랙티스](#8-베스트-프랙티스)
9. [학습 로드맵](#9-학습-로드맵)

---

## 1. 서비스 개요

### 1.1 무엇을 할 수 있나요?

이 스킬은 **텍스트 콘텐츠를 전문가 수준의 PowerPoint 프레젠테이션으로 자동 변환**합니다.

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────────┐
│  텍스트/Markdown │ ──→ │   Claude    │ ──→ │  전문 PPT 파일   │
│  사용자 입력      │     │   AI 처리    │     │  (.pptx)        │
└─────────────────┘     └─────────────┘     └─────────────────┘
```

### 1.2 핵심 기능 5가지

| # | 기능 | 설명 | 사용 예 |
|---|------|------|--------|
| 1 | **새 PPT 생성** | 텍스트로 PPT 생성 | "AI 트렌드 PPT 만들어줘" |
| 2 | **템플릿 기반 생성** | 브랜드 양식으로 생성 | "동국제강 양식으로 보고서 만들어줘" |
| 3 | **기존 PPT 수정** | 텍스트 교체, 재배열 | "3번 슬라이드 제목 바꿔줘" |
| 4 | **스타일 추출** | 이미지에서 색상 추출 | "이 이미지 스타일로 PPT 만들어줘" |
| 5 | **디자인 검색** | 웹에서 레퍼런스 검색 | "미니멀 테크 PPT 디자인 찾아줘" |

### 1.3 지원 입력/출력

**입력:**
- Markdown 문서
- JSON 구조화 데이터
- 일반 텍스트
- 기존 PPTX 파일
- 이미지 (스타일 참조용)
- 웹 URL (슬라이드 크롤링)

**출력:**
- PPTX 파일 (PowerPoint 2016+)
- 썸네일 이미지 (검증용)
- YAML 템플릿 (등록용)

---

## 2. 아키텍처 이해

### 2.1 시스템 구성도

```
┌─────────────────────────────────────────────────────────────┐
│                        PPT-GEN 스킬                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  SKILL.md   │   │ html2pptx.md│   │  ooxml.md   │       │
│  │  (메인가이드) │   │ (HTML변환)   │   │ (XML편집)    │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    scripts/                          │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐       │   │
│  │  │html2pptx.js│ │inventory.py│ │ replace.py │       │   │
│  │  └────────────┘ └────────────┘ └────────────┘       │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐       │   │
│  │  │rearrange.py│ │thumbnail.py│ │template-   │       │   │
│  │  │            │ │            │ │analyzer.py │       │   │
│  │  └────────────┘ └────────────┘ └────────────┘       │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐       │   │
│  │  │asset-      │ │template-   │ │style-      │       │   │
│  │  │manager.py  │ │manager.py  │ │extractor.py│       │   │
│  │  └────────────┘ └────────────┘ └────────────┘       │   │
│  │  ┌────────────┐                                      │   │
│  │  │slide-      │                                      │   │
│  │  │crawler.py  │                                      │   │
│  │  └────────────┘                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   templates/                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │documents/│  │contents/ │  │ assets/  │           │   │
│  │  │(문서양식) │  │(슬라이드) │  │(이미지등) │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  references/                         │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │   │
│  │  │custom-       │ │design-       │ │color-        │ │   │
│  │  │elements.md   │ │system.md     │ │palettes.md   │ │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 핵심 컴포넌트

#### 가이드 문서 (3개)
| 파일 | 역할 | Claude 참조 시점 |
|------|------|-----------------|
| `SKILL.md` | 워크플로우 선택, 전체 흐름 | 모든 PPT 요청 시 |
| `html2pptx.md` | HTML → PPTX 변환 규칙 | 새 PPT 생성 시 |
| `ooxml.md` | XML 직접 편집 규칙 | 기존 PPT 수정 시 |

#### 스크립트 (10개)
| 스크립트 | 역할 | 워크플로우 |
|---------|------|-----------|
| `html2pptx.js` | HTML → PPTX 변환 | html2pptx |
| `inventory.py` | PPTX 텍스트 추출 | ooxml |
| `replace.py` | 텍스트 교체 | ooxml, template |
| `rearrange.py` | 슬라이드 재배열 | ooxml |
| `thumbnail.py` | 썸네일 생성 | 검증 |
| `template-analyzer.py` | PPTX → YAML | template-analyze |
| `asset-manager.py` | 에셋 CRUD | asset-manage |
| `template-manager.py` | 템플릿 관리 | template-manage |
| `style-extractor.py` | 색상 추출 | style-extract |
| `slide-crawler.py` | 슬라이드 크롤링 | slide-crawl |

---

## 3. 워크플로우 가이드

### 3.1 워크플로우 선택 플로우차트

```
사용자 요청 접수
       │
       ▼
┌──────────────────┐
│ 기존 PPTX 파일이  │──Yes──→ [ooxml] 기존 PPT 수정
│ 첨부되어 있나요?  │
└──────────────────┘
       │ No
       ▼
┌──────────────────┐
│ 회사/브랜드 양식  │──Yes──→ [template] 템플릿 기반 생성
│ 요청인가요?       │
└──────────────────┘
       │ No
       ▼
┌──────────────────┐
│ 스타일 이미지가   │──Yes──→ [style-extract] → [html2pptx]
│ 첨부되어 있나요?  │
└──────────────────┘
       │ No
       ▼
┌──────────────────┐
│ 디자인 레퍼런스   │──Yes──→ [design-search] → [html2pptx]
│ 검색 요청인가요?  │
└──────────────────┘
       │ No
       ▼
[html2pptx] 새 PPT 생성
```

### 3.2 워크플로우 상세

#### WF1: html2pptx (새 PPT 생성)

**트리거:** "PPT 만들어줘", "프레젠테이션 생성해줘"

**처리 흐름:**
```
1. 콘텐츠 분석
   └→ 섹션 분리, 슬라이드 수 결정

2. 디자인 결정
   └→ 컬러 팔레트, 레이아웃 유형 선택

3. HTML 슬라이드 생성 (슬라이드당 1개 HTML)
   └→ 720×405px, CSS 인라인

4. PPTX 변환
   └→ node scripts/html2pptx.js slides/ output.pptx

5. 검증
   └→ python scripts/thumbnail.py output.pptx thumbnails/
```

**입력 예시:**
```markdown
# AI 기술 트렌드 2024

## 1. 생성형 AI
- GPT-4, Claude 등 LLM 발전
- 이미지, 영상 생성 기술

## 2. 엣지 AI
- 온디바이스 처리
- 저전력 AI 칩

## 3. AI 규제
- EU AI Act
- 국내 AI 기본법
```

**출력:** `ai_trends_2024.pptx` (3 슬라이드)

---

#### WF2: template (템플릿 기반 생성)

**트리거:** "동국제강 양식으로", "회사 템플릿으로"

**처리 흐름:**
```
1. 템플릿 로드
   └→ templates/documents/{그룹}/registry.yaml 확인
   └→ 양식.yaml 로드

2. 콘텐츠 매핑
   └→ 사용자 콘텐츠 → 슬라이드 플레이스홀더

3. PPTX 생성/수정
   └→ 원본 PPTX 복사 또는 HTML 생성
   └→ 텍스트 교체

4. 브랜드 적용
   └→ config.yaml의 색상, 폰트 적용
```

**템플릿 구조:**
```yaml
# templates/documents/dongkuk/제안서1.yaml
document:
  id: 제안서1
  name: 제안서 (기본)
  source: .claude/includes/PPT기본양식.pptx

slides:
  - category: cover
    slide_index: 0
    placeholders:
      - type: title
      - type: subtitle
  - category: toc
    slide_index: 1
  - category: body
    slide_index: 2
```

---

#### WF3: ooxml (기존 PPT 수정)

**트리거:** "이 PPT 수정해줘", 파일 첨부 + 수정 요청

**처리 흐름:**
```
1. 인벤토리 추출
   └→ python scripts/inventory.py input.pptx > inventory.json

2. 변경사항 계획
   └→ 텍스트 교체, 슬라이드 재배열 결정

3. XML 수정
   └→ python scripts/replace.py input.pptx replacements.json output.pptx
   └→ python scripts/rearrange.py input.pptx "1,3,2,4" output.pptx

4. 검증
   └→ 썸네일 생성하여 확인
```

**인벤토리 예시:**
```json
{
  "slides": [
    {
      "index": 0,
      "texts": [
        {
          "text": "2023년 실적 보고서",
          "xpath": "//p:sp[1]//a:t",
          "type": "title"
        }
      ]
    }
  ]
}
```

---

#### WF4: template-analyze (템플릿 등록)

**트리거:** "이 PPTX를 템플릿으로 등록해줘"

**처리 흐름:**
```
1. PPTX 분석
   └→ python scripts/template-analyzer.py input.pptx 제안서1 --group mycompany

2. 자동 생성 파일
   └→ templates/documents/{group}/config.yaml
   └→ templates/documents/{group}/제안서1.yaml
   └→ templates/documents/{group}/registry.yaml
```

---

#### WF5: style-extract (스타일 추출)

**트리거:** "이 이미지 스타일 추출해줘", "스타일 저장해줘", 이미지 첨부

**처리 흐름 (LLM Vision 자연어 처리):**
```
1. 이미지 분석 (LLM Vision - Read tool)
   └→ 스크립트 실행 없이 Claude가 직접 분석

2. 색상 추출 및 역할 분류
   └→ Primary, Secondary, Accent, Background, Text

3. 자동 분류 (color-palettes.md 참조)
   └→ 무드 감지: Navy/Blue→전문적, Green→자연, Red/Orange→활기

4. 자동 저장 (3타입 구조)
   └→ 테마: documents/{그룹}/config.yaml
   └→ 레이아웃: contents/templates/{id}.yaml
   └→ 이미지: assets/images/{id}.png

5. Registry 자동 업데이트
```

**출력 예시:**
```yaml
colors:
  palette: [4E9F3D, 1E5128, D8E9A8, 7BC74D, FFFFFF]
  roles:
    primary: 4E9F3D      # 채도 높은 색 → 제목/강조
    secondary: 1E5128    # 두 번째 채도 → 부제목
    accent: D8E9A8       # 나머지 → 포인트
    background: FFFFFF   # 가장 밝은 색 → 배경
    text: 1E5128         # 가장 어두운 색 → 본문
```

---

#### WF6: design-search (디자인 검색)

**트리거:** "PPT 디자인 찾아줘", "레퍼런스 검색해줘"

**처리 흐름:**
```
1. 웹 검색
   └→ Dribbble, Behance, Pinterest 검색

2. 레퍼런스 제시
   └→ 스타일, 색상, 특징 설명

3. 사용자 선택
   └→ 선택된 스타일로 PPT 생성
```

---

#### WF7: template-manage (템플릿 관리)

**트리거:** "템플릿 목록 보여줘", "템플릿 삭제해줘"

```bash
# 목록 조회
python scripts/template-manager.py list
python scripts/template-manager.py list --type documents

# 상세 정보
python scripts/template-manager.py info 제안서1

# 아카이브 (비활성화)
python scripts/template-manager.py archive 제안서1

# 복원
python scripts/template-manager.py restore 제안서1

# 삭제
python scripts/template-manager.py delete 제안서1
```

---

#### WF8: asset-manage (에셋 관리)

**트리거:** "이 아이콘 저장해줘", "에셋 검색해줘"

```bash
# 추가
python scripts/asset-manager.py add icon.svg --id chart-line --tags "chart,data"

# 검색
python scripts/asset-manager.py search chart
python scripts/asset-manager.py search --tags background

# 목록
python scripts/asset-manager.py list --type icons

# 삭제
python scripts/asset-manager.py delete chart-line
```

---

#### WF9: slide-crawl (슬라이드 크롤링)

**트리거:** "이 슬라이드 패턴 저장해줘", URL 제공

```bash
# 크롤링 및 템플릿 생성
python scripts/slide-crawler.py "https://slideshare.net/..." --output my-template

# 분석만
python scripts/slide-crawler.py "https://speakerdeck.com/..." --analyze-only
```

---

## 4. 템플릿 시스템

### 4.1 3타입 구조

```
templates/
├── documents/       # [타입 1] 문서 템플릿
│   └── {그룹}/
│       ├── config.yaml      # 브랜드 테마
│       ├── registry.yaml    # 양식 목록
│       └── {양식}.yaml      # 양식 정의
│
├── contents/        # [타입 2] 콘텐츠 템플릿
│   ├── registry.yaml
│   └── templates/
│       └── {패턴}.yaml
│
└── assets/          # [타입 3] 공용 에셋
    ├── registry.yaml
    ├── icons/
    └── images/
```

### 4.2 문서 템플릿 (Documents)

**용도:** 회사/브랜드별 전체 PPT 양식

**config.yaml (그룹 테마):**
```yaml
group:
  id: dongkuk
  name: 동국그룹

theme:
  colors:
    primary: "#002452"     # 네이비
    secondary: "#C51F2A"   # 레드
    dark_text: "#262626"
    light_bg: "#FFFFFF"
  fonts:
    title: Arial
    body: Arial
```

**양식.yaml (개별 양식):**
```yaml
document:
  id: 제안서1
  name: 제안서 (기본)
  source: .claude/includes/PPT기본양식.pptx

slides:
  - index: 0
    category: cover
    use_for: 문서 제목, 발표 표지
  - index: 1
    category: toc
    use_for: 목차, 아젠다
  - index: 2
    category: content_bullets
    use_for: 설명, 개요, 리스트
```

### 4.3 콘텐츠 템플릿 (Contents)

**용도:** 재사용 가능한 슬라이드 패턴

**예시: timeline1.yaml**
```yaml
template:
  id: timeline1
  name: 타임라인 (가로)
  category: timeline

structure:
  type: horizontal
  items: 4-6

html_pattern: |
  <div class="timeline">
    <div class="timeline-item">
      <div class="date">Q1 2024</div>
      <div class="title">Phase 1</div>
      <div class="desc">설명</div>
    </div>
    <!-- 반복 -->
  </div>

usage:
  keywords: [로드맵, 일정, 마일스톤, 계획]
  use_for: 프로젝트 일정, 로드맵, 단계별 계획
```

### 4.4 에셋 (Assets)

**용도:** 공용 아이콘, 이미지

**registry.yaml:**
```yaml
icons:
  - id: chart-line
    name: 라인 차트
    file: icons/chart-line.svg
    tags: [chart, data, analytics]

images:
  - id: hero-tech-bg
    name: 테크 배경
    file: images/hero-tech-bg.png
    tags: [background, tech]
```

---

## 5. 스크립트 상세 가이드

### 5.1 html2pptx.js

**역할:** HTML 파일들을 PPTX로 변환

**사용법:**
```bash
node scripts/html2pptx.js <input_dir> <output.pptx> [options]

# 예시
node scripts/html2pptx.js slides/ output.pptx
node scripts/html2pptx.js slides/ output.pptx --layout 4x3
```

**입력 HTML 규칙:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720px;      /* 필수: 슬라이드 너비 */
      height: 405px;     /* 필수: 슬라이드 높이 (16:9) */
      margin: 0;
      background-color: #FFFFFF;
    }
  </style>
</head>
<body>
  <h1 style="position:absolute; left:30px; top:30px; font-size:36px;">
    제목
  </h1>
  <div style="position:absolute; left:30px; top:100px;">
    <ul>
      <li>항목 1</li>
      <li>항목 2</li>
    </ul>
  </div>
</body>
</html>
```

**지원 요소:** `p, h1-h6, ul, ol, li, div, img, span, b, i, u, br`

**지원 CSS:** `font-size, color, background-color, border, border-radius, box-shadow`

**Placeholder (차트/표 위치):**
```html
<div id="chart-1" class="placeholder"
     style="position:absolute; left:50px; top:100px; width:400px; height:300px;">
</div>
```

---

### 5.2 inventory.py

**역할:** PPTX에서 모든 텍스트 추출

**사용법:**
```bash
python scripts/inventory.py <input.pptx> [--output inventory.json]

# 예시
python scripts/inventory.py presentation.pptx > inventory.json
```

**출력 형식:**
```json
{
  "file": "presentation.pptx",
  "slide_count": 5,
  "slides": [
    {
      "index": 0,
      "texts": [
        {
          "text": "프레젠테이션 제목",
          "shape_id": 2,
          "type": "title",
          "position": {"left": 0.5, "top": 0.3}
        }
      ]
    }
  ]
}
```

---

### 5.3 replace.py

**역할:** PPTX 내 텍스트 일괄 교체

**사용법:**
```bash
python scripts/replace.py <input.pptx> <replacements.json> <output.pptx>

# 예시
python scripts/replace.py input.pptx replacements.json output.pptx
```

**replacements.json 형식:**
```json
{
  "replacements": [
    {"from": "2023년", "to": "2024년"},
    {"from": "기존 제목", "to": "새로운 제목"},
    {"from": "{{company}}", "to": "동국제강"}
  ]
}
```

---

### 5.4 rearrange.py

**역할:** 슬라이드 순서 변경

**사용법:**
```bash
python scripts/rearrange.py <input.pptx> <order> <output.pptx>

# 예시 (1,3,2,4 순서로 재배열)
python scripts/rearrange.py input.pptx "1,3,2,4" output.pptx

# 예시 (2번 슬라이드 제거)
python scripts/rearrange.py input.pptx "1,3,4,5" output.pptx
```

---

### 5.5 thumbnail.py

**역할:** PPTX 슬라이드 썸네일 생성 (검증용)

**사용법:**
```bash
python scripts/thumbnail.py <input.pptx> <output_dir> [--cols N]

# 예시
python scripts/thumbnail.py output.pptx thumbnails/
python scripts/thumbnail.py output.pptx thumbnails/ --cols 4
```

**출력:** 각 슬라이드의 PNG 이미지 + 전체 그리드 이미지

---

### 5.6 template-analyzer.py

**역할:** PPTX를 분석하여 YAML 템플릿으로 변환

**사용법:**
```bash
python scripts/template-analyzer.py <input.pptx> <template_id> --group <group_id> [options]

# 예시
python scripts/template-analyzer.py company.pptx 제안서1 --group acme
python scripts/template-analyzer.py report.pptx 보고서1 --group acme --name "보고서 (기본)" --type report
```

**옵션:**
- `--group`: 그룹 ID (필수)
- `--name`: 표시 이름
- `--type`: proposal, report, plan, general
- `--description`: 설명

**생성 파일:**
```
templates/documents/{group}/
├── config.yaml       # 테마 (색상, 폰트)
├── registry.yaml     # 양식 목록
└── {template_id}.yaml # 양식 정의
```

---

### 5.7 asset-manager.py

**역할:** 에셋 CRUD 관리

**명령어:**

```bash
# add - 에셋 추가
python scripts/asset-manager.py add <file_or_url> --id <id> [--tags "tag1,tag2"] [--name "표시이름"]

# 로컬 파일
python scripts/asset-manager.py add chart-icon.svg --id chart-line --tags "chart,data"

# URL에서 다운로드
python scripts/asset-manager.py add "https://example.com/bg.png" --id hero-bg --tags "background"
```

```bash
# search - 검색
python scripts/asset-manager.py search <query>
python scripts/asset-manager.py search chart
python scripts/asset-manager.py search --tags background
```

```bash
# list - 목록
python scripts/asset-manager.py list
python scripts/asset-manager.py list --type icons
python scripts/asset-manager.py list --type images
python scripts/asset-manager.py list --format json
python scripts/asset-manager.py list --format yaml
```

```bash
# info - 상세 정보
python scripts/asset-manager.py info <id>
python scripts/asset-manager.py info chart-line
```

```bash
# delete - 삭제
python scripts/asset-manager.py delete <id>
python scripts/asset-manager.py delete chart-line
python scripts/asset-manager.py delete chart-line -f  # 확인 없이
```

---

### 5.8 template-manager.py

**역할:** 템플릿 조회/관리

**명령어:**

```bash
# list - 목록
python scripts/template-manager.py list
python scripts/template-manager.py list --type documents
python scripts/template-manager.py list --type contents
python scripts/template-manager.py list --archived  # 아카이브 포함
python scripts/template-manager.py list --format json
```

```bash
# info - 상세 정보
python scripts/template-manager.py info <template_id>
python scripts/template-manager.py info 제안서1
python scripts/template-manager.py info 제안서1 --preview  # 내용 미리보기
```

```bash
# archive - 아카이브 (숨김)
python scripts/template-manager.py archive <template_id>
python scripts/template-manager.py archive 제안서1
```

```bash
# restore - 복원
python scripts/template-manager.py restore <template_id>
python scripts/template-manager.py restore 제안서1
```

```bash
# delete - 완전 삭제
python scripts/template-manager.py delete <template_id>
python scripts/template-manager.py delete 제안서1
python scripts/template-manager.py delete 제안서1 -f  # 확인 없이
```

---

### 5.9 style-extractor.py (선택적 CLI 도구)

**역할:** 이미지에서 색상 추출 및 분류

> **참고:** 일반적으로 Claude가 LLM Vision으로 직접 분석합니다.
> 이 스크립트는 대량 이미지 배치 처리나 자동화 파이프라인용입니다.

**권장 방법 (자연어):**
```
"이 이미지 스타일 추출해줘"
→ Claude가 LLM Vision으로 분석 → 자동 분류 → 자동 저장
```

**CLI 사용법 (배치/자동화용):**
```bash
python scripts/style-extractor.py <image> [options]

# YAML 스타일 가이드 생성
python scripts/style-extractor.py design.png --output style.yaml

# 색상만 추출 (6개)
python scripts/style-extractor.py design.png --colors-only --count 6

# CSS 변수로 출력
python scripts/style-extractor.py design.png --format css

# JSON 출력
python scripts/style-extractor.py design.png --format json
```

**옵션:**
- `--output, -o`: 출력 파일 경로
- `--count, -n`: 추출할 색상 수 (기본: 5)
- `--format, -f`: 출력 형식 (yaml, json, css)
- `--colors-only`: 색상만 출력 (분류 없이)

**출력 예시 (YAML):**
```yaml
style:
  name: design
  source: design.png

colors:
  palette: [4E9F3D, 1E5128, D8E9A8, 7BC74D, FFFFFF]
  roles:
    primary: 4E9F3D
    secondary: 1E5128
    accent: D8E9A8
    background: FFFFFF
    text: 1E5128

pptx_colors:
  primary: 4E9F3D
  secondary: 1E5128
  accent: D8E9A8
  background: FFFFFF
  text: 1E5128

chart_colors: [4E9F3D, 1E5128, D8E9A8, 7BC74D]
```

**출력 예시 (CSS):**
```css
:root {
  --color-primary: #4E9F3D;
  --color-secondary: #1E5128;
  --color-accent: #D8E9A8;
  --color-background: #FFFFFF;
  --color-text: #1E5128;

  --palette-1: #4E9F3D;
  --palette-2: #1E5128;
  --palette-3: #D8E9A8;
  --palette-4: #7BC74D;
  --palette-5: #FFFFFF;
}
```

---

### 5.10 slide-crawler.py

**역할:** 온라인 슬라이드 크롤링 및 템플릿 생성

**사용법:**
```bash
python scripts/slide-crawler.py <url> [options]

# SlideShare 크롤링
python scripts/slide-crawler.py "https://www.slideshare.net/user/deck" --output my-template

# Speaker Deck 크롤링
python scripts/slide-crawler.py "https://speakerdeck.com/user/deck" --output timeline2 --category timeline

# 분석만 (저장 안함)
python scripts/slide-crawler.py "https://slideshare.net/..." --analyze-only
```

**옵션:**
- `--output, -o`: 템플릿 ID (저장 시 필수)
- `--name, -n`: 템플릿 이름
- `--category, -c`: 카테고리 (cover, timeline, process 등)
- `--analyze-only`: 분석만 수행

**지원 사이트:**
- SlideShare (slideshare.net)
- Speaker Deck (speakerdeck.com)
- 기타 웹페이지 (이미지 기반 추출)

**생성 파일:**
```
templates/contents/templates/{template_id}.yaml
templates/contents/registry.yaml (자동 업데이트)
```

---

## 6. 디자인 시스템

### 6.1 슬라이드 규격

| 비율 | 크기 (px) | 용도 |
|------|----------|------|
| **16:9** | 720 × 405 | 기본 (프레젠테이션) |
| 4:3 | 720 × 540 | 레거시, 인쇄 |
| 16:10 | 720 × 450 | 노트북 화면 |

### 6.2 타이포그래피

| 요소 | 크기 | 굵기 |
|------|------|------|
| 메인 타이틀 | 48pt | Bold |
| 부제목 | 28pt | Semi-bold |
| 섹션 제목 | 24pt | Bold |
| 본문 | 16pt | Regular |
| 캡션 | 11pt | Regular |
| 강조 숫자 | 60pt | Bold |

**웹 안전 폰트:** Arial, Helvetica, Times New Roman, Georgia, Verdana

### 6.3 레이아웃

**권장: 2열 비대칭**
```
┌─────────────────────────────────────┐
│  제목 (전체 너비)                    │
├──────────────┬──────────────────────┤
│   텍스트     │    차트/이미지        │
│   (40%)      │      (60%)           │
└──────────────┴──────────────────────┘
```

**여백:**
- 외부: 30px
- 내부 패딩: 40px
- 요소 간격: 20-30px

### 6.4 색상 규칙

**HEX 표기 (# 제외):**
```javascript
// 올바름
color: "FF0000"
chartColors: ["4472C4", "ED7D31"]

// 잘못됨 (파일 손상 가능)
color: "#FF0000"
```

**역할별 색상:**
| 역할 | 용도 |
|------|------|
| Primary | 제목, 강조, CTA |
| Secondary | 부제목, 보조 |
| Accent | 하이라이트, 아이콘 |
| Background | 슬라이드 배경 |
| Text | 본문 텍스트 |

---

## 7. 실습 튜토리얼

### 실습 1: 첫 PPT 만들기

**목표:** 간단한 3페이지 PPT 생성

**Step 1:** 콘텐츠 준비
```markdown
# 회사 소개

## 비전
고객 중심의 혁신적 솔루션 제공

## 핵심 가치
- 혁신
- 신뢰
- 협력

## 연락처
contact@company.com
```

**Step 2:** Claude에게 요청
```
위 내용으로 회사 소개 PPT 3장 만들어줘.
색상은 블루 계열로 해줘.
```

**Step 3:** 결과 확인
- 생성된 PPTX 파일 열기
- 썸네일로 레이아웃 확인

---

### 실습 2: 템플릿 등록하기

**목표:** 기존 PPTX를 템플릿으로 등록

**Step 1:** PPTX 파일 준비

**Step 2:** 분석 실행
```bash
python scripts/template-analyzer.py my_template.pptx 제안서1 --group mycompany --name "제안서 (기본)"
```

**Step 3:** 생성 파일 확인
```
templates/documents/mycompany/
├── config.yaml
├── registry.yaml
└── 제안서1.yaml
```

**Step 4:** 템플릿 사용
```
mycompany 양식으로 신규 사업 제안서 만들어줘
```

---

### 실습 3: 스타일 추출 및 적용

**목표:** 이미지에서 색상을 추출하여 PPT에 적용

**Step 1:** 참조 이미지 첨부 + 요청
```
[design.png 첨부]
이 이미지 스타일 추출해서 저장해줘
```

**Step 2:** Claude 자동 처리 (LLM Vision)
```
→ 색상 분석: Primary #4E9F3D, Secondary #1E5128...
→ 무드 분류: "자연/친환경" (Green 계열)
→ 자동 저장:
  - templates/documents/extracted/config.yaml (테마)
  - templates/contents/templates/nature-20250106.yaml (레이아웃)
  - templates/assets/images/ref-nature-20250106.png (원본)
→ Registry 업데이트 완료
```

**Step 3:** 추출된 스타일로 PPT 생성
```
방금 추출한 스타일로 환경 보고서 PPT 만들어줘
```

**Step 4:** (선택) CLI로 배치 처리
```bash
# 여러 이미지를 한번에 처리할 때만 사용
python scripts/style-extractor.py design.png --output style.yaml
```

---

### 실습 4: 기존 PPT 수정

**목표:** 기존 PPTX의 텍스트 교체 및 재배열

**Step 1:** 텍스트 인벤토리 추출
```bash
python scripts/inventory.py presentation.pptx > inventory.json
```

**Step 2:** 교체 규칙 작성
```json
{
  "replacements": [
    {"from": "2023년", "to": "2024년"},
    {"from": "기존 회사명", "to": "새 회사명"}
  ]
}
```

**Step 3:** 텍스트 교체
```bash
python scripts/replace.py presentation.pptx replacements.json output.pptx
```

**Step 4:** 슬라이드 재배열 (선택)
```bash
python scripts/rearrange.py output.pptx "1,3,2,4,5" final.pptx
```

---

### 실습 5: 에셋 관리

**목표:** 아이콘을 추가하고 검색하여 사용

**Step 1:** 아이콘 추가
```bash
python scripts/asset-manager.py add chart-icon.svg --id chart-line --tags "chart,data,analytics"
```

**Step 2:** 검색
```bash
python scripts/asset-manager.py search chart
```

**Step 3:** 목록 확인
```bash
python scripts/asset-manager.py list --type icons
```

**Step 4:** PPT 생성 시 사용
```
차트 아이콘(chart-line)을 사용해서 데이터 분석 PPT 만들어줘
```

---

## 8. 베스트 프랙티스

### 8.1 PPT 생성 시

**DO (권장):**
- 슬라이드당 핵심 메시지 1개
- 연속 3장 이상 동일 레이아웃 피하기
- 비대칭 2열 레이아웃 활용
- 여백 충분히 확보 (30px 이상)
- 텍스트보다 비주얼 우선

**DON'T (금지):**
- 한 슬라이드에 너무 많은 정보
- 작은 폰트 (12pt 미만)
- 5개 초과 불릿 포인트
- 저해상도 이미지
- 과도한 색상 사용 (5색 초과)

### 8.2 템플릿 관리 시

**DO:**
- 명확한 ID/이름 사용 (제안서1, 보고서1)
- 그룹별로 분류 (회사, 프로젝트)
- 사용하지 않는 템플릿은 아카이브
- registry.yaml 정기 확인

**DON'T:**
- 중복 템플릿 생성
- 원본 PPTX 직접 수정
- 경로에 특수문자 사용

### 8.3 에셋 관리 시

**DO:**
- 의미 있는 태그 부여
- 고해상도 이미지 사용 (150 DPI 이상)
- SVG 아이콘 권장
- 출처 기록 (original_url)

**DON'T:**
- 저작권 위반 이미지 사용
- 태그 없이 추가
- 중복 에셋 생성

### 8.4 색상 사용 시

**DO:**
- 3-5색 조합 유지
- 대비 확인 (4.5:1 이상)
- 브랜드 색상 일관되게 사용
- HEX에서 # 제외

**DON'T:**
- 너무 많은 색상 (5색 초과)
- 낮은 대비 (밝은 배경 + 밝은 텍스트)
- 임의의 색상 매번 변경

---

## 9. 학습 로드맵

### Level 1: 기초 (1-2일)

1. **개념 이해**
   - 서비스 개요 읽기
   - 워크플로우 선택 가이드 이해

2. **첫 PPT 생성**
   - html2pptx 워크플로우로 간단한 PPT 만들기
   - 실습 1 완료

3. **기존 PPT 수정**
   - inventory.py로 텍스트 추출
   - replace.py로 텍스트 교체
   - 실습 4 완료

---

### Level 2: 중급 (3-5일)

1. **템플릿 시스템 이해**
   - 3타입 구조 학습
   - 기존 템플릿 분석

2. **템플릿 등록**
   - template-analyzer.py 사용
   - 실습 2 완료

3. **스타일 추출**
   - style-extractor.py 사용
   - 실습 3 완료

4. **디자인 시스템 학습**
   - references/ 문서 읽기
   - 색상 팔레트 이해

---

### Level 3: 고급 (1주+)

1. **에셋 관리**
   - asset-manager.py 마스터
   - 실습 5 완료

2. **고급 템플릿 관리**
   - template-manager.py 활용
   - 아카이브/복원 운영

3. **슬라이드 크롤링**
   - slide-crawler.py 사용
   - 외부 슬라이드 패턴 수집

4. **커스텀 워크플로우**
   - 여러 워크플로우 조합
   - 자동화 파이프라인 구축

---

### 학습 체크리스트

**Level 1:**
- [ ] 서비스 개요 이해
- [ ] 워크플로우 선택 가이드 숙지
- [ ] 첫 PPT 생성 (html2pptx)
- [ ] 기존 PPT 텍스트 교체
- [ ] 썸네일로 결과 검증

**Level 2:**
- [ ] 템플릿 3타입 구조 이해
- [ ] 새 템플릿 등록 (template-analyzer)
- [ ] 이미지 스타일 추출 (style-extractor)
- [ ] 디자인 시스템 문서 숙지
- [ ] 컬러 팔레트 활용

**Level 3:**
- [ ] 에셋 추가/검색/삭제
- [ ] 템플릿 아카이브/복원
- [ ] 온라인 슬라이드 크롤링
- [ ] 복합 워크플로우 실행
- [ ] 베스트 프랙티스 적용

---

## 부록: 빠른 참조

### 자주 사용하는 명령어

```bash
# PPT 생성
node scripts/html2pptx.js slides/ output.pptx

# 템플릿 등록
python scripts/template-analyzer.py input.pptx 제안서1 --group mycompany

# 텍스트 추출/교체
python scripts/inventory.py input.pptx > inventory.json
python scripts/replace.py input.pptx replacements.json output.pptx

# 스타일 추출
python scripts/style-extractor.py image.png --output style.yaml

# 에셋 관리
python scripts/asset-manager.py add icon.svg --id my-icon --tags "tag1,tag2"
python scripts/asset-manager.py search keyword

# 템플릿 관리
python scripts/template-manager.py list
python scripts/template-manager.py info 제안서1

# 슬라이드 크롤링
python scripts/slide-crawler.py "https://slideshare.net/..." --output my-template
```

### 의존성 설치

```bash
# Node.js
npm install pptxgenjs playwright sharp

# Python (필수)
pip install python-pptx pyyaml

# Python (유틸리티)
pip install Pillow requests beautifulsoup4

# Python (선택)
pip install colorthief markitdown
```

### 문서 위치

| 문서 | 위치 | 내용 |
|------|------|------|
| README.md | `.claude/skills/ppt-gen/` | 전체 개요 |
| GUIDE.md | `.claude/skills/ppt-gen/` | 학습 가이드 (이 문서) |
| SKILL.md | `.claude/skills/ppt-gen/` | Claude 가이드 |
| custom-elements.md | `references/` | HTML 요소 스키마 |
| design-system.md | `references/` | 디자인 규칙 |
| color-palettes.md | `references/` | 컬러 팔레트 |

---

## 문의 및 피드백

이 스킬에 대한 문의나 개선 제안은 프로젝트 관리자에게 연락하세요.
