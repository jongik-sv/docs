# PRD: PPT Skills Suite

**버전**: 4.2
**작성일**: 2026-01-08
**상태**: Draft

---

## 1. 개요

### 1.1 제품 비전

Claude Code 환경에서 **전문 디자이너 수준의 PPT**를 자동 생성하고 관리하는 통합 서비스.
기존 단일 `ppt-gen` 스킬을 **4개의 전문화된 스킬**과 **1개의 관리 앱**으로 분리하여 모듈성과 확장성을 강화.

### 1.2 핵심 결정사항 (v4.0)

| 항목 | 결정 |
|------|------|
| 아키텍처 | **4 스킬 + 1 앱** (기존 단일 스킬에서 분리) |
| 스킬 네이밍 | **ppt- 접두어 통일** (ppt-extract, ppt-design, ppt-create, ppt-image) |
| 관리 기능 | **Electron 데스크톱 앱** (ppt-manager) |
| 공유 유틸리티 | **ppt-create에 포함** (thumbnail.py, ooxml/) |
| 템플릿 시스템 | **v4.0** (테마, 콘텐츠, 오브젝트, 문서, 에셋) |

### 1.3 타겟 사용자

- **Primary**: 기업/비즈니스 사용자 (제안서, 보고서, 사업계획서)
- **Secondary**: 컨설턴트, 스타트업, 프로젝트 매니저
- **Tertiary**: 디자이너 (템플릿 추출/관리)

---

## 2. 아키텍처

### 2.1 구성 요소 (4 스킬 + 1 앱)

```
┌─────────────────────────────────────────────────────────────────┐
│                        PPT Skills Suite                          │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│ ppt-        │ ppt-        │ ppt-        │ ppt-        │ ppt-    │
│ extract     │ design      │ create      │ image       │ manager │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────┤
│ 콘텐츠 추출  │ PPT 디자인   │ PPT 생성    │ 이미지 생성  │ 관리 앱  │
│ [스킬]      │ [스킬]      │ [스킬]      │ [스킬]      │[Electron]│
│             │             │ + 공유유틸   │             │         │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
```

### 2.2 구성요소 간 의존성

```
                    ┌─────────────────┐
                    │   ppt-extract   │
                    │  (콘텐츠 추출)   │
                    └────────┬────────┘
                             │ templates/contents/
                             │ templates/themes/
                             ▼
┌───────────────┐   ┌─────────────────┐   ┌───────────────┐
│  ppt-manager  │◄──│    templates/    │──►│  ppt-design   │
│  [Electron]   │   │   (공유 저장소)   │   │  (디자인)     │
│               │   └─────────────────┘   └───────────────┘
└───────────────┘            ▲
                             │ registry.yaml
                             │ shapes YAML
                             ▼
                    ┌─────────────────┐
                    │   ppt-create    │
                    │  (PPT 생성)     │
                    │  + 공유 유틸    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   ppt-image     │
                    │  (이미지 생성)   │
                    └─────────────────┘
```

### 2.3 공유 리소스

| 리소스 | 위치 | 읽기 | 쓰기 |
|--------|------|------|------|
| 테마 | `templates/themes/` | 전체 | ppt-extract |
| 콘텐츠 템플릿 | `templates/contents/` | 전체 | ppt-extract, ppt-manager |
| 문서 템플릿 | `templates/documents/` | ppt-create | ppt-extract |
| 에셋 | `templates/assets/` | ppt-create | ppt-manager |
| OOXML 스키마 | `ppt-create/ooxml/schemas/` | ppt-create | (읽기 전용) |
| 썸네일 유틸 | `ppt-create/scripts/thumbnail.py` | 전체 | - |

---

## 3. Claude Code 스킬 (4개)

### 3.1 ppt-extract (콘텐츠 추출)

**책임**: PPT/이미지에서 재사용 가능한 템플릿과 스타일 추출

**워크플로우**:

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `content-extract` | "이 슬라이드 저장해줘" | PPT 슬라이드 → YAML 템플릿 |
| `image-extract` | "이 이미지 레이아웃 추출해줘" | 이미지 → YAML 템플릿 (NEW) |
| `document-extract` | "이 PPT를 양식으로 등록해줘" | 전체 문서 → 문서 템플릿 |
| `style-extract` | "이 이미지 스타일로" | 이미지 → 색상/무드 추출 |

**스크립트**:
- `template-analyzer.py` (528줄) - PPTX → YAML 분석
- `style-extractor.py` (383줄) - 이미지 색상 추출
- `slide-crawler.py` (516줄) - 온라인 슬라이드 크롤링

**출력물**:
- `templates/themes/*.yaml`
- `templates/contents/templates/**/*.yaml`
- `templates/contents/thumbnails/**/*.png`
- `templates/documents/**/*.yaml`

---

### 3.2 ppt-design (PPT 디자인)

**책임**: 디자인 레퍼런스 검색 및 PPT 분석

**워크플로우**:

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `design-search` | "PPT 디자인 찾아줘" | 웹에서 디자인 레퍼런스 검색 |
| `analysis` | "PPT 분석해줘" | PPT 구조/내용 분석 |

**도구**: 주로 LLM Vision + WebSearch 활용

**참조 문서**:
- `references/color-palettes.md` - 컬러 팔레트 가이드
- `references/design-system.md` - 디자인 시스템 규칙

---

### 3.3 ppt-create (PPT 생성)

**책임**: PPT 생성 및 수정 + 공유 유틸리티 제공

**워크플로우**:

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `html2pptx` | "PPT 만들어줘" | HTML → PPTX 변환 |
| `template` | "동국제강 양식으로" | 템플릿 기반 생성 |
| `ooxml` | "이 PPT 수정해줘" | OOXML 직접 편집 |

**스크립트**:
- `html2pptx.js` (1,065줄) - HTML → PPTX 변환
- `inventory.py` (1,020줄) - 텍스트 추출
- `replace.py` (385줄) - 텍스트 교체
- `rearrange.py` (231줄) - 슬라이드 재배열
- `thumbnail.py` (777줄) - **공유 유틸리티** (썸네일 생성)
- `migrate-templates.py` (157줄) - 템플릿 마이그레이션

**OOXML 리소스**:
- `ooxml/scripts/` - unpack.py, pack.py, validate.py
- `ooxml/schemas/` - ISO/ECMA OOXML 스키마 (XSD)

**참조 문서**:
- `references/custom-elements.md` - HTML 요소 스키마
- `references/content-schema.md` - 콘텐츠 템플릿 v4.0 스키마

---

### 3.4 ppt-image (이미지 생성)

**책임**: 이미지/썸네일 생성 및 아이콘 처리

**워크플로우**:

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `thumbnail` | "썸네일 만들어줘" | PPT 썸네일 그리드 생성 |

**스크립트**:
- `image-prompt-generator.js` (289줄) - AI 이미지 프롬프트 생성
- `rasterize-icon.js` (168줄) - SVG → PNG 래스터화

**미구현 기능** (TODO):
- DALL-E/Midjourney/Stable Diffusion 연동
- 프롬프트 → 이미지 자동 생성 파이프라인

---

## 4. ppt-manager (Electron 앱)

### 4.1 기능 요구사항

| 기능 | 설명 | 우선순위 |
|------|------|----------|
| 템플릿 목록 | 썸네일 그리드 뷰 | P0 |
| 템플릿 상세 | 미리보기 + 메타데이터 | P0 |
| 템플릿 삭제/아카이브 | CRUD 작업 | P0 |
| 에셋 추가 | 드래그&드롭 업로드 | P1 |
| 에셋 검색 | 태그/키워드 필터링 | P1 |
| 태그 관리 | 태그 추가/수정/삭제 | P2 |
| 테마 미리보기 | 색상 팔레트 시각화 | P2 |

### 4.2 UI/UX 설계

```
┌─────────────────────────────────────────────────────────────────┐
│  ppt-manager                                          [─][□][×] │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────┐ ┌─────────────────────────────────────────────┐   │
│ │ 사이드바   │ │                 메인 영역                    │   │
│ │           │ │                                             │   │
│ │ ▼ 템플릿   │ │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │   │
│ │   콘텐츠   │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │   문서     │ │  │cover│ │ toc │ │comp │ │proc │ │stat │  │   │
│ │   테마     │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │           │ │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │   │
│ │ ▼ 에셋    │ │                                             │   │
│ │   아이콘   │ │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │   │
│ │   이미지   │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │           │ │  │grid │ │time │ │quote│ │close│ │cycle│  │   │
│ │           │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ └───────────┘ │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │   │
│               └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ 검색: [________________] 카테고리: [전체 ▼] 테마: [전체 ▼]       │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 기술 스택

| 영역 | 기술 |
|------|------|
| 프레임워크 | Electron + React |
| 상태관리 | Zustand 또는 Jotai |
| UI 라이브러리 | Tailwind CSS + Radix UI |
| 빌드 | Vite + electron-builder |
| Python 연동 | child_process (spawn) |
| 데이터 캐싱 | SQLite (선택적) |

### 4.4 데이터 흐름

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│  IPC Handler    │────▶│  Python Script  │
│                 │     │  (Electron)     │     │                 │
│  TemplateGrid   │◀────│  templates.ts   │◀────│  template-      │
│  AssetLibrary   │     │  assets.ts      │     │  manager.py     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │  templates/     │
                        │  (파일 시스템)   │
                        └─────────────────┘
```

---

## 5. 템플릿 시스템 (v4.0)

### 5.1 테마 (themes/)

**경로**: `templates/themes/`

**파일 목록** (4개):
- `default.yaml` - 기본 블루 테마
- `deepgreen.yaml` - 자연/친환경 테마
- `brandnew.yaml` - 신선한 스카이블루 테마
- `동국.yaml` - 동국그룹 브랜드 테마

**구조**:
```yaml
theme:
  id: deepgreen
  name: "Deep Green"
  description: "자연스럽고 깔끔한 딥그린 테마"

colors:
  primary: "#1E5128"      # 주요 강조색
  secondary: "#4E9F3D"    # 보조 강조색
  accent: "#D8E9A8"       # 하이라이트
  background: "#FFFFFF"   # 배경색
  surface: "#F4F6F6"      # 카드/패널 배경
  dark_text: "#191A19"    # 본문 텍스트
  light: "#FFFFFF"        # 밝은 텍스트
  gray: "#AAB7B8"         # 음소거 요소

typography:
  heading_font: "Arial"
  body_font: "Arial"
  korean_font: "Malgun Gothic"

style_hints:
  rounded_corners: 8
  shadow_blur: 4
```

---

### 5.2 콘텐츠 템플릿 (contents/)

**경로**: `templates/contents/`

**레지스트리**: `registry.yaml`
```yaml
version: "4.0"
default_theme: deepgreen

categories:
  - id: cover      # 표지
  - id: toc        # 목차
  - id: section    # 섹션 구분
  - id: comparison # 비교/대조
  - id: process    # 프로세스
  - id: chart      # 차트
  - id: stats      # 통계
  - id: grid       # 그리드
  - id: diagram    # 다이어그램
  - id: timeline   # 타임라인
  - id: content    # 일반 콘텐츠
  - id: quote      # 인용문
  - id: closing    # 마무리
  - id: cycle      # 순환
  - id: matrix     # 매트릭스
  - id: feature    # 기능
  - id: flow       # 플로우
  - id: table      # 테이블

templates:
  - id: cover-centered1
    name: "표지 (중앙 정렬)"
    file: templates/cover/cover-centered1.yaml
    thumbnail: thumbnails/cover/cover-centered1.png
    category: cover
    design_intent: cover-centered
    use_for: [표지, 타이틀]
    prompt_keywords: [표지, 타이틀, 중앙정렬]
```

**템플릿 파일 구조 (v4.0)**:
```yaml
content_template:
  id: comparison-2col1
  name: "2열 비교"
  version: "4.0"

design_meta:
  quality_score: 9.2
  design_intent: comparison-2col

canvas:
  reference_width: 1920
  reference_height: 1080

content:
  layout:
    type: grid
    columns: 2

  zones:
    - id: left-panel
      type: container
      geometry: {x: 2%, y: 15%, cx: 46%, cy: 80%}
      style_ref: primary-fill
      object_desc: "둥근 모서리 사각형 배경"

    - id: right-panel
      type: container
      geometry: {x: 52%, y: 15%, cx: 46%, cy: 80%}
      style_ref: secondary-fill
      object_desc: "둥근 모서리 사각형 배경"

  spacing:
    column_gap: 4%
    row_gap: 3%
```

**카테고리별 템플릿 수** (40개+):

| 카테고리 | 개수 | 예시 |
|----------|------|------|
| cover | 3 | cover-centered1, cover-photo1, cover-simple1 |
| toc | 3 | toc-3col1, toc-list-image1, toc-simple1 |
| section | 2 | section-number1, section-textured1 |
| comparison | 4 | comparison-2col1, pros-cons1 |
| process | 5 | process-flow1, process-honeycomb1 |
| chart | 2 | chart-bar-table1 |
| stats | 2 | stats-dotgrid1, stat-cards1 |
| grid | 3 | grid-4col-icon1, grid-3col-image1 |
| diagram | 6 | matrix-2x21, cycle-circular1, venn-4segment1 |
| timeline | 1 | timeline1 |
| content | 1 | image-text1 |
| quote | 1 | quote-centered1 |
| closing | 1 | closing-thankyou1 |
| cycle | 2 | cycle-4arrow1, cycle-6segment-colorful1-v3 |
| matrix | 1 | venn-4segment1 |
| feature | 1 | feature-center-icon1 |
| flow | 1 | flow-circular-apple1 |
| table | 1 | table-comparison-3col1 |

---

### 5.3 문서 템플릿 (documents/)

**경로**: `templates/documents/{그룹}/`

**구조**:
```
documents/dongkuk/
├── config.yaml          # 그룹 테마
├── registry.yaml        # 양식 목록
├── 제안서1.yaml         # 양식 정의
└── assets/              # 계열사 로고
    └── dongkuk-steel/
```

**config.yaml**:
```yaml
group:
  id: dongkuk
  name: 동국그룹

theme:
  colors:
    primary: "#002452"
    secondary: "#C51F2A"
  fonts:
    title: "본고딕 Bold"
    body: "본고딕 Normal"

companies:
  - id: dongkuk-steel
  - id: dongkuk-cm
```

**양식 파일** (제안서1.yaml):
```yaml
document:
  id: 제안서1
  name: "제안서 (기본)"
  type: proposal

slides:
  - index: 0
    category: cover
    placeholders:
      - id: title
        font_size: 32pt
  - index: 1
    category: toc
  - index: 2
    category: body
    name: "내지(불릿)"

llm_layout_guide:
  cover: 0
  toc: 1
  bullets: 2
  chart: 3
  text_heavy: 4
```

---

### 5.4 에셋 (assets/)

**경로**: `templates/assets/`

**icon-mappings.yaml**:
```yaml
mappings:
  보안:
    icon: "fa/FaShieldAlt"
    aliases: ["security", "안전"]
  AI:
    icon: "fa/FaBrain"
    aliases: ["인공지능", "머신러닝"]
  성장:
    icon: "fa/FaChartLine"
    aliases: ["growth", "증가"]

categories:
  technology:
    default: "fa/FaMicrochip"
  business:
    default: "fa/FaBriefcase"
```

**image-prompt-templates.yaml**:
```yaml
templates:
  hero:
    base: "Professional, impactful hero image"
    modifiers: ["high contrast", "bold composition"]
    aspect_ratio: "16:9"
  background:
    base: "Subtle, elegant background pattern"
    modifiers: ["minimal", "soft gradients"]

industry_styles:
  tech: ["sleek", "innovative", "digital"]
  finance: ["professional", "trustworthy"]
```

---

### 5.5 YAML 파일별 역할 정의

| 파일 | 역할 | 읽기 스킬 | 쓰기 스킬 |
|------|------|----------|----------|
| `themes/*.yaml` | 테마 정의 (색상, 폰트) | 전체 | ppt-extract |
| `contents/registry.yaml` | 콘텐츠 템플릿 인덱스 | 전체 | ppt-extract, ppt-manager |
| `contents/templates/**/*.yaml` | 슬라이드 레이아웃 패턴 | ppt-create, ppt-design | ppt-extract |
| `contents/objects/registry.yaml` | 오브젝트 레지스트리 (NEW) | ppt-create | ppt-extract |
| `contents/objects/**/*.yaml` | 오브젝트 정의 (NEW) | ppt-create | ppt-extract |
| `documents/*/config.yaml` | 그룹/회사 테마 | ppt-create | ppt-extract |
| `documents/*/registry.yaml` | 문서 양식 목록 | ppt-create | ppt-extract |
| `documents/*/*.yaml` | 문서 구조 정의 | ppt-create | ppt-extract |
| `assets/icon-mappings.yaml` | 키워드→아이콘 매핑 | ppt-create | ppt-manager |
| `assets/image-prompt-templates.yaml` | AI 이미지 프롬프트 | ppt-image | - |

---

### 5.6 오브젝트 라이브러리 (objects/) - NEW v4.0

**경로**: `templates/contents/objects/`

**구조**:
```
objects/
├── registry.yaml           # 오브젝트 레지스트리
├── cycle/
│   ├── 6segment-colorful.yaml
│   └── 4arrow.yaml
├── honeycomb/
│   └── process-hex.yaml
├── arrows/
│   └── curved-arrows.yaml
├── icons/
│   └── fa-icons.yaml
└── images/
    └── hero-backgrounds.yaml
```

**registry.yaml**:
```yaml
version: "1.0"

objects:
  - id: cycle-6segment-colorful
    file: cycle/6segment-colorful.yaml
    type: ooxml
    metadata:
      category: cycle
      tags: [colorful, segmented, 6-element, process]
      semantic: "6단계 순환 다이어그램"
      element_count: 6
      complexity: high
      style: colorful

  - id: cycle-4arrow
    file: cycle/4arrow.yaml
    type: svg
    metadata:
      category: cycle
      semantic: "4단계 순환 화살표"
      element_count: 4
      complexity: medium
```

**오브젝트 타입**:

| 타입 | 설명 | 용도 |
|------|------|------|
| `ooxml` | PPTX 네이티브 도형 | 복잡한 다이어그램 |
| `svg` | 벡터 그래픽 | 확장 가능한 도형 |
| `image` | 래스터 이미지 | 배경, 사진 |
| `description` | 텍스트 설명만 | 간단한 도형 (LLM 생성) |

---

## 6. 콘텐츠-오브젝트 분리 스키마 (v4.0)

### 6.1 핵심 개념

v4.0에서는 **콘텐츠**(배치)와 **오브젝트**(도형)를 분리하여 재사용성과 유연성을 높입니다.

```
┌─────────────────────────────────────────┐
│ CONTENT (콘텐츠)                         │
│ - 배치, 여백, 구조                       │
│ - "어디에" 배치할 것인가?                │
│ - zones[] 기반                          │
└─────────────────────────────────────────┘
                     │
                     │ 동적 참조
                     ▼
┌─────────────────────────────────────────┐
│ OBJECT (오브젝트)                        │
│ - 실제 도형/이미지 정의                  │
│ - "무엇을" 그릴 것인가?                  │
│ - 4가지 타입: OOXML, SVG, Image, Desc   │
└─────────────────────────────────────────┘
```

### 6.2 동적 오브젝트 선택 시스템

기존 고정 참조(`object_ref`)의 한계를 극복하기 위해 **3계층 참조 시스템**을 도입합니다.

**Zone 스키마**:
```yaml
zones:
  - id: main-diagram
    type: placeholder
    geometry: {x: 10%, y: 20%, cx: 80%, cy: 60%}
    placeholder_type: DIAGRAM

    # 1. 동적 검색 (LLM이 registry에서 최적 오브젝트 선택)
    object_hint:
      category: [cycle, process]
      semantic: "순환 프로세스"
      element_count: 4-6
      style: colorful

    # 2. 폴백 (검색 실패 시)
    object_default: "objects/cycle/6segment-colorful.yaml"

    # 3. 간단한 도형 (설명 기반 생성)
    object_desc: null
```

**선택 우선순위**:
1. `object_hint` 있음 → Registry 검색 → 최적 오브젝트 선택
2. 매칭 실패 → `object_default` 사용
3. `object_desc`만 있음 → LLM이 설명 기반 생성
4. 모두 없음 → 텍스트 플레이스홀더만

### 6.3 LLM 오브젝트 선택 흐름

```
사용자: "4단계 순환 프로세스 PPT 만들어줘"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. 콘텐츠 분석 & 템플릿 선택                                  │
│    - 콘텐츠: "순환 프로세스" → category: cycle               │
│    - 템플릿: process-visual1 선택                           │
│    - object_hint: {category: cycle, element_count: 4}       │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 오브젝트 Registry 검색                                    │
│    Query: category=cycle, element_count=4                   │
│                                                             │
│    결과:                                                     │
│    ┌──────────────────────┬────────────┬──────────┐         │
│    │ 오브젝트             │ 매칭 점수  │ 선택     │         │
│    ├──────────────────────┼────────────┼──────────┤         │
│    │ cycle-4arrow         │ 95%        │ ✓        │         │
│    │ cycle-6segment       │ 60%        │          │         │
│    └──────────────────────┴────────────┴──────────┘         │
└─────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PPT 생성                                                 │
│    - 콘텐츠 geometry로 위치 결정                             │
│    - 선택된 오브젝트(cycle-4arrow)로 렌더링                   │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 유연성 모드

| 모드 | 설명 | 스키마 설정 |
|------|------|------------|
| **고정** | 특정 오브젝트만 사용 | `object_default` only |
| **검색** | LLM이 최적 선택 | `object_hint` + `object_default` |
| **자유** | 설명 기반 생성 | `object_desc` only |
| **혼합** | 힌트 + 설명 | `object_hint` + `object_desc` |

### 6.5 v3.0 → v4.0 마이그레이션

| 항목 | v3.0 | v4.0 |
|------|------|------|
| 배치+도형 | `shapes[]` 혼재 | `zones[]` + `objects/` 분리 |
| 복잡한 도형 | 3중 저장 (path, inline, shapes) | 오브젝트 파일 단일 저장 |
| 오브젝트 참조 | 없음 (직접 정의) | `object_hint`, `object_default`, `object_desc` |
| 재사용성 | 템플릿 단위 | 오브젝트 단위 재사용 가능 |

**호환성 전략**:
```yaml
content_template:
  version: "4.0"
  legacy_shapes: [...]  # v3.0 shapes 유지 (deprecated)
  content: {...}        # v4.0 새 구조
```

---

## 7. 디자인 토큰 시스템

### 7.1 토큰 목록

| 토큰 | 용도 | 예시 값 (deepgreen) |
|------|------|---------------------|
| `primary` | 주요 강조색 | #1E5128 |
| `secondary` | 보조 강조색 | #4E9F3D |
| `accent` | 하이라이트 | #D8E9A8 |
| `background` | 배경색 | #FFFFFF |
| `surface` | 카드/패널 배경 | #F4F6F6 |
| `dark_text` | 본문 텍스트 | #191A19 |
| `light` | 밝은 텍스트 | #FFFFFF |
| `gray` | 음소거 요소 | #AAB7B8 |

### 7.2 테마 적용 흐름

```
콘텐츠 템플릿 (디자인 토큰)
         │
         │ style.fill.color: primary
         ▼
    테마 선택 (deepgreen)
         │
         │ colors.primary: "#1E5128"
         ▼
    HTML 생성 (실제 색상)
         │
         │ background-color: #1E5128
         ▼
    PPTX 변환
```

---

## 8. Template Priority Rule

PPT 생성 시 **필수** 준수 프로세스:

```
1. 슬라이드 목록 작성
   └─ 콘텐츠 분석 → 슬라이드 유형/키워드 정리

2. registry.yaml 검색
   └─ 각 슬라이드별 매칭 템플릿 찾기

3. 매칭 결과 테이블 작성 (필수 출력물)
   ┌─────────┬──────────────┬─────────────────┐
   │ 슬라이드 │ 콘텐츠 유형   │ 매칭 템플릿      │
   ├─────────┼──────────────┼─────────────────┤
   │ 1       │ 표지         │ cover-centered1 │
   │ 2       │ 목차         │ toc-3col1       │
   │ 3       │ A vs B       │ comparison-2col1│
   └─────────┴──────────────┴─────────────────┘

4. 템플릿 YAML 로드
   └─ 매칭된 템플릿의 shapes[] 구조 참조

5. HTML 생성
   └─ 템플릿 geometry/style → HTML 변환
```

**금지사항**: registry.yaml 검색 없이 직접 디자인 (매칭 불가 시에만 허용)

---

## 9. 스크립트 목록 및 배분

### 전체 스크립트 (13개, 6,783줄)

| 스크립트 | 줄수 | 배분 스킬 | 역할 |
|---------|------|----------|------|
| html2pptx.js | 1,065 | ppt-create | HTML → PPTX 변환 |
| inventory.py | 1,020 | ppt-create | 텍스트 추출 |
| asset-manager.py | 819 | ppt-manager (앱) | 에셋 관리 |
| thumbnail.py | 777 | ppt-create (공유) | 썸네일 생성 |
| template-analyzer.py | 528 | ppt-extract | PPTX → YAML 분석 |
| slide-crawler.py | 516 | ppt-extract | 온라인 슬라이드 크롤링 |
| template-manager.py | 445 | ppt-manager (앱) | 템플릿 관리 |
| replace.py | 385 | ppt-create | 텍스트 교체 |
| style-extractor.py | 383 | ppt-extract | 색상 추출 |
| image-prompt-generator.js | 289 | ppt-image | 이미지 프롬프트 생성 |
| rearrange.py | 231 | ppt-create | 슬라이드 재배열 |
| rasterize-icon.js | 168 | ppt-image | SVG 래스터화 |
| migrate-templates.py | 157 | ppt-create | 템플릿 마이그레이션 |

---

## 10. 기술 스택 및 의존성

### Claude Code 스킬

**Node.js**:
- pptxgenjs - PPTX 생성
- playwright - HTML 렌더링
- sharp - 이미지 처리
- react-icons - 아이콘 라이브러리

**Python**:
- python-pptx - PPTX 편집
- pyyaml - YAML 파싱
- markitdown - 문서 변환
- defusedxml - XML 파싱
- Pillow - 이미지 처리
- colorthief - 색상 추출

**시스템**:
- LibreOffice (soffice) - PPTX → PDF 변환
- Poppler (pdftoppm) - PDF → 이미지 변환

### ppt-manager (Electron 앱)

- Electron 28+
- React 18+
- Vite
- Tailwind CSS
- Radix UI
- electron-builder

---

## 11. 구현 현황 및 로드맵

### 11.1 완료된 기능 (95%)

| 영역 | 상태 | 설명 |
|------|------|------|
| html2pptx 파이프라인 | ✅ | HTML → PPTX 변환 |
| 템플릿 기반 생성 | ✅ | 문서 템플릿 사용 |
| OOXML 편집 | ✅ | 기존 PPT 수정 |
| 콘텐츠 템플릿 추출 | ✅ | v2.0 스키마 |
| 문서 템플릿 추출 | ✅ | 회사별 양식 등록 |
| 스타일 추출 | ✅ | 이미지 색상 분석 |
| 디자인 검색 | ✅ | 웹 레퍼런스 검색 |
| 템플릿 관리 | ✅ | CLI 기반 CRUD |
| 에셋 관리 | ✅ | CLI 기반 CRUD |
| 썸네일 생성 | ✅ | 검증용 이미지 |
| 3타입 템플릿 시스템 | ✅ | 테마/콘텐츠/문서/에셋 |
| 디자인 토큰 | ✅ | 테마 독립적 템플릿 |

### 11.2 미완료 기능 (5%)

| 기능 | 상태 | 설명 |
|------|------|------|
| AI 이미지 생성 연동 | ❌ | DALL-E/Midjourney 연결 |
| ppt-manager Electron 앱 | ⬜ | GUI 관리 앱 신규 개발 |
| 스킬 분리 | ⬜ | 4개 스킬로 재구성 |

---

## 12. 사용 예시

### ppt-extract 사용

```
사용자: "이 슬라이드 저장해줘" [PPT 파일 첨부]

Claude:
1. 슬라이드 분석 → 디자인 의도 파악
2. template-analyzer.py 실행
3. YAML 템플릿 생성
4. registry.yaml 업데이트
5. 썸네일 생성 및 저장
```

### ppt-create 사용

```
사용자: "스마트 물류 시스템 제안서 PPT 만들어줘"

Claude:
1. 콘텐츠 분석 → 슬라이드 구조 설계
2. registry.yaml 검색 → 템플릿 매칭
3. 테마 선택 (deepgreen)
4. HTML 슬라이드 생성
5. html2pptx.js 실행
6. 썸네일 검증 및 결과 전달
```

### ppt-manager 사용 (Electron 앱)

```
1. 앱 실행 → 템플릿 그리드 표시
2. 카테고리 필터 (comparison)
3. 템플릿 클릭 → 상세 정보 확인
4. "아카이브" 버튼 클릭 → 비활성화
5. 에셋 탭 → 새 아이콘 드래그&드롭
```

---

## 부록

### A. YAML 스키마 정의

콘텐츠 템플릿 v4.0 스키마: `ppt-create/references/content-schema.md` 참조

### B. 콘텐츠 템플릿 카테고리 (19개)

cover, toc, section, comparison, process, chart, stats, grid, diagram, timeline, content, quote, closing, cycle, matrix, feature, flow, table, infographic

### C. 아이콘 매핑 목록

46개 키워드 → 아이콘 매핑: `templates/assets/icon-mappings.yaml` 참조

### D. ppt-manager 화면 설계

섹션 4.2 UI/UX 설계 참조

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 3.0 | 2026-01-06 | 초기 PRD (단일 ppt-gen 스킬) |
| 4.0 | 2026-01-08 | 4 스킬 + 1 앱 분리 구조로 재설계 |
| 4.1 | 2026-01-08 | 콘텐츠-오브젝트 분리 스키마 추가, 동적 오브젝트 선택 시스템 |
| 4.2 | 2026-01-08 | 문서 전체 v4.0 버전 참조 통일, 템플릿 예시 v4.0 스키마로 업데이트 |
