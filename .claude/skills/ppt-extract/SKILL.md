---
name: ppt-extract
description: "PPT 템플릿/에셋 추출 서비스. Use when: (1) 슬라이드에서 콘텐츠/오브젝트 추출, (2) PPTX에서 문서 양식/슬라이드 마스터 추출, (3) 이미지에서 테마/스타일 추출, (4) 온라인 슬라이드 크롤링"
---

# PPT Template Extraction Service

PPTX, 이미지에서 재사용 가능한 템플릿과 에셋을 추출합니다. PPT 생성 파이프라인(ppt-gen)과 독립적으로 실행됩니다.

## Workflow Selection

| 요청 유형 | 워크플로우 | 가이드 |
|----------|-----------|--------|
| "콘텐츠 추출해줘", "슬라이드 저장" | content-extract | [workflows/content-extract.md](workflows/content-extract.md) |
| "문서 양식 추출해줘", "템플릿 등록" | document-extract | [workflows/document-extract.md](workflows/document-extract.md) |
| "이 이미지 스타일로" | style-extract | [workflows/style-extract.md](workflows/style-extract.md) |

## Output Structure

추출 결과물은 `templates/` 폴더에 저장됩니다:

```
C:/project/docs/templates/
├── themes/                  # 테마 정의 (style-extract 출력)
│   └── {theme-id}.yaml
├── contents/                # 콘텐츠 템플릿 (content-extract 출력)
│   ├── templates/{category}/
│   ├── objects/
│   └── registry.yaml
└── documents/               # 문서 템플릿 (document-extract 출력)
    └── {group}/
        ├── config.yaml
        ├── registry.yaml
        └── {양식}.yaml
```

## Dependencies

**Python:**
- python-pptx: PPTX 분석
- pyyaml: YAML 생성
- colorthief: 이미지 색상 추출
- Pillow: 이미지 처리
- defusedxml: XML 파싱

**System:**
- LibreOffice (`soffice`): 썸네일 생성용

## Scripts

| 스크립트 | 용도 |
|---------|------|
| `scripts/template-analyzer.py` | PPTX → YAML 분석 |
| `scripts/style-extractor.py` | 이미지 색상 추출 |
| `scripts/slide-crawler.py` | 온라인 슬라이드 크롤링 |

## Shared Resources (ppt-gen에서 공유)

추출 작업에 필요한 공유 스크립트:
- `ppt-gen/ooxml/scripts/unpack.py`: PPTX 언팩
- `ppt-gen/scripts/thumbnail.py`: 썸네일 생성
- `ppt-gen/scripts/asset-manager.py`: 에셋 관리/크롤링

## References

- [ppt-gen/references/content-schema.md](../ppt-gen/references/content-schema.md): 콘텐츠 템플릿 v4.0 스키마 (공유)
- [references/font-mappings.yaml](references/font-mappings.yaml): 폰트 매핑 정의
