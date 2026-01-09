# PRD: PPT Skills Suite

**버전**: 5.5
**작성일**: 2026-01-09
**상태**: Draft

### 변경 이력
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 5.5 | 2026-01-09 | 1단계 Setup에 사전 질문(AskUserQuestion) 필수화 추가 |
| 5.4 | 2026-01-09 | 5단계 파이프라인 스키마 v5.5 업데이트 |

---

## 1. 개요

### 1.1 제품 비전

Claude Code 환경에서 **전문 디자이너 수준의 PPT**를 자동 생성하고 관리하는 통합 서비스.
**2개 스킬 + 1 앱** 구조: `ppt-extract`(추출) + `ppt-gen`(생성) + `ppt-manager`(관리).

### 1.2 핵심 결정사항 (v4.7)

| 항목 | 결정 |
|------|------|
| 아키텍처 | **2개 스킬 + 1 앱**: ppt-extract (추출) + ppt-gen (생성) + ppt-manager (관리) |
| 기능 분류 | **추출 스킬** (파이프라인 외부) + **생성 스킬** (5단계 파이프라인) |
| 관리 기능 | **CLI 기반** (미래: Electron 데스크톱 앱) |
| 템플릿 시스템 | **v4.0** (테마, 콘텐츠, 오브젝트, 문서, 에셋) |

### 1.3 타겟 사용자

- **Primary**: 기업/비즈니스 사용자 (제안서, 보고서, 사업계획서)
- **Secondary**: 컨설턴트, 스타트업, 프로젝트 매니저
- **Tertiary**: 디자이너 (템플릿 추출/관리)

---

## 2. 아키텍처

### 2.1 2개 스킬 + 1 앱 구조

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PPT Skills Suite (2개 스킬 + 1 앱)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ppt-extract (추출 스킬) - 파이프라인 외부                          │   │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                               │   │
│  │ • content-extract  : 콘텐츠/오브젝트 추출 (PPTX, 이미지)           │   │
│  │ • document-extract : 문서 양식 추출 (슬라이드 마스터, 로고)         │   │
│  │ • style-extract    : 테마 추출                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              │ 템플릿/에셋 등록                         │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ppt-gen (생성 스킬) - 5단계 파이프라인                             │   │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                              │   │
│  │ • html2pptx : 새 PPT 생성 (5단계 파이프라인 실행)                  │   │
│  │ • template  : 템플릿 기반 생성                                    │   │
│  │ • ooxml     : 기존 PPT 수정                                       │   │
│  │ • analysis  : PPT 분석                                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ ppt-manager (Electron 앱) - 관리 기능                             │   │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                               │   │
│  │ • 템플릿 관리 (목록/아카이브/삭제)                                  │   │
│  │ • 에셋 관리 (추가/검색/삭제)                                       │   │
│  │ • 디자인 레퍼런스 검색                                             │   │
│  │ • 썸네일 생성/미리보기                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 역할 분류

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ppt-extract (추출 스킬) - 템플릿/에셋 준비                               │
├─────────────────────────────────────────────────────────────────────────┤
│ PPT 생성 파이프라인과 독립적으로 실행. 결과물은 templates/ 폴더에 저장.   │
│                                                                         │
│ ┌─────────────────┬────────────────────┬─────────────────────────────┐ │
│ │ 워크플로우       │ 입력               │ 출력                         │ │
│ ├─────────────────┼────────────────────┼─────────────────────────────┤ │
│ │ style-extract   │ 이미지             │ themes/*.yaml              │ │
│ │ content-extract │ PPTX, 이미지       │ 콘텐츠 YAML, 오브젝트 YAML   │ │
│ │ document-extract│ PPTX               │ 문서 템플릿, 슬라이드 마스터  │ │
│ └─────────────────┴────────────────────┴─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              │ 추출된 템플릿/에셋
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ ppt-gen (생성 스킬) - 5단계 파이프라인                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 추출된 템플릿/에셋을 활용하여 PPT 생성. → 섹션 14 참조                    │
│                                                                         │
│ ┌─────────────────┬────────────────────────────────────────────────┐   │
│ │ 생성           │ html2pptx, template, ooxml                      │   │
│ ├─────────────────┼────────────────────────────────────────────────┤   │
│ │ 분석           │ analysis                                        │   │
│ └─────────────────┴────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              │ 생성된 PPT
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ ppt-manager (Electron 앱) - 관리 기능                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┬────────────────────────────────────────────────┐   │
│ │ 템플릿 관리      │ 목록 조회, 아카이브, 삭제                        │   │
│ ├─────────────────┼────────────────────────────────────────────────┤   │
│ │ 에셋 관리       │ 추가, 검색, 삭제                                 │   │
│ ├─────────────────┼────────────────────────────────────────────────┤   │
│ │ 디자인 검색      │ 웹에서 디자인 레퍼런스 검색                       │   │
│ ├─────────────────┼────────────────────────────────────────────────┤   │
│ │ 미리보기        │ 썸네일 생성, PPT 미리보기                         │   │
│ └─────────────────┴────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.3 공유 리소스

| 리소스 | 위치 | 설명 |
|--------|------|------|
| 테마 | `templates/themes/` | 색상/폰트 정의 |
| 콘텐츠 템플릿 | `templates/contents/` | 슬라이드 레이아웃 패턴 |
| 오브젝트 | `templates/contents/objects/` | 재사용 가능한 도형 |
| 문서 템플릿 | `templates/documents/` | 회사별 양식 |
| 에셋 | `templates/assets/` | 아이콘, 이미지 |
| OOXML 스키마 | `ooxml/schemas/` | ISO/ECMA 스키마 (읽기 전용) |

---

## 3. 스킬 정의

### 3.1 ppt-extract 스킬 (추출)

템플릿과 에셋을 준비하는 스킬입니다. PPT 생성 파이프라인과 독립적으로 실행됩니다.

| 워크플로우 | 트리거 | 입력 | 출력 |
|-----------|--------|------|------|
| `content-extract` | "이 슬라이드 저장해줘" | PPTX, 이미지 | 콘텐츠 YAML, 오브젝트 YAML |
| `document-extract` | "이 PPT를 양식으로 등록해줘" | PPTX | 문서 템플릿 YAML, OOXML, 에셋 |
| `style-extract` | "이 이미지 스타일로" | 이미지 | 테마 YAML |

**document-extract 출력물**:
```
templates/documents/{group}/
├── {template-id}.yaml     # 양식 정의 (레이아웃, 이미지 매핑)
├── config.yaml            # 테마 색상/폰트
├── registry.yaml          # 양식 목록
├── assets/default/        # 로고, 아이콘, 배경 이미지
└── ooxml/                 # 원본 OOXML (ppt-gen에서 재사용)
    ├── slideLayoutN.xml   # 레이아웃 정의
    ├── slideMaster1.xml   # 슬라이드 마스터
    ├── theme1.xml         # 테마
    └── _rels/             # 이미지 참조 관계 파일
```

**스크립트**:
- `template-analyzer.py` (750줄+) - PPTX → YAML/OOXML 추출
- `style-extractor.py` (383줄) - 이미지 색상 추출
- `slide-crawler.py` (516줄) - 온라인 슬라이드 크롤링

### 3.2 플레이스홀더 추출 방법 (document-extract)

PPTX 문서 양식 추출 시 **슬라이드 레이아웃**에서 플레이스홀더 정보를 추출합니다.

#### 3.2.1 추출 소스

| 소스 파일 | 경로 | 설명 |
|----------|------|------|
| 슬라이드 레이아웃 | `ppt/slideLayouts/slideLayout*.xml` | 각 레이아웃의 플레이스홀더 정의 |
| 슬라이드 마스터 | `ppt/slideMasters/slideMaster1.xml` | 공통 플레이스홀더 (로고, 푸터) |
| 관계 파일 | `ppt/slideLayouts/_rels/*.xml.rels` | 이미지 참조 매핑 |

#### 3.2.2 플레이스홀더 XML 구조

```xml
<!-- ppt/slideLayouts/slideLayout1.xml -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <!-- 플레이스홀더 타입과 인덱스 -->
      <p:ph type="title" idx="0"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <!-- 위치와 크기 (EMU 단위) -->
      <a:off x="457200" y="274638"/>
      <a:ext cx="8229600" cy="1143000"/>
    </a:xfrm>
  </p:spPr>
</p:sp>
```

#### 3.2.3 EMU → % 변환

```python
# 슬라이드 기본 크기 (EMU): 10" x 7.5"
slide_width_emu = 9144000
slide_height_emu = 6858000

# EMU → 퍼센트 변환
x_percent = round(x_emu / slide_width_emu * 100, 1)
y_percent = round(y_emu / slide_height_emu * 100, 1)
width_percent = round(cx_emu / slide_width_emu * 100, 1)
height_percent = round(cy_emu / slide_height_emu * 100, 1)
```

#### 3.2.4 플레이스홀더 타입 (PPTX 표준)

| type | idx | 역할 | 용도 |
|------|-----|------|------|
| `title` | 0 | 슬라이드 제목 | 일반 슬라이드 제목 |
| `ctrTitle` | - | 중앙 제목 | 표지 슬라이드 |
| `subTitle` | - | 부제목 | 표지, 섹션 구분 |
| `body` | 1 | 본문 텍스트 | 불릿 포인트, 내용 |
| `pic` | - | 이미지 영역 | 사진, 그래픽 |
| `chart` | - | 차트 영역 | 데이터 시각화 |
| `tbl` | - | 표 영역 | 데이터 테이블 |
| `dgm` | - | 다이어그램 | SmartArt |
| `sldNum` | 12 | 슬라이드 번호 | 페이지 번호 |
| `ftr` | 10 | 바닥글 | 푸터 텍스트 |
| `dt` | 11 | 날짜/시간 | 날짜 표시 |

#### 3.2.5 추출 결과 YAML 예시

```yaml
# templates/documents/dongkuk-systems/기본양식.yaml
layouts:
  - index: 1
    name: "표지 (White Big)"
    category: cover
    use_for: "문서 제목, 발표 표지"
    keywords: [표지, 제목, 타이틀, 커버]
    placeholders:
      - type: ctrTitle
        role: "중앙 제목"
        position:
          x: 5.0%
          y: 35.0%
          width: 90.0%
          height: 15.0%
      - type: subTitle
        role: "부제목"
        position:
          x: 5.0%
          y: 52.0%
          width: 90.0%
          height: 8.0%
    images:
      - rId: rId2
        file: "assets/default/image2.png"
    ooxml_ref: "ooxml/slideLayout1.xml"
```

#### 3.2.6 ppt-gen에서 활용

추출된 플레이스홀더 정보는 PPT 생성 시 다음과 같이 활용됩니다:

1. **레이아웃 선택**: `category`, `keywords`로 콘텐츠에 맞는 레이아웃 매칭
2. **콘텐츠 배치**: `position`으로 텍스트/이미지 배치 위치 결정
3. **OOXML 편집**: `ooxml_ref`로 원본 XML 로드 후 텍스트 치환
4. **이미지 복원**: `images[].rId` → `assets/default/` 파일 매핑

---

## 4. ppt-gen 스킬 (생성)

### 4.1 생성 워크플로우 (5단계 파이프라인)

새로운 PPT를 생성하거나 기존 PPT를 수정하는 워크플로우입니다.

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `html2pptx` | "PPT 만들어줘" | **5단계 파이프라인 실행** (섹션 14 참조) |
| `template` | "동국제강 양식으로" | 템플릿 기반 생성 |
| `ooxml` | "이 PPT 수정해줘" | OOXML 직접 편집 |

**스크립트**:
- `html2pptx.js` (1,065줄) - HTML → PPTX 변환
- `inventory.py` (1,020줄) - 텍스트 추출
- `replace.py` (385줄) - 텍스트 교체
- `rearrange.py` (231줄) - 슬라이드 재배열

---

### 4.2 분석 워크플로우

| 워크플로우 | 트리거 | 설명 |
|-----------|--------|------|
| `analysis` | "PPT 분석해줘" | PPT 구조/내용 분석 |

**도구**: LLM Vision 활용

---

### 4.3 이미지 생성 (미구현)

| 워크플로우 | 트리거 | 상태 |
|-----------|--------|------|
| (미정) | "이미지 생성해줘" | ❌ 미구현 |

**미구현 기능** (TODO):
- DALL-E/Midjourney/Stable Diffusion 연동
- 프롬프트 → 이미지 자동 생성 파이프라인

**현재 사용 가능**:
- `image-prompt-generator.js` (289줄) - AI 이미지 프롬프트 생성 (프롬프트만)
- `rasterize-icon.js` (168줄) - SVG → PNG 래스터화

---

### 3.6 참조 문서

| 문서 | 설명 |
|------|------|
| `references/custom-elements.md` | HTML 요소 스키마 |
| `references/content-schema.md` | 콘텐츠 템플릿 v4.0 스키마 |
| `references/color-palettes.md` | 컬러 팔레트 가이드 |
| `references/design-system.md` | 디자인 시스템 규칙 |

---

## 5. ppt-manager (Electron 앱)

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

## 6. 템플릿 시스템 (v4.0)

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

**레지스트리 (v4.1 분리형)**:

```
templates/contents/
├── registry.yaml              # 마스터 (인덱스): 카테고리 목록 + 통계
├── registry-chart.yaml        # 차트 카테고리 템플릿
├── registry-closing.yaml      # 마무리 카테고리 템플릿
├── registry-comparison.yaml   # 비교 카테고리 템플릿
├── registry-content.yaml      # 콘텐츠 카테고리 템플릿
├── registry-cycle.yaml        # 사이클 카테고리 템플릿
├── registry-diagram.yaml      # 다이어그램 카테고리 템플릿
├── registry-grid.yaml         # 그리드 카테고리 템플릿
├── registry-hierarchy.yaml    # 계층 카테고리 템플릿
├── registry-matrix.yaml       # 매트릭스 카테고리 템플릿
├── registry-process.yaml      # 프로세스 카테고리 템플릿
├── registry-stats.yaml        # 통계 카테고리 템플릿
├── registry-table.yaml        # 테이블 카테고리 템플릿
└── registry-timeline.yaml     # 타임라인 카테고리 템플릿
```

**마스터 registry.yaml**:
```yaml
version: "4.1"
type: index
categories:
  chart:
    name: 차트
    description: 차트/그래프 레이아웃
    file: registry-chart.yaml
    count: 3
  comparison:
    name: 비교
    description: 비교 레이아웃
    file: registry-comparison.yaml
    count: 2
  # ... 13개 카테고리
stats:
  total_templates: 28
  total_categories: 12
```

**카테고리별 registry-{category}.yaml**:
```yaml
category: comparison
name: 비교
description: 비교 레이아웃
version: "4.1"

templates:
  - id: comparison-2col1
    name: 2열 불릿 비교
    file: templates/comparison/comparison-2col1.yaml
    thumbnail: thumbnails/comparison/comparison-2col1.png
    source_slide_index: 2
    # 검색 메타데이터
    description: "좌우 2열 대칭 구조로 두 항목 비교"
    match_keywords: [비교, 장단점, vs, 대조, 좌우, 2열, comparison]
    expected_prompt: |
      비교 슬라이드를 만들어줘.
      - 좌우 2열로 배치
      - 각 열에 중제목 + 불릿 포인트 리스트
```

**동기화 스크립트**: `.claude/skills/ppt-gen/scripts/sync_registry.py`
- 개별 템플릿 YAML → 분리형 registry 자동 생성
- 사용: `python sync_registry.py [--dry-run] [--test "검색어"]`

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
├── config.yaml              # 그룹 테마 (색상, 폰트)
├── registry.yaml            # 양식 목록
├── 제안서1.yaml             # 양식 정의
├── assets/                  # 미디어 에셋
│   └── default/
│       ├── image1.emf       # 로고
│       ├── image2.png       # 아이콘
│       └── image3.png       # 배경 이미지
└── ooxml/                   # 원본 OOXML (ppt-gen에서 재사용)
    ├── slideLayout1.xml     # 레이아웃 정의
    ├── slideLayout2.xml
    ├── ...
    ├── slideMaster1.xml     # 슬라이드 마스터 (공통 요소)
    ├── theme1.xml           # 테마 (색상/폰트 정의)
    └── _rels/               # 관계 파일 (이미지 참조 매핑)
        ├── slideLayout1.xml.rels
        ├── slideLayout2.xml.rels
        ├── ...
        └── slideMaster1.xml.rels
```

**OOXML 파일 역할**:

| 파일 | 역할 | ppt-gen 사용 |
|------|------|--------------|
| `slideLayoutN.xml` | 레이아웃 구조, 플레이스홀더 정의 | 슬라이드 생성 시 레이아웃 적용 |
| `slideMaster1.xml` | 공통 요소 (로고, 배경, 텍스트 스타일) | 마스터 복사하여 사용 |
| `theme1.xml` | 색상 팔레트, 폰트 스킴 | 테마 적용 |
| `_rels/*.xml.rels` | rId → 파일 경로 매핑 | 이미지 참조 연결 |

**ppt-gen에서 문서양식 사용 흐름**:
```
1. 양식.yaml 읽기
   └─ layouts[].images[].rId 참조 확인

2. _rels 파일에서 실제 파일 경로 매핑
   └─ rId7 → ../media/image2.png

3. PPTX 생성 시:
   └─ assets/default/image2.png → ppt/media/image2.png 복사
   └─ _rels 파일 생성 (새 rId 매핑)
   └─ OOXML에 rId 참조 삽입

4. 결과: 원본과 동일한 로고/이미지 포함
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
| `contents/registry.yaml` | 콘텐츠 템플릿 마스터 인덱스 (v4.1) | 전체 | sync_registry.py |
| `contents/registry-{category}.yaml` | 카테고리별 템플릿 레지스트리 (v4.1) | 전체 | sync_registry.py |
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

## 7. 콘텐츠-오브젝트 분리 스키마 (v4.0)

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

## 7. OOXML 하이브리드 스키마 (v2.1 NEW)

### 7.1 핵심 아이디어

PPTX에서 추출한 shape를 YAML로 저장할 때, **추상화된 속성**과 함께 **원본 OOXML**을 함께 저장하여 PPT 생성 시 그대로 재사용합니다.

```
┌─────────────────────────────────────┐
│ PPTX 추출                           │
│ ━━━━━━━━━━━━━                        │
│ 복잡한 도형 → OOXML fragment 보존   │
│ 단순한 도형 → 자연어 설명           │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ YAML 템플릿                          │
│ ━━━━━━━━━━━━━                        │
│ shape_source: ooxml | description  │
│ geometry, style (테마 적용용)       │
│ ooxml.fragment (원본 보존)          │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│ PPT 생성                             │
│ ━━━━━━━━━━                           │
│ OOXML → 직접 삽입 (좌표/색상 치환)  │
│ Description → LLM이 HTML/OOXML 생성 │
└─────────────────────────────────────┘
```

### 7.2 Shape Source 타입 (5가지)

| shape_source | 설명 | PPT 생성 시 처리 |
|--------------|------|-----------------|
| `ooxml` | 원본 OOXML 보존 | fragment 그대로 사용 (좌표/색상만 치환) |
| `svg` | SVG 벡터 경로 | SVG → OOXML 변환 (`<a:custGeom>`) |
| `reference` | 다른 shape/Object 참조 | 참조 대상의 OOXML 복사 + 오버라이드 |
| `html` | HTML/CSS 스니펫 | HTML → 이미지 → PPT 삽입 |
| `description` | 자연어 설명 | LLM이 설명에 맞게 OOXML 생성 |

### 7.3 복잡도 판단 기준

**자동 분류 로직**:

| 복잡 → `ooxml` | 단순 → `description` |
|----------------|---------------------|
| 그라데이션 채우기 (`<a:gradFill>`) | 단색 채우기 (`<a:solidFill>`) |
| 커스텀 도형 (`<a:custGeom>`) | 기본 도형 (`<a:prstGeom>`) |
| 3D 효과, 베벨, 반사 | 단순 그림자 또는 없음 |
| 복잡한 텍스트 (여러 서식) | 단일 스타일 텍스트 |
| 그룹화된 도형 (`<p:grpSp>`) | 단일 도형 |
| 패턴/텍스처 채우기 | 단색/투명 |
| 방사형 세그먼트 (3개+) | 사각형, 원, 기본 화살표 |

### 7.4 Extraction Mode

슬라이드 타입에 따라 추출 범위를 결정합니다:

| 슬라이드 타입 | extraction_mode | 추출 범위 | 이유 |
|--------------|-----------------|----------|------|
| Cover (표지) | `full` | 전체 | 제목 자체가 콘텐츠 |
| TOC (목차) | `full` | 전체 | 목차 구조 전체가 콘텐츠 |
| Section (섹션) | `full` | 전체 | 섹션 제목이 주요 콘텐츠 |
| Closing (마무리) | `full` | 전체 | 전체 레이아웃이 콘텐츠 |
| Agenda (안건) | `full` | 전체 | 안건 목록 전체가 콘텐츠 |
| **Content (일반)** | `content_only` | 콘텐츠 Zone만 | 제목은 마스터에서 관리 |

### 7.5 OOXML Shape 구조

```yaml
shapes:
  - id: "shape-1"
    name: "복잡한 배경 도형"
    shape_source: ooxml    # ← 복잡도 판단 결과

    # 기존 추상화 속성 (테마 적용/커스터마이징용)
    type: custom_shape
    geometry:
      x: 0%
      y: 28.4%
      cx: 100%
      cy: 34.8%
    style:
      fill:
        type: gradient
        color: primary      # 디자인 토큰
      stroke:
        type: none

    # NEW: 원본 OOXML 보존
    ooxml:
      fragment: |
        <p:sp>
          <p:nvSpPr>...</p:nvSpPr>
          <p:spPr>
            <a:xfrm>
              <a:off x="0" y="3074400"/>
              <a:ext cx="12192000" cy="3762000"/>
            </a:xfrm>
            <a:custGeom>...</a:custGeom>
            <a:gradFill>...</a:gradFill>
          </p:spPr>
        </p:sp>

      # 원본 EMU 좌표 (스케일링 계산용)
      emu:
        x: 0
        y: 3074400
        cx: 12192000
        cy: 3762000

      # 원본 색상 참조 (테마 매핑용)
      colors:
        fill: ["#1A5C3E", "#2D8B5A"]
        stroke: null
        text: "#FFFFFF"
```

### 7.6 Description Shape 구조

```yaml
shapes:
  - id: "shape-2"
    name: "단순 배경"
    shape_source: description

    type: rectangle
    geometry:
      x: 0%
      y: 0%
      cx: 100%
      cy: 100%
    style:
      fill:
        type: solid
        color: surface
        opacity: 0.25

    # NEW: 자연어 설명 (LLM이 OOXML 생성 시 참조)
    description:
      text: "사각형 배경, surface 색상, 25% 투명도"
      hints:
        shape_type: rectangle
        fill_token: surface
        opacity: 0.25
```

### 7.7 장점 요약

| 항목 | 기존 (v2.0) | 개선 (v2.1) |
|------|------------|-------------|
| 복잡 도형 보존 | 재구성 필요 | OOXML로 100% 보존 |
| 단순 도형 | 속성 나열 | Description으로 간결화 |
| 생성 속도 | 모두 재생성 | 복잡한 것만 치환 |
| 정확도 | 근사치 | 원본 동일 (복잡 도형) |
| 재사용성 | 템플릿 단위 | Object 단위 컴포넌트 |
| 일관성 | 제목 포함 | 콘텐츠만 분리 (content_only) |

---

## 8. 디자인 토큰 시스템

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

## 9. Template Priority Rule

PPT 생성 시 **필수** 준수 프로세스:

```
1. 슬라이드 목록 작성
   └─ 콘텐츠 분석 → 슬라이드 유형/키워드 정리

2. 분리형 registry 검색 (v4.1)
   └─ registry.yaml(마스터) → registry-{category}.yaml 순회
   └─ 카테고리 힌트 있으면 해당 registry만 검색 (토큰 효율)

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

**금지사항**: 분리형 registry 검색 없이 직접 디자인 (매칭 불가 시에만 허용)

---

## 10. 스크립트 목록 및 배분

### 전체 스크립트 (14개)

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
| **sync_registry.py** | 220 | ppt-gen | 분리형 registry 동기화 (v4.1) |
| rasterize-icon.js | 172 | ppt-image | SVG 래스터화 |
| icon-decision.js | 280 | ppt-gen | 아이콘 필요성 자동 판단 |
| icon-resolver.js | 200 | ppt-gen | 아이콘 생성/삽입 |
| migrate-templates.py | 157 | ppt-create | 템플릿 마이그레이션 |

---

## 11. 기술 스택 및 의존성

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

## 12. 구현 현황 및 로드맵

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

## 13. 사용 예시

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
3. 사전 질문 (AskUserQuestion) ← MANDATORY
   - 청중: 경영진/실무자/혼합/일반
   - 시간: 5-10분/10-20분/20-30분/30분+
   - 강조점: 전체 균형/특정 영역 강조
4. 테마 선택 (deepgreen)
5. HTML 슬라이드 생성
6. html2pptx.js 실행
7. 썸네일 검증 및 결과 전달
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

## 14. Output 폴더 및 파이프라인 추적 시스템 (v5.2)

### 14.1 개요

PPT 생성 시 **누적 방식 JSON 파일**에 중간 과정을 저장합니다. 각 단계 완료 시 **이전 단계 데이터를 모두 포함**한 새 파일을 생성합니다.

**핵심 원칙**:
- **누적 방식**: 각 stage-N.json 파일이 1~N단계 데이터를 모두 포함
- 세션 재개 가능 (중단된 작업 이어서 진행)
- 단계별 디버깅 용이 (직전 파일과 비교 가능)
- 특정 단계만 재실행 가능

### 14.2 Output 폴더 구조 (누적 방식)

```
output/
    {session-id}/                    # 세션 폴더 (예: 2026-01-08_143025_a7b2c3d4)
        stage-1.json                 # 1단계 데이터
        stage-2.json                 # 1단계 + 2단계 데이터
        stage-3.json                 # 1단계 + 2단계 + 3단계 데이터
        stage-4.json                 # 1단계 ~ 4단계 데이터
        stage-5.json                 # 최종 (모든 단계 포함)
        slides/                      # HTML 슬라이드 (4단계 산출물)
            slide-001.html
            slide-002.html
            ...
        assets/                      # 이미지, 아이콘 등
            icons/
            images/
        output.pptx                  # 최종 PPTX (5단계 산출물)
        thumbnails/                  # 검증용 썸네일
            grid.jpg
```

**세션 ID 형식**: `{날짜}_{시간}_{해시}` (예: `2026-01-08_143025_a7b2c3d4`)

**누적 방식 장점**:
- **디버깅 용이**: 각 stage-N.json만 보면 해당 시점의 전체 상태 파악
- **비교 용이**: 문제 발생 시 직전 파일(stage-N-1.json)과 비교
- **단계 재실행**: stage-N-1.json에서 데이터 로드 후 재실행
- **단일 파일 참조**: 최신 파일 하나만 읽으면 전체 상태 확인

### 14.3 PPT 생성 파이프라인 (5단계)

idea.md 기반 5단계 파이프라인:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PPT 생성 파이프라인 (5단계)                            │
├─────────────────────────────────────────────────────────────────────────┤

[사용자 요청]
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1단계: 발표 자료 생성 설정 (Setup)                                        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                       │
│ • **사전 질문 (MANDATORY)**: AskUserQuestion 도구 사용                    │
│   - 청중: 경영진/실무자/혼합/일반                                          │
│   - 시간: 5-10분/10-20분/20-30분/30분+ → 슬라이드 수 자동 결정              │
│   - 강조점: 전체 균형/특정 영역 강조                                        │
│                                                                         │
│ • 입력 (문서에서 추출 또는 사용자 지정):                                   │
│   - 문서 종류 (제안서, 보고서, 사업계획서 등)                              │
│   - 발표 목적 (제안, 보고, 교육 등)                                       │
│   - 테마 / 문서양식 (회사별 디자인)                                        │
│                                                                         │
│ 📄 저장: stage-1.json (누적)                                              │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2단계: 자료 검색 후 발표 자료 생성 (Outline)                               │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                │
│ • 입력: 1단계에서 입력 받은 문서 종류, 청중, 목적, 시간                     │
│ • 출력: 슬라이드별 발표 내용 JSON                                         │
│   - 슬라이드 1 ~ 슬라이드 N                                               │
│   - 각 슬라이드별: 제목, 핵심 포인트, 발표자 노트                          │
│                                                                         │
│ 📄 저장: stage-2.json (1~2단계 누적)                                            │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3단계: 슬라이드별 콘텐츠 종류 선정 (Template Matching)                     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                       │
│ • LLM이 DB로 관리되는 콘텐츠, 오브젝트에서 선정                            │
│ • 입력: 2단계 출력 JSON + 1단계 테마/문서양식                              │
│ • 출력: 슬라이드별 콘텐츠, 오브젝트 선정 JSON                              │
│   - 적당한 오브젝트가 없으면 → 이미지 생성 프롬프트 생성                   │
│                                                                         │
│ ┌─────────┬──────────────┬─────────────────┬──────────────┐             │
│ │ 슬라이드 │ 콘텐츠 유형   │ 매칭 템플릿      │ 오브젝트     │             │
│ ├─────────┼──────────────┼─────────────────┼──────────────┤             │
│ │ 1       │ cover        │ cover-centered1 │ -            │             │
│ │ 2       │ toc          │ toc-3col1       │ -            │             │
│ │ 3       │ comparison   │ comparison-2col1│ -            │             │
│ │ 4       │ process      │ process-flow1   │ cycle-4arrow │             │
│ └─────────┴──────────────┴─────────────────┴──────────────┘             │
│                                                                         │
│ 📄 저장: stage-3.json (1~3단계 누적)                                           │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4단계: 콘텐츠 생성 (Content Generation)                                   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                   │
│ • 입력: 3단계 출력 JSON + 콘텐츠 템플릿 llm_guide                          │
│                                                                         │
│ A. 플레이스홀더 텍스트 생성                                               │
│    - replacement.json 생성 (제목, Action Title, 불릿 등)                  │
│                                                                         │
│ B. 콘텐츠 디자인 생성 (content_visual 레이아웃인 경우)                     │
│    - 콘텐츠 템플릿의 data_slots 스키마에 맞는 데이터 생성                  │
│    - ooxml-generator.py로 OOXML 변환                                     │
│    - content_design 필드에 저장                                          │
│                                                                         │
│ C. 이미지 생성 프롬프트 (선택적, 미구현)                                   │
│    - 필요시 image_prompts[] 생성                                         │
│                                                                         │
│ ┌─────────┬──────────────┬────────────────────────────────────┐         │
│ │ 슬라이드 │ 레이아웃      │ 생성 내용                           │         │
│ ├─────────┼──────────────┼────────────────────────────────────┤         │
│ │ 0       │ cover        │ placeholder_bindings만              │         │
│ │ 3       │ content_visual│ + content_design (grid/timeline)   │         │
│ │ 4       │ content_text │ placeholder_bindings만              │         │
│ └─────────┴──────────────┴────────────────────────────────────┘         │
│                                                                         │
│ 📄 저장: stage-4.json (1~4단계 누적)                                      │
│ 📁 출력: slides/slide-N-data.json, slides/slide-N-content.xml            │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5단계: 슬라이드별 콘텐츠를 HTML/PPTX로 생성                                │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                │
│ • 입력: 3단계 출력 JSON + 4단계 이미지 (없으면 텍스트 박스)                 │
│ • 처리:                                                                 │
│   - HTML 슬라이드 생성 (템플릿 geometry + 콘텐츠)                         │
│   - 디자인 토큰 → 테마 색상 치환                                          │
│   - HTML → PPTX 변환 (html2pptx.js)                                      │
│   - 썸네일 생성 (검증용)                                                 │
│ • 출력: HTML/PPTX                                                       │
│                                                                         │
│ 📁 출력: slides/*.html, output.pptx, thumbnails/grid.jpg                 │
│ 📄 저장: stage-5.json (최종, 모든 단계 누적)                                         │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
[최종 산출물]
    └─ {presentation-name}.pptx
```

### 14.4 슬라이드별 플랫 구조 JSON 스키마 (v5.5)

각 슬라이드에 데이터가 **플랫하게 누적**됩니다 (단계별 분리 없음).

#### 스키마 구조

```json
{
  "session": { "id", "title", "created_at", "status" },
  "current_stage": 1-5,
  "setup": { "presentation": {...}, "theme": {...} },
  "slides": [
    {
      "index": 0,
      "title": "표지",              // 2단계: 아웃라인
      "purpose": "cover",
      "key_points": [...],
      "source_content": {           // 2단계: 원본 콘텐츠 (v5.5)
        "raw_text": "...",
        "source_file": "...",
        "source_section": "..."
      },
      "layout_match": {             // 3단계: 레이아웃 매칭 (v5.5)
        "layout_index": 0,
        "layout_name": "...",
        "reason": "...",
        "alternatives_considered": [...]
      },
      "content_template": {         // 3단계: 콘텐츠 템플릿 매칭 (v5.5)
        "id": "deepgreen-grid-3col1",
        "file": "templates/grid/...",
        "match_score": 0.85,
        "match_factors": {...},
        "alternatives": [...]
      },
      "icon_decision": {            // 3단계: 아이콘 결정 (v5.5)
        "needs_icons": true,
        "confidence": 0.85,
        "matched_keywords": [...]
      },
      "content_bindings": {         // 4단계: 콘텐츠 바인딩 (v5.5)
        "title": "...",
        "items": [{ "slot": "card_1", "title": "...", "icon": "..." }]
      },
      "style_applied": {            // 4단계: 스타일 토큰 (v5.5)
        "theme_id": "...",
        "tokens_used": [{ "name": "primary", "hex": "#...", "usage": [...] }]
      },
      "assets_generated": {         // 4단계: 생성된 에셋 (v5.5)
        "icons": [{ "id": "wms", "react_icon": "fa/FaWarehouse", "file": "icons/wms.png" }],
        "images": []
      },
      "image_prompts": [...],       // 4단계: 이미지 생성 프롬프트
      "html_file": "...",           // 4단계: HTML 파일
      "ooxml_bindings": {...},      // 4단계: OOXML 바인딩
      "generation": {               // 5단계: 생성 메타 (v5.5)
        "method": "html2pptx",
        "pptx_slide_index": 1,
        "generated_at": "2026-01-09T...",
        "warnings": []
      }
    }
  ],
  "output": { "pptx_file", "thumbnail_file", "slide_count" }
}
```

#### 생성 방식 (2가지)

| 방식 | 용도 | 바인딩 |
|------|------|--------|
| **HTML** | 새 슬라이드 생성 | `html_file`, `assets`, `text_content` |
| **OOXML** | 문서양식 편집 | `ooxml_bindings` (ID별 텍스트/이미지/색상) |

- **SVG**: 바인딩 불가 → 정적 아이콘/그래픽으로만 사용

#### stage-4.json 예시 (슬라이드별 플랫 데이터)

```json
{
  "session": {
    "id": "2026-01-08_143025_a7b2c3d4",
    "title": "스마트 물류 시스템 제안서",
    "status": "in_progress"
  },
  "current_stage": 4,
  "setup": {
    "presentation": { "title": "...", "audience": "경영진" },
    "theme": { "id": "deepgreen", "colors": { "primary": "#1E5128" } }
  },
  "slides": [
    {
      "index": 0,
      "title": "표지",
      "purpose": "cover",
      "key_points": ["제안사", "날짜"],
      "template_id": "cover-centered1",
      "match_score": 0.95,
      "html_file": "slides/slide-001.html",
      "assets": { "icons": ["logo.svg"], "images": [] },
      "text_content": { "headline": "스마트 물류 시스템" }
    },
    {
      "index": 1,
      "title": "목차",
      "purpose": "toc",
      "template_id": "toc-3col1",
      "ooxml_bindings": {
        "template": "documents/dongkuk/toc.xml",
        "mappings": [
          { "id": "sp_title", "type": "text", "value": "목차" },
          { "id": "sp_item1", "type": "text", "value": "1. 소개" }
        ]
      }
    }
  ]
}
```

#### OOXML 바인딩 타입

| type | 설명 | 예시 |
|------|------|------|
| `text` | 텍스트 교체 | `{ "id": "sp_title", "type": "text", "value": "제목" }` |
| `image` | 이미지 교체 | `{ "id": "sp_logo", "type": "image", "value": "logo.png" }` |
| `color` | 색상 교체 | `{ "id": "sp_accent", "type": "color", "value": "#1E5128" }` |

### 14.5 세션 관리

**세션 상태**:

| 상태 | 설명 |
|------|------|
| `in_progress` | 진행 중 |
| `paused` | 일시 중단 (재개 가능) |
| `completed` | 완료 |
| `failed` | 실패 |

**세션 재개 흐름** (누적 방식):
1. `output/` 폴더에서 기존 세션 목록 확인
2. 사용자가 재개할 세션 선택
3. 가장 최근 stage-N.json 파일 로드 (N이 가장 큰 파일)
4. `current_stage` 확인 후 다음 단계부터 이어서 진행

**Session Manager API** (v5.6):
```javascript
const SessionManager = require('./scripts/session-manager');

// 새 세션 생성
const session = await SessionManager.create('스마트 물류 제안서');

// 1단계: 전역 설정
await session.completeSetup({
  presentation: { title: '...', audience: '경영진' },
  theme: { id: 'deepgreen', colors: { primary: '#1E5128' } }
});

// 2~4단계: 슬라이드별 데이터 누적 (deep merge 지원)
await session.updateSlide(0, { title: '표지', purpose: 'cover' });
await session.updateSlide(0, {
  content_template: { id: 'cover-centered1', match_score: 0.95 }
});
await session.updateSlide(0, {
  content_bindings: { title: '스마트 물류', items: [...] },
  style_applied: { theme_id: 'deepgreen', tokens_used: [...] }
});

// 5단계: 최종 생성
await session.updateSlide(0, { generation: { method: 'html2pptx' } });
await session.completeGeneration({ pptx_file: 'output.pptx' });

// 세션 재개
const session = await SessionManager.resume('2026-01-09_143025_a7b2c3d4');

// v5.5: 슬라이드 재실행 (Stage-4부터 재시작)
const ctx = await session.rerunSlide(3, 4);

// v5.5: 디자인 결정 요약 조회
const summary = session.getSlideDesignSummary(3);
console.log(summary.decisions.template);  // 'deepgreen-grid-3col1'
console.log(summary.assets.icons);        // 4 (생성된 아이콘 수)
```

**클린업 정책**: 수동 관리 (사용자가 직접 삭제)

### 14.6 디자인 평가 루프 (v5.7 NEW)

Stage 4에서 HTML 슬라이드 생성 후, LLM이 디자인 품질을 평가하고 불합격 시 재매칭/재디자인하는 반복 루프.

#### 평가 기준 (100점 만점)

| 카테고리 | 배점 | 평가 항목 |
|---------|-----|----------|
| **레이아웃** | 25점 | 정렬 일관성(10), 여백 균형(8), 시각적 균형(7) |
| **타이포그래피** | 20점 | 가독성(10), 계층 구조(5), 줄간격/자간(5) |
| **색상** | 20점 | 대비(10), 조화(5), 강조 적절성(5) |
| **콘텐츠 적합성** | 25점 | 템플릿 매칭(15), 정보량(10) |
| **시각 요소** | 10점 | 아이콘/이미지(5), 장식 요소(5) |

#### 합격/불합격 기준

| 점수 | 결과 |
|-----|------|
| **70점 이상** | 합격 → Stage 5 진행 |
| **70점 미만** | 불합격 → 재매칭 |

#### 자동 불합격 (Critical Failures)

점수와 관계없이 불합격:
- 텍스트 오버플로우 (슬라이드 영역 이탈)
- 색상 대비 실패 (WCAG AA 미만, 4.5:1 이하)
- element_count 불일치 (차이 2개 이상)
- 필수 콘텐츠 누락 (title, key_points)

#### 반복 루프 흐름

```
Stage 4.0: HTML 생성 (attempt = 1)
    │
    ▼
Stage 4.1: 기술 검증 (기존)
    │
    ▼
Stage 4.2: 디자인 평가 (LLM)
    │
    ├─ 합격 (≥70) ─────────────────► Stage 5
    │
    └─ 불합격 (<70 또는 Critical)
           │
           ▼
       attempt < 3?
           │
           ├─ Yes → 재매칭 (실패 템플릿 제외)
           │            │
           │            └───► Stage 4.0 (attempt++)
           │
           └─ No → 최고 점수 디자인 선택 (best_of_3)
                       │
                       ▼
                   Stage 5
```

#### 슬라이드별 평가 데이터

```json
{
  "slides[i]": {
    "evaluation": {
      "attempt_number": 2,
      "current_score": 78,
      "passed": true,
      "selected_reason": "passed | best_of_3",
      "details": {
        "layout": { "score": 22, "max": 25, "issues": [] },
        "typography": { "score": 18, "max": 20, "issues": [] },
        "color": { "score": 17, "max": 20, "issues": [] },
        "content_fit": { "score": 15, "max": 25, "issues": [] },
        "visual": { "score": 6, "max": 10, "issues": [] }
      },
      "critical_failures": null
    },
    "attempt_history": [
      {
        "attempt": 1,
        "template_id": "deepgreen-feature-cards1",
        "score": 52,
        "passed": false,
        "critical_failures": ["element_count_mismatch"],
        "timestamp": "..."
      }
    ]
  }
}
```

#### selected_reason 값

| 값 | 설명 |
|----|------|
| `passed` | 70점 이상 합격 |
| `best_of_3` | 3회 실패 후 최고 점수 선택 |

#### 재매칭 알고리즘

1. 동일 category, 실패 템플릿 제외
2. element_count 근접 정렬
3. design_intent 다양성 (실패한 것과 다른 레이아웃)
4. 후보 없으면 다른 category 확장 검색

---

## 부록

### A. YAML 스키마 정의

콘텐츠 템플릿 v4.0 스키마: `ppt-create/references/content-schema.md` 참조

### B. 콘텐츠 템플릿 카테고리 (19개)

cover, toc, section, comparison, process, chart, stats, grid, diagram, timeline, content, quote, closing, cycle, matrix, feature, flow, table, infographic

### C. 아이콘 시스템

#### C.1 아이콘 매핑 목록

50+ 키워드 → 아이콘 매핑: `templates/assets/icon-mappings.yaml` 참조

**카테고리별 분류**:
- technology: 보안, 속도, 데이터, AI, 클라우드, 서버 등 (10개)
- business: 성장, 목표, 전략, 성공, 효율 등 (8개)
- logistics: 창고, 배송, 주문, 재고, 대시보드 (5개)
- risk: 위험, 지연, 오류, 변경 (4개)
- 기타: communication, process, finance, quality, document, location, customer

#### C.2 아이콘 자동 판단 로직

**판단 모듈**: `icon-decision.js`

슬라이드의 아이콘 필요성을 자동 판단하여 `needs_icons: true/false` 결정.

**판단 점수 계산**:
```
총점 = (카테고리 적합도 × 0.30) + (항목수 적합도 × 0.25) +
       (키워드 매핑율 × 0.25) + (템플릿 지원 × 0.20)

needs_icons = 총점 ≥ 0.5
```

**카테고리별 적합도**:

| 카테고리 | 적합도 | 설명 |
|---------|-------|------|
| grid, feature, stats | 1.0 (높음) | 아이콘으로 시각적 구분 효과적 |
| process, comparison | 0.7 (중간) | 선택적 적용 |
| timeline, content | 0.5 (낮음) | 다른 시각 요소로 대체 가능 |
| cover, toc, table | 0.0 (불필요) | 텍스트 중심 |

**항목수 적합도**:

| 항목 수 | 적합도 |
|--------|-------|
| 3~6개 | 1.0 (최적) |
| 2개, 7~8개 | 0.7 (적합) |
| 1개 | 0.3 (낮음) |
| 9개+ | 0.4 (아이콘 과다) |

#### C.3 아이콘 생성/삽입

**생성 모듈**: `icon-resolver.js`

1. `icon-decision.js`에서 `needs_icons: true` 판단
2. `matched_keywords`에서 키워드-아이콘 매핑 추출
3. `rasterize-icon.js`로 PNG 생성 (테마 primary 색상)
4. HTML 템플릿에 `<img>` 태그로 삽입

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
| 4.3 | 2026-01-08 | Output 폴더 및 5단계 파이프라인 추적 시스템 추가 |
| 4.4 | 2026-01-08 | 단계별 JSON 파일 분리 구조로 변경 (session.json + stage-N-*.json) |
| 4.5 | 2026-01-08 | idea.md 기반 5단계 파이프라인으로 재정리 |
| 4.6 | 2026-01-08 | 2개 스킬 구조로 변경: ppt-extract (추출) + ppt-gen (생성) |
| 4.7 | 2026-01-08 | 관리 기능을 ppt-manager 앱으로 분리, 스킬 단순화 |
| 4.8 | 2026-01-08 | **OOXML 하이브리드 스키마 (v2.1)** 추가: shape_source (ooxml, svg, reference, html, description), extraction_mode (full, content_only), Object 분리 저장 |
| 4.9 | 2026-01-08 | **문서양식 추출 확장**: slideMaster + theme + _rels 관계파일 추출, ppt-gen에서 로고/이미지 재사용 가능 |
| 5.0 | 2026-01-09 | TODO 섹션 추가, 스킬 분리 작업 시작 |
| 5.1 | 2026-01-09 | **누적 방식 JSON** 구조로 변경: 각 stage-N.json이 이전 단계 데이터 포함, session-manager.js 구현, 테마 YAML 추가 |
| 5.2 | 2026-01-09 | **슬라이드별 플랫 구조**: 단계 구분 없이 슬라이드에 데이터 플랫 누적, `updateSlide()` API, OOXML 바인딩 (text/image/color), SVG 정적 사용만 |
| 5.3 | 2026-01-09 | **문서+콘텐츠 통합 아키텍처**: 기본양식.yaml 플레이스홀더 시맨틱 역할 정의 (semantic_role, constraints, llm_hints), content_zone 개념 도입, 콘텐츠 템플릿 llm_guide/ooxml_export 섹션 추가, ooxml-generator.py 구현, document-content-workflow.md 워크플로우 문서화 |
| 5.4 | 2026-01-09 | **아이콘 자동 판단 시스템**: icon-decision.js (필요성 판단), icon-resolver.js (생성/삽입), icon-mappings.yaml 활성화 (50+ 키워드), 카테고리/항목수/키워드 기반 점수 계산 |
| 5.5 | 2026-01-09 | **Stage 4 콘텐츠 디자인 통합**: template.md 워크플로우에 Step 6.5/7.5 추가, insert-ooxml.py 스크립트 구현, 4단계를 "이미지 생성"에서 "콘텐츠 생성"으로 확장 (placeholder_bindings + content_design), stage-4.json에 content_design 필드 추가 |
| 5.6 | 2026-01-09 | **세션 스키마 확장 (디자인 자체 문서화)**: stage-*.json에 상세 디자인 정보 저장 (`source_content`, `layout_match`, `content_template`, `icon_decision`, `content_bindings`, `style_applied`, `assets_generated`, `generation`), deep merge 지원 (`updateSlide()`), 슬라이드 재실행 (`rerunSlide()`), 디자인 요약 조회 (`getSlideDesignSummary()`), icon-resolver.js v5.5 스키마 적용 |

---

## 15. TODO List (작업 추적)

### 15.1 현재 진행 상황

| 영역 | 상태 | 완료율 |
|------|------|--------|
| ppt-extract 스킬 | ✅ 완료 | 100% |
| ppt-gen 스킬 | 🔄 수정중 | 80% |
| 템플릿 시스템 | 🔄 재구성 | 60% |
| ppt-manager 앱 | ⬜ 미착수 | 0% |

### 15.2 작업 항목

#### Phase 1: ppt-extract 스킬 완성 (현재)

- [x] **1.1 스크립트 경로 정리** ✅ (2026-01-09)
  - [x] ppt-gen에서 중복 스크립트 삭제 (template-analyzer.py, style-extractor.py, slide-crawler.py)
  - [x] ppt-gen에서 추출 관련 워크플로우 삭제 (content-extract.md, document-extract.md, style-extract.md)
  - [x] ppt-gen SKILL.md에서 삭제된 워크플로우 참조 수정

- [x] **1.2 워크플로우 연결 확인** ✅ (2026-01-09)
  - [x] content-extract.md → ppt-gen 공유 스크립트 경로로 수정
  - [x] document-extract.md → ppt-gen 공유 스크립트 경로로 수정

- [x] **1.3 references 정리** ✅ (2026-01-09)
  - [x] ppt-extract의 content-schema.md 삭제 (ppt-gen 버전이 최신)
  - [x] ppt-extract SKILL.md에 Shared Resources 섹션 추가
  - [x] font-mappings.yaml 참조 추가

- [x] **1.4 테스트** ✅ (2026-01-09)
  - [x] unpack.py 테스트 (PPTX → 언팩 폴더)
  - [x] thumbnail.py 테스트 (썸네일 그리드 생성)
  - [x] style-extractor.py 테스트 (이미지 → 색상 추출)
  - [x] 임시 파일 정리 확인

#### Phase 2: ppt-gen 스킬 완성

- [x] **2.1 5단계 파이프라인 워크플로우** ✅ (v5.1)
  - [x] html2pptx.md 검증
  - [x] 누적 방식 JSON 스키마 구현 (`pipeline.schema.json`)
  - [x] session 관리 구현 (`session-manager.js`)
  - [x] 테마 YAML 추가 (`templates/themes/`)

- [x] **2.2 스크립트 정리** ✅
  - [x] 추출 관련 스크립트 제거 (ppt-extract로 이동됨)
  - [x] 생성 관련 스크립트만 유지

- [x] **2.3 테스트** ✅
  - [x] html2pptx 파이프라인 E2E 테스트
  - [x] 템플릿 기반 생성 테스트

#### Phase 3: 템플릿 재구축

- [ ] **3.1 deepgreen 테마 완성**
  - [ ] 모든 카테고리별 템플릿 확인
  - [ ] 썸네일 생성

- [ ] **3.2 registry.yaml 정리**
  - [ ] 삭제된 템플릿 참조 제거
  - [ ] 새 템플릿 등록

- [x] **3.3 동국시스템즈 문서 템플릿** ✅ (2026-01-09)
  - [x] config.yaml 완성
  - [x] 기본양식.yaml 플레이스홀더 스키마 개선
    - semantic_role, constraints, llm_hints 추가
    - content_zone 정의 (Layout 4)
    - selection_guide 추가
  - [x] 콘텐츠 템플릿 스키마 개선 (llm_guide, ooxml_export)
  - [x] OOXML 생성 스크립트 구현 (ooxml-generator.py)
  - [x] 파이프라인 워크플로우 문서화 (document-content-workflow.md)

#### Phase 4: 통합 테스트

- [ ] 추출 → 생성 파이프라인 E2E 테스트
- [ ] 문서 양식 기반 생성 테스트

### 15.3 완료된 항목

- [x] PRD v4.9 작성 (2026-01-08)
- [x] 2개 스킬 구조 결정 (ppt-extract + ppt-gen)
- [x] OOXML 하이브리드 스키마 설계 (v2.1)
- [x] 5단계 파이프라인 설계
- [x] ppt-extract SKILL.md 초안 작성
- [x] ppt-extract workflows 초안 작성
- [x] **Phase 1: ppt-extract 스킬 완성** (2026-01-09)
  - 스크립트 중복 정리 (ppt-gen → ppt-extract 분리)
  - 워크플로우 경로 수정 (공유 스크립트 참조)
  - references 정리 (content-schema.md 공유)
  - 테스트 완료 (unpack, thumbnail, style-extractor)

#### Phase 5: 코드 중복 제거 및 리팩터링 ✅ (2026-01-09)

- [x] **P1 (HIGH): YAML 유틸리티 공유 모듈화**
  - [x] `shared/yaml_utils.py` 생성 (load_yaml, save_yaml, load_registry, save_registry)
  - [x] `shared/config.py` 생성 (경로 상수 중앙화)
  - [x] `shared/__init__.py` 생성 (패키지화)
  - [x] ppt-extract/scripts 업데이트 (slide-crawler.py, template-analyzer.py)
  - [x] ppt-gen/scripts 업데이트 (asset-manager.py, template-manager.py)

- [x] **P2 (MEDIUM): 하드코딩된 경로 수정**
  - [x] asset-manager.py:73 `PROJECT_ROOT = Path("C:/project/docs")` → shared/config.py 사용

- [x] **P3 (MEDIUM): XML 추출 함수 파라미터화**
  - [x] `shared/xml_utils.py` 생성
  - [x] template-analyzer.py의 6개 함수 → 공유 모듈로 통합
    - extract_layout_ooxml()
    - extract_layout_rels()
    - extract_slide_master_ooxml()
    - extract_slide_master_rels()
    - extract_theme_ooxml()
    - (extract_theme_rels() 추가)

- [x] **P4 (LOW): 레지스트리 매니저** ✅ 완료 (v4.1)
  - [x] `ppt-gen/scripts/sync_registry.py` - 분리형 registry 동기화 스크립트
    - 개별 템플릿 YAML → 카테고리별 registry 자동 생성
    - 마스터 registry.yaml 인덱스 업데이트
    - 검색 메타데이터 통합 (match_keywords, description, expected_prompt)
