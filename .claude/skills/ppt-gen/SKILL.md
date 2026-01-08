---
name: ppt-gen
description: "AI-powered PPT generation service. Use when: (1) Creating presentations from Markdown/JSON content, (2) Using templates to generate branded presentations, (3) Modifying or editing existing presentations, (4) Analyzing PPT structure. For template/style extraction, use ppt-extract skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPT Generation Service

AI 기반 PPT 자동 생성 서비스. 콘텐츠를 입력받아 전문가 수준의 프레젠테이션을 생성합니다.

## Workflow Selection

사용자 요청에 따라 적절한 워크플로우를 선택합니다.

| 요청 유형 | 워크플로우 | 가이드 |
|----------|-----------|--------|
| "PPT 만들어줘" (템플릿 없음) | html2pptx | [workflows/html2pptx.md](workflows/html2pptx.md) |
| "동국제강 양식으로" (템플릿 사용) | template | [workflows/template.md](workflows/template.md) |
| "이 PPT 수정해줘" | ooxml | [workflows/ooxml.md](workflows/ooxml.md) |
| "PPT 분석해줘" | analysis | [workflows/analysis.md](workflows/analysis.md) |

> **추출 기능**: 콘텐츠/문서/스타일 추출은 **ppt-extract** 스킬을 사용하세요.

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Template Priority Rule (CRITICAL)

**PPT 생성 시 반드시 콘텐츠 템플릿 우선 검색** - 이 단계를 건너뛰면 안 됩니다.

### 필수 프로세스

1. **슬라이드 목록 작성**: 콘텐츠 분석 → 슬라이드 유형/키워드 정리
2. **registry.yaml 검색**: 각 슬라이드별 매칭 템플릿 찾기
3. **매칭 결과 테이블 작성**: 어떤 템플릿을 사용할지 명시 (필수 출력물)
4. **템플릿 YAML 로드**: 매칭된 템플릿의 `shapes[]` 구조 참조
5. **HTML 생성**: 템플릿 geometry/style을 HTML로 변환

### 유연한 템플릿 활용

템플릿은 **2가지 레벨**에서 활용합니다:

**슬라이드 레벨**: 전체 레이아웃 참조
- 슬라이드 전체 구조를 템플릿에서 가져오기
- 예: `deepgreen-cover1` → 표지 슬라이드 전체

**요소 레벨**: 개별 shapes 참조 (더 유연함)
- 템플릿의 특정 shape만 가져와서 조합
- 예: `deepgreen-stats1`의 도트그리드 통계 박스 1개만 가져오기
- 예: `deepgreen-grid4col1`의 아이콘+텍스트 카드 패턴만 가져오기
- 예: `timeline1`의 단계 표시 요소만 가져와서 커스텀 레이아웃에 배치

**조합 전략**:
- 여러 템플릿에서 필요한 shapes 선택
- geometry(위치/크기)는 새 슬라이드에 맞게 조정
- style(색상/폰트)은 일관성 유지

### 직접 디자인 허용 조건

- registry.yaml을 검색했으나 **매칭되는 템플릿이 없는 경우만**
- 매칭 결과 테이블에 ❌ 표시된 슬라이드만 직접 디자인

### 금지 사항

- registry.yaml 검색 없이 직접 디자인 시작
- 매칭 가능한 템플릿이 있는데 직접 디자인

### Shape Source 기반 하이브리드 추출 (v3.1)

콘텐츠 템플릿 추출 시, 도형 복잡도에 따라 **shape_source** 타입이 결정됩니다:

**5가지 Shape Source 타입**:

| shape_source | 설명 | PPT 생성 시 처리 |
|--------------|------|-----------------|
| `ooxml` | 원본 OOXML 보존 | fragment 그대로 사용 (좌표/색상만 치환) |
| `svg` | SVG 벡터 경로 | SVG → OOXML 변환 (custGeom) |
| `reference` | 다른 shape/Object 참조 | 참조 대상의 OOXML 복사 + 오버라이드 |
| `html` | HTML/CSS 스니펫 | HTML → 이미지 → PPT 삽입 |
| `description` | 자연어 설명 | LLM이 설명에 맞게 OOXML 생성 |

**복잡도에 따른 자동 분류**:

| 복잡 → `ooxml` | 단순 → `description` |
|----------------|---------------------|
| 그라데이션 채우기 | 단색 채우기 |
| 커스텀 도형 (`<a:custGeom>`) | 기본 도형 (`<a:prstGeom>`) |
| 3D 효과, 베벨, 반사 | 단순 그림자 또는 없음 |
| 복잡한 텍스트 (여러 서식) | 단일 스타일 텍스트 |
| 그룹화된 도형 | 단일 도형 |
| 방사형 세그먼트 (3개+) | 사각형, 원, 기본 화살표 |

**Extraction Mode (슬라이드 타입별)**:

| 슬라이드 타입 | extraction_mode | 추출 범위 |
|--------------|-----------------|----------|
| Cover, TOC, Section, Closing | `full` | 전체 슬라이드 |
| Content (일반) | `content_only` | 콘텐츠 Zone만 (제목/푸터 제외) |

**Object 분리 저장**:
- 재사용 가능한 다이어그램은 `templates/contents/objects/`에 별도 저장
- 템플릿에서 `shape_source: reference`로 참조

**참조**:
- **ppt-extract** 스킬의 content-extract 워크플로우 (추출 관련)
- [content-schema.md](references/content-schema.md) v2.1 스키마

이 규칙으로:
- 복잡한 도형 100% 보존 (OOXML)
- 단순 도형은 자연어로 간결화
- 재사용 가능한 Object 컴포넌트
- 일관된 디자인 품질 보장

## 3-Type Template System (v3.0)

> **v3.0 Update**: 템플릿이 스킬에서 분리되어 프로젝트 루트(`C:/project/docs/templates/`)에 저장됩니다.
> 테마와 컨텐츠가 분리되어 독립적으로 관리됩니다.

템플릿은 3가지 타입으로 관리됩니다:

| 타입 | 경로 | 용도 |
|------|------|------|
| 테마 | `C:/project/docs/templates/themes/` | 색상/폰트/스타일 정의 (deepgreen, brandnew, default) |
| 콘텐츠 템플릿 | `C:/project/docs/templates/contents/` | 슬라이드 패턴 (테마 독립적, 디자인 토큰 사용) |
| 문서 템플릿 | `C:/project/docs/templates/documents/` | 그룹/회사별 문서 양식 |
| 공용 에셋 | `C:/project/docs/templates/assets/` | 공용 이미지/아이콘 |

### 테마 선택 (MANDATORY)

**PPT 생성 시작 전 반드시 테마를 선택해야 합니다.**

```markdown
## 🎨 테마 선택

| # | 테마 | 설명 | 주요 색상 |
|---|------|------|----------|
| 1 | **Deep Green** | 자연스럽고 깔끔한 딥그린 | 🟢 #1E5128 / 🟩 #4E9F3D |
| 2 | **Brand New** | 신선한 스카이블루 | 🔵 #7BA4BC / 🩷 #F5E1DC |
| 3 | **Default** | 중립적인 기본 블루 | 💙 #2563EB / 🩵 #DBEAFE |

> 번호 선택 또는 직접 색상 지정 가능
```

### 디자인 토큰 시스템

콘텐츠 템플릿은 실제 색상 대신 디자인 토큰을 사용합니다:

```yaml
# 템플릿 (디자인 토큰)
style:
  fill:
    color: primary      # ← 토큰
  text:
    font_color: light   # ← 토큰

# 테마 적용 후 (실제 색상)
style:
  fill:
    color: "#1E5128"    # ← Deep Green primary
  text:
    font_color: "#FFFFFF"
```

**사용 가능한 디자인 토큰**:
- `primary`: 주요 강조색
- `secondary`: 보조 강조색
- `accent`: 하이라이트
- `background`: 배경색
- `surface`: 카드/패널 배경
- `dark_text`: 본문 텍스트
- `light`: 밝은 텍스트
- `gray`: 음소거 요소

## Dependencies

Required dependencies (should already be installed):

### Node.js
- **pptxgenjs**: Creating presentations via html2pptx
- **playwright**: HTML rendering in html2pptx
- **sharp**: SVG rasterization and image processing
- **react-icons, react, react-dom**: Icons

### Python
- **markitdown**: `pip install "markitdown[pptx]"` (text extraction)
- **python-pptx**: PPTX manipulation
- **defusedxml**: Secure XML parsing

### System
- **LibreOffice** (`soffice`): PPTX → PDF conversion (required for thumbnails)
  - Linux: `apt install libreoffice`
  - macOS: `brew install --cask libreoffice`
- **Poppler** (`pdftoppm`): PDF → Image conversion (required for thumbnails)
  - Linux: `apt install poppler-utils`
  - macOS: `brew install poppler`

## Code Style Guidelines

**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements
- **임시 스크립트는 절대로 스킬 폴더 안에 생성 금지** → 프로젝트 루트에 생성

## References

| 문서 | 용도 |
|------|------|
| [html2pptx.md](html2pptx.md) | HTML→PPTX 변환 상세 가이드 |
| [ooxml.md](ooxml.md) | OOXML 편집 상세 가이드 |
| [references/content-schema.md](references/content-schema.md) | 콘텐츠 템플릿 v2.0 스키마 |
| [references/design-intent.md](references/design-intent.md) | 디자인 의도 분류 |
| [references/color-palettes.md](references/color-palettes.md) | 색상 팔레트 레퍼런스 |

## 미구현 사항 (TODO)

스킬 사용 중 "뭐가 안 돼?" 질문 시 아래 목록 참조:

- [ ] **이미지 생성 모델 연동**: MCP를 통한 DALL-E, Midjourney, Stable Diffusion 연결
  - 현재: 이미지 생성 프롬프트 생성만 지원 (`scripts/image-prompt-generator.js`)
  - 향후: 프롬프트 → 이미지 자동 생성 → PPT 삽입 파이프라인

---

## 완료 후 정리

**중요**: 스킬 작업 완료 시 생성한 임시 파일을 반드시 삭제합니다.

### 삭제 대상

1. **프로젝트 루트 임시 스크립트**:
   - `extract_*.py`
   - `generate_*.py`
   - `*_thumbnail*.py`
   - `create_thumbnail.py`
   - `shapes_data.json`

2. **임시 작업 파일**:
   - 작업용 `.pptx` 파일 (사용자 요청 최종 출력물 제외)
   - 임시 `.pdf` 파일
   - 다운로드한 참조 이미지 (templates/ 외부)

3. **스킬 디렉토리 내 파일** (생성 금지 위반 시):
   - 임시 스크립트가 스킬 폴더에 생성되었다면 즉시 삭제

### 보존 대상 (삭제 금지)

- `templates/` 하위 모든 파일
- `registry.yaml` 파일들
- 사용자가 명시적으로 요청한 최종 출력물
- 기존 스킬 스크립트 (`scripts/` 내 기본 파일)
