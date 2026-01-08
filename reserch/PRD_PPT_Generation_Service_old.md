# PRD: Claude Code PPT 자동 생성 서비스

**버전**: 3.0
**작성일**: 2026-01-06
**상태**: Approved

---

## 1. 개요

### 1.1 제품 비전

Claude Code 환경에서 구조화된 문서를 입력받아 **전문 디자이너 수준의 PPT**를 자동 생성하는 Skill 기반 서비스.

### 1.2 핵심 결정사항

| 항목 | 결정 |
|------|------|
| 구현 방식 | **Skills만 사용** (MCP Tools 제외) |
| 기술 스택 | **기존 시스템 활용** (PptxGenJS + html2pptx.js) |
| 템플릿 DB | **YAML 기반** (벡터 유사도 제외, LLM이 선택) |
| Skill | **pptx → ppt-gen 이름 변경** (통합된 단일 Skill) |
| 템플릿 구조 | **2단계 분리** (문서 템플릿 + 콘텐츠 템플릿) |

### 1.3 타겟 사용자

- **Primary**: 기업/비즈니스 사용자 (제안서, 보고서, 사업계획서)
- **Secondary**: 컨설턴트, 스타트업, 프로젝트 매니저

---

## 2. 시스템 아키텍처

### 2.1 Skill 구조

```
.claude/
├── skills/
│   └── ppt-gen/                     # 통합 PPT Skill
│       ├── SKILL.md                 # 메인 진입점 + 워크플로우 라우터
│       ├── html2pptx.md             # HTML→PPTX 워크플로우 가이드
│       ├── ooxml.md                 # OOXML 편집 워크플로우 가이드
│       ├── scripts/
│       │   ├── html2pptx.js         # HTML → PPTX 변환
│       │   ├── inventory.py         # 텍스트 추출
│       │   ├── replace.py           # 텍스트 교체
│       │   ├── rearrange.py         # 슬라이드 재배열
│       │   ├── thumbnail.py         # 썸네일 생성
│       │   └── template-analyzer.py # PPTX → YAML 분석
│       └── templates/
│           ├── documents/           # [타입 1] 문서 템플릿 (그룹/회사별)
│           │   └── dongkuk/         # 그룹 폴더
│           │       ├── config.yaml  # 그룹 공통 테마
│           │       ├── registry.yaml # 양식 목록 및 설명
│           │       ├── assets/      # 계열사별 에셋
│           │       │   ├── dongkuk-steel/
│           │       │   └── default/
│           │       ├── 제안서1.yaml
│           │       └── 보고서1.yaml
│           ├── contents/            # [타입 2] 콘텐츠 템플릿 (슬라이드 패턴)
│           │   ├── registry.yaml
│           │   ├── templates/
│           │   │   ├── cover1.yaml
│           │   │   ├── cover2.yaml
│           │   │   ├── toc1.yaml
│           │   │   ├── timeline1.yaml
│           │   │   └── comparison1.yaml
│           │   └── thumbnails/
│           └── assets/              # [타입 3] 공용 에셋 (이미지/아이콘)
│               ├── registry.yaml
│               ├── icons/
│               ├── images/
│               └── thumbnails/
├── includes/
│   ├── PPT기본양식.pptx             # 마스터 템플릿
│   └── PPT기본양식_분석보고서.md     # 템플릿 분석 문서
└── agents/
    └── ppt-designer.md              # 디자인 Sub-agent
```

### 2.2 처리 파이프라인

```
입력 (Markdown/JSON/텍스트)
         ↓
┌─────────────────────────────────────┐
│         ppt-gen Skill               │
├─────────────────────────────────────┤
│  [1. 워크플로우 라우터]              │
│      ├─ 새 PPT → html2pptx         │
│      ├─ 템플릿 사용 → template      │
│      └─ 수정 → ooxml               │
│                                     │
│  [2. 콘텐츠 분석] - LLM             │
│      └─ 구조 파악, 슬라이드 설계     │
│                                     │
│  [3. 레이아웃 선택] - LLM           │
│      └─ YAML 템플릿 참조            │
│                                     │
│  [4. 생성] - ppt-gen 스크립트       │
│      └─ html2pptx.js / replace.py  │
│                                     │
│  [5. 검증] - thumbnail.py          │
└─────────────────────────────────────┘
         ↓
출력 (.pptx 파일)
```

---

## 3. 워크플로우

### 3.1 새 PPT 생성 (html2pptx)

**트리거**: 템플릿 언급 없이 PPT 생성 요청

```
1. 콘텐츠 분석 → 슬라이드 구조 설계
2. 색상/스타일 결정
3. HTML 슬라이드 생성 (720pt × 405pt)
4. html2pptx.js로 변환
5. 썸네일 검증
```

### 3.2 템플릿 기반 생성 (template)

**트리거**: 특정 템플릿/브랜드 언급

```
1. templates/*.yaml 로드
2. LLM이 콘텐츠 ↔ 레이아웃 매핑
3. rearrange.py → 슬라이드 구성
4. inventory.py → 텍스트 추출
5. replace.py → 텍스트 교체
6. 썸네일 검증
```

### 3.3 기존 PPT 수정 (ooxml)

**트리거**: 기존 PPT 파일 수정 요청

```
1. PPTX 언팩 → XML 추출
2. XML 편집 (슬라이드, 테마 등)
3. 검증 → 리팩
```

### 3.4 템플릿 분석/등록 (template-analyze) [신규]

**트리거**: "이 PPT를 템플릿으로 등록해줘"

```
1. thumbnail.py → 썸네일 생성
2. template-analyzer.py → 테마/레이아웃 추출
3. 그룹 폴더 생성 또는 선택
4. config.yaml + {양식}.yaml 저장
5. documents/{그룹}/registry.yaml 업데이트
```

### 3.5 스타일 추출 (style-extract) [신규]

**트리거**: "이 이미지 스타일로 만들어줘"

```
1. LLM Vision으로 이미지 분석
2. 색상/레이아웃 패턴 추출
3. 스타일 가이드 생성
4. html2pptx로 적용
```

### 3.6 디자인 검색 (design-search) [신규]

**트리거**: "PPT 디자인 찾아줘"

```
1. WebSearch로 디자인 레퍼런스 검색
2. 이미지 분석 → 스타일 추출
3. 추천 디자인 제시
```

### 3.7 템플릿 관리 (template-manage) [신규]

**트리거**: "템플릿 목록/삭제/정리"

```
1. registry.yaml 조회
2. 썸네일과 함께 목록 표시
3. 삭제/아카이브 실행
```

---

## 4. 템플릿 시스템 (3타입 구조)

### 4.1 타입 1: 문서 템플릿 (그룹/회사별)

그룹 또는 회사별 **폴더 단위**로 관리합니다. 공통 테마, 계열사별 에셋, 문서 양식 포함.

**폴더 구조:**
```
documents/dongkuk/              # 그룹 폴더
├── config.yaml                 # 그룹 공통 테마
├── registry.yaml               # 양식 목록 및 설명
├── assets/                     # 계열사별 에셋
│   ├── dongkuk-steel/logo.png
│   ├── dongkuk-cm/logo.png
│   └── default/logo.png
├── 제안서1.yaml                # 제안서 스타일 1 (전체 구성)
├── 제안서2.yaml                # 제안서 스타일 2 (전체 구성)
├── 보고서1.yaml                # 보고서 스타일 1 (전체 구성)
└── 프로젝트계획서1.yaml         # 프로젝트계획서 스타일 1 (전체 구성)
```

**config.yaml (그룹 공통 테마):**
```yaml
# documents/dongkuk/config.yaml
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
    name: 동국제강
  - id: dongkuk-cm
    name: 동국씨엠
  - id: default
    name: 동국그룹 (기본)
```

**registry.yaml (양식 목록 및 설명):**
```yaml
# documents/dongkuk/registry.yaml
templates:
  - id: 제안서1
    name: 제안서 (기본)
    file: 제안서1.yaml
    type: proposal
    description: "표지 + 목차 + 본문(불릿) + 마무리 구성"

  - id: 제안서2
    name: 제안서 (이미지 중심)
    file: 제안서2.yaml
    type: proposal
    description: "이미지 배경 표지 + 2열 본문 + 마무리 구성"

  - id: 보고서1
    name: 보고서 (기본)
    file: 보고서1.yaml
    type: report
    description: "심플한 표지 + 데이터 중심 본문 구성"
```

**양식 파일 예시 (제안서1.yaml):**
```yaml
# documents/dongkuk/제안서1.yaml
document:
  id: 제안서1
  name: 제안서 (기본)
  type: proposal
  source: .claude/includes/PPT기본양식.pptx

slides:
  - category: cover
    slide_index: 0
    description: "표지 - 로고 중앙, 제목 하단"

  - category: toc
    slide_index: 1
    description: "목차"

  - category: body
    slide_index: 2
    description: "본문 - 제목 + 불릿 리스트"

  - category: closing
    slide_index: 5
    description: "마무리"
```

### 4.2 타입 2: 콘텐츠 템플릿 (슬라이드 패턴)

모든 **슬라이드 콘텐츠 패턴**을 관리합니다. 표지, 목차, 본문 슬라이드 모두 포함.

**폴더 구조:**
```
contents/
├── registry.yaml               # 콘텐츠 레지스트리
├── templates/                  # 템플릿 파일들
│   ├── cover1.yaml
│   ├── cover2.yaml
│   ├── toc1.yaml
│   ├── timeline1.yaml
│   ├── timeline2.yaml
│   ├── comparison1.yaml
│   └── ...
└── thumbnails/                 # 미리보기 이미지
    ├── cover1.jpg
    ├── cover2.jpg
    └── comparison1.jpg
```

**템플릿 파일 예시:**
```yaml
# contents/templates/comparison1.yaml
content_template:
  id: comparison1
  name: 비교 (A vs B) - 기본
  description: "두 가지 항목을 나란히 비교하는 2열 대칭 레이아웃"

structure:
  type: two-column-symmetric
  left:
    header: "Before / Option A"
  right:
    header: "After / Option B"

use_for:
  - "A vs B 비교"
  - "Before/After 변화"
  - "현재 vs 목표"

keywords: ["비교", "vs", "대비", "차이"]
```

**콘텐츠 템플릿 종류:**

| 카테고리 | ID 예시 | 데이터 특성 | 구조 |
|---------|---------|-----------|------|
| cover | `cover1`, `cover2` | 프레젠테이션 표지 | 제목 + 부제목 + 로고 |
| toc | `toc1`, `toc2` | 목차/아젠다 | 번호 + 항목 리스트 |
| section | `section1` | 챕터 전환 | 큰 제목 + 배경 |
| comparison | `comparison1`, `comparison2` | A vs B | 2열 대칭 |
| timeline | `timeline1`, `timeline2` | 시간순 데이터 | 가로/세로 흐름 |
| stat-cards | `stat-cards1` | 숫자 강조 | 큰 숫자 + 설명 |
| process-flow | `process-flow1` | 단계별 절차 | 화살표 연결 |
| feature-grid | `feature-grid1` | 기능 목록 | 아이콘 + 텍스트 |
| pros-cons | `pros-cons1` | 양면 평가 | 2열 (✓/✗) |

### 4.3 레지스트리

**콘텐츠 레지스트리** (`contents/registry.yaml`):
```yaml
# contents/registry.yaml
templates:
  - id: cover1
    name: 표지 (기본)
    file: templates/cover1.yaml
    thumbnail: thumbnails/cover1.jpg
    category: cover
    description: "중앙 정렬 제목 + 하단 로고"
    use_for: ["표지", "타이틀 슬라이드"]

  - id: cover2
    name: 표지 (이미지 배경)
    file: templates/cover2.yaml
    thumbnail: thumbnails/cover2.jpg
    category: cover
    description: "전체 배경 이미지 + 오버레이 제목"
    use_for: ["표지", "비주얼 강조"]

  - id: comparison1
    name: 비교 (A vs B) - 기본
    file: templates/comparison1.yaml
    thumbnail: thumbnails/comparison1.jpg
    category: comparison
    description: "두 가지 항목을 나란히 비교하는 2열 대칭 레이아웃"
    use_for: ["A vs B 비교", "Before/After"]
```

**문서 템플릿 레지스트리** (`documents/{그룹}/registry.yaml`):
```yaml
# documents/dongkuk/registry.yaml
templates:
  - id: 제안서1
    name: 제안서 (기본)
    file: 제안서1.yaml
    type: proposal
    description: "표지 + 목차 + 본문(불릿) + 마무리 구성"
```

- `documents/{그룹}/config.yaml` → 그룹 테마 설정
- `documents/{그룹}/registry.yaml` → 양식 목록 및 설명
- `documents/{그룹}/*.yaml` → 개별 양식 파일
- `documents/{그룹}/assets/{계열사}/` → 계열사별 에셋

### 4.4 타입 3: 에셋 템플릿 (이미지/아이콘)

생성하거나 다운로드한 **이미지, SVG, 아이콘**을 관리합니다. 재사용 가능한 에셋 라이브러리.

```yaml
# templates/assets/registry.yaml
icons:
  - id: chart-line
    name: 라인 차트 아이콘
    file: icons/chart-line.svg
    source: generated        # generated | downloaded | brand
    tags: ["chart", "data", "analytics"]
    created: 2026-01-06

  - id: arrow-right
    name: 오른쪽 화살표
    file: icons/arrow-right.svg
    source: generated
    tags: ["arrow", "navigation", "flow"]

images:
  - id: hero-tech-bg
    name: 테크 배경 이미지
    file: images/hero-tech-bg.png
    source: downloaded
    tags: ["background", "tech", "hero"]
    original_url: "https://example.com/image.png"

  - id: dongkuk-logo
    name: 동국제강 로고
    file: images/dongkuk-logo.png
    source: brand
    tags: ["logo", "dongkuk", "brand"]
```

**에셋 소스 타입:**

| source | 설명 | 예시 |
|--------|------|------|
| `generated` | Claude가 SVG/이미지로 직접 생성 | 아이콘, 다이어그램, 차트 |
| `downloaded` | 웹에서 다운로드 | 배경 이미지, 스톡 사진 |
| `brand` | 브랜드 공식 에셋 (Brandfetch 등) | 회사 로고, 브랜드 아이콘 |

### 4.5 LLM 선택 프로세스

벡터 유사도 검색 대신 **LLM이 직접 선택**:

1. `registry.yaml`에서 `description` + `use_for` 목록 읽기
2. 데이터 특성과 매칭:
   - "A vs B" 데이터 → `comparison` 템플릿
   - "2024~2026 로드맵" → `timeline` 템플릿
   - "매출 150억" → `stat-cards` 템플릿
3. 선택된 템플릿의 `structure` 정보로 HTML 생성

---

## 5. 구현 완료 현황

### Phase 1: 핵심 스크립트 (완료)

| 파일 | 상태 | 설명 |
|------|------|------|
| `ppt-gen/SKILL.md` | ✅ 완료 | 워크플로우 라우터 |
| `ppt-gen/html2pptx.md` | ✅ 완료 | HTML→PPTX 워크플로우 가이드 |
| `ppt-gen/ooxml.md` | ✅ 완료 | OOXML 편집 워크플로우 가이드 |
| `ppt-gen/scripts/*` | ✅ 완료 | 5개 스크립트 (html2pptx.js 등) |

### Phase 2: 3타입 템플릿 시스템 (진행중)

| 파일 | 상태 | 설명 |
|------|------|------|
| `ppt-gen/SKILL.md` | 🔄 수정 | 워크플로우 추가 (analyze, extract, search, manage, asset) |
| `ppt-gen/templates/documents/{그룹}/` | ⬜ 신규 | 그룹별 문서 템플릿 폴더 |
| `ppt-gen/templates/documents/{그룹}/config.yaml` | ⬜ 신규 | 그룹 테마 설정 |
| `ppt-gen/templates/documents/{그룹}/registry.yaml` | ⬜ 신규 | 그룹별 양식 목록 |
| `ppt-gen/templates/contents/registry.yaml` | ⬜ 신규 | 콘텐츠 템플릿 레지스트리 |
| `ppt-gen/templates/assets/registry.yaml` | ⬜ 신규 | 에셋 레지스트리 |
| `ppt-gen/scripts/template-analyzer.py` | ⬜ 신규 | PPTX → YAML 분석 스크립트 |

### Phase 3: 레퍼런스 (예정)

| 파일 | 설명 |
|------|------|
| `references/custom-elements.md` | 요소 스키마 |
| `references/design-system.md` | 디자인 규칙 |
| `references/color-palettes.md` | 컬러 팔레트 |

---

## 6. 기술 스택

### 6.1 스크립트 (ppt-gen/scripts/)

| 스크립트 | 역할 |
|---------|------|
| `html2pptx.js` | HTML → PPTX 변환 (977줄) |
| `inventory.py` | PPT 텍스트 추출 |
| `replace.py` | 텍스트 교체 |
| `rearrange.py` | 슬라이드 재배열 |
| `thumbnail.py` | 썸네일 생성 |

### 6.2 의존성

**Node.js**:
- pptxgenjs (PPTX 생성)
- playwright (HTML 렌더링)
- sharp (이미지 처리)

**Python**:
- python-pptx
- markitdown
- defusedxml

---

## 7. 사용 예시

### 새 PPT 생성

```
사용자: "스마트 물류 시스템 제안서 PPT 만들어줘"

Claude:
1. 콘텐츠 분석 → 섹션 구조 파악
2. 색상 결정 (물류 = 파랑 계열)
3. HTML 슬라이드 생성
4. html2pptx 변환
5. 결과 전달
```

### 템플릿 기반 생성

```
사용자: "동국제강 양식으로 분기 실적 보고서 만들어줘"

Claude:
1. dongkuk/config.yaml 로드 → 테마 적용
2. dongkuk/registry.yaml → 보고서1.yaml 선택
3. dongkuk/assets/dongkuk-steel/logo.png → 로고 적용
4. rearrange → inventory → replace
5. 결과 전달
```

---

## 8. 참고 자료

- [PPT 자동생성 연구보고서](./PPT_자동생성_연구보고서.md)
- [Professional PPT Architecture Research](./professional-ppt-architecture-research_제미나이작성.md)
- [구현 계획](../.claude/plans/cuddly-beaming-aurora.md)
