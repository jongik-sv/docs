---
name: ppt-gen
description: "AI-powered PPT generation service. Use when: (1) Creating presentations from Markdown/JSON content, (2) Using templates to generate branded presentations, (3) Modifying or editing existing presentations, (4) Automating slide design with LLM-based layout selection"
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
| "콘텐츠 추출해줘", "슬라이드 저장" | content-extract | [workflows/content-extract.md](workflows/content-extract.md) |
| "문서 양식 추출해줘", "템플릿 등록" | document-extract | [workflows/document-extract.md](workflows/document-extract.md) |
| "이 이미지 스타일로" | style-extract | [workflows/style-extract.md](workflows/style-extract.md) |
| "PPT 디자인 찾아줘" | design-search | [workflows/design-search.md](workflows/design-search.md) |
| "템플릿 목록/삭제" | template-manage | [workflows/template-manage.md](workflows/template-manage.md) |
| "이 아이콘/이미지 저장해줘" | asset-manage | [workflows/asset-manage.md](workflows/asset-manage.md) |
| "썸네일 생성해줘" | thumbnail | [workflows/thumbnail.md](workflows/thumbnail.md) |

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## 3-Type Template System

템플릿은 3가지 타입으로 관리됩니다:

| 타입 | 경로 | 용도 |
|------|------|------|
| 문서 템플릿 | `templates/documents/{그룹}/` | 그룹/회사별 테마, 에셋, 문서 양식 |
| 콘텐츠 템플릿 | `templates/contents/` | 슬라이드 패턴 (표지, 목차, 비교표 등) |
| 공용 에셋 | `templates/assets/` | 그룹/회사 무관한 공용 이미지/아이콘 |

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
- **LibreOffice**: PDF conversion
- **Poppler**: pdftoppm for PDF to images

## Code Style Guidelines

**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

## References

| 문서 | 용도 |
|------|------|
| [html2pptx.md](html2pptx.md) | HTML→PPTX 변환 상세 가이드 |
| [ooxml.md](ooxml.md) | OOXML 편집 상세 가이드 |
| [references/content-schema.md](references/content-schema.md) | 콘텐츠 템플릿 v2.0 스키마 |
| [references/design-intent.md](references/design-intent.md) | 디자인 의도 분류 |
| [references/color-palettes.md](references/color-palettes.md) | 색상 팔레트 레퍼런스 |
