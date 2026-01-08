# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PPT Skills Suite - Claude Code 환경에서 전문 디자이너 수준의 PPT를 자동 생성하고 관리하는 통합 서비스.

**구조**: 2개 스킬 + 1 앱
- `ppt-extract`: 템플릿/에셋 추출 (파이프라인 외부)
- `ppt-gen`: PPT 생성 (5단계 파이프라인)
- `ppt-manager`: 관리 앱 (Electron, 미구현)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ ppt-extract (추출)                                          │
│ • content-extract  : PPTX/이미지 → 콘텐츠 YAML             │
│ • document-extract : PPTX → 문서 템플릿 + OOXML            │
│ • style-extract    : 이미지 → 테마 YAML                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ 템플릿/에셋 등록
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ ppt-gen (생성) - 5단계 파이프라인                            │
│ 1. Setup → 2. Outline → 3. Matching → 4. Content → 5. PPTX │
│ • html2pptx : 새 PPT 생성                                  │
│ • template  : 템플릿 기반 생성                              │
│ • ooxml     : 기존 PPT 수정                                │
└─────────────────────────────────────────────────────────────┘
```

## Template System (v4.0)

```
templates/
├── themes/           # 테마 정의 (색상, 폰트)
│   └── {theme}.yaml
├── contents/         # 콘텐츠 템플릿 (슬라이드 패턴)
│   ├── templates/{category}/
│   ├── objects/      # 재사용 오브젝트
│   └── registry.yaml
├── documents/        # 문서 템플릿 (회사별 양식)
│   └── {group}/
│       ├── config.yaml
│       ├── registry.yaml
│       ├── {양식}.yaml
│       ├── assets/default/
│       └── ooxml/
└── assets/           # 공용 에셋
```

**디자인 토큰**: `primary`, `secondary`, `accent`, `background`, `surface`, `dark_text`, `light`, `gray`

## Key Scripts

| 스크립트 | 위치 | 용도 |
|---------|------|------|
| `html2pptx.js` | ppt-gen/scripts | HTML → PPTX 변환 |
| `template-analyzer.py` | ppt-extract/scripts | PPTX → YAML 추출 |
| `inventory.py` | ppt-gen/scripts | 텍스트 추출 |
| `replace.py` | ppt-gen/scripts | 텍스트 교체 |
| `thumbnail.py` | ppt-gen/scripts | 썸네일 생성 |

## Common Commands

```bash
# HTML → PPTX 변환
node .claude/skills/ppt-gen/scripts/html2pptx.js slides/ output.pptx

# PPTX에서 문서 템플릿 추출
python .claude/skills/ppt-extract/scripts/template-analyzer.py input.pptx 템플릿ID --group 그룹ID

# 텍스트 추출
python .claude/skills/ppt-gen/scripts/inventory.py input.pptx > inventory.json

# 썸네일 생성 (검증용)
python .claude/skills/ppt-gen/scripts/thumbnail.py input.pptx output_dir/ --cols 4
```

## Dependencies

**Node.js**: pptxgenjs, playwright, sharp, react-icons

**Python**: python-pptx, pyyaml, markitdown, defusedxml, Pillow, colorthief

**System**: LibreOffice (soffice), Poppler (pdftoppm)

## Critical Rules

1. **Template Priority Rule**: PPT 생성 시 반드시 `registry.yaml` 검색 후 템플릿 매칭. 매칭 없이 직접 디자인 금지.

2. **Shape Source Types** (v2.1):
   - `ooxml`: 복잡한 도형 원본 보존
   - `svg`: SVG 벡터
   - `reference`: 다른 shape 참조
   - `html`: HTML 스니펫
   - `description`: 자연어 설명

3. **Output 폴더 구조**:
   ```
   output/{session-id}/
   ├── session.json
   ├── stage-1-setup.json
   ├── stage-2-outline.json
   ├── stage-3-matching.json
   ├── stage-4-content.json
   ├── stage-5-generation.json
   ├── slides/*.html
   └── output.pptx
   ```

4. **임시 파일 정리**: 작업 완료 후 `workspace/`, 루트의 임시 스크립트 삭제 필수. `templates/` 하위는 보존.

## Content Categories (19개)

cover, toc, section, comparison, process, chart, stats, grid, diagram, timeline, content, quote, closing, cycle, matrix, feature, flow, table, infographic
