# PPT 자동 생성 서비스 - 구현 현황

## 핵심 결정사항

| 항목 | 결정 |
|------|------|
| 구현 방식 | Skills만 사용 (MCP 제외) |
| 기술 스택 | PptxGenJS + html2pptx.js |
| 템플릿 DB | YAML 기반 (LLM이 직접 선택) |
| 템플릿 구조 | 3타입 분리 (문서 + 콘텐츠 + 에셋) |

---

## 워크플로우 (7가지)

| # | 워크플로우 | 트리거 | 상태 |
|---|-----------|--------|------|
| 1 | html2pptx | 새 PPT 생성 요청 | ✅ 완료 |
| 2 | template | 회사 양식으로 생성 | ✅ 완료 |
| 3 | ooxml | 기존 PPT 수정 | ✅ 완료 |
| 4 | template-analyze | PPT → YAML 등록 | ✅ 완료 |
| 5 | style-extract | 이미지 스타일 추출 | ✅ 완료 |
| 6 | design-search | 디자인 레퍼런스 검색 | ✅ 완료 |
| 7 | template-manage | 템플릿 목록/삭제 | ✅ 완료 |
| 8 | asset-manage | 에셋 관리 | ✅ 완료 |
| 9 | slide-crawl | 온라인 슬라이드 크롤링 | ✅ 완료 |

---

## 템플릿 3타입 구조

| 타입 | 폴더 | 설명 |
|------|------|------|
| 문서 | `documents/{그룹}/` | 회사/브랜드별 전체 PPT 양식 |
| 콘텐츠 | `contents/` | 슬라이드 패턴 (cover, timeline 등) |
| 에셋 | `assets/` | 공용 이미지/아이콘 |

---

## 구현 현황

### Phase 1: 핵심 스크립트 ✅ 완료

| 파일 | 상태 |
|------|------|
| `SKILL.md` | ✅ |
| `html2pptx.md` | ✅ |
| `ooxml.md` | ✅ |
| `scripts/html2pptx.js` | ✅ |
| `scripts/inventory.py` | ✅ |
| `scripts/replace.py` | ✅ |
| `scripts/rearrange.py` | ✅ |
| `scripts/thumbnail.py` | ✅ |

### Phase 2: 3타입 템플릿 시스템 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `templates/documents/dongkuk/` | ✅ | 동국그룹 폴더 |
| `templates/documents/dongkuk/config.yaml` | ✅ | 그룹 테마 |
| `templates/documents/dongkuk/registry.yaml` | ✅ | 양식 목록 |
| `templates/documents/dongkuk/제안서1.yaml` | ✅ | 제안서 양식 |
| `templates/contents/registry.yaml` | ✅ | 콘텐츠 레지스트리 |
| `templates/contents/templates/*.yaml` | ✅ | 8개 콘텐츠 템플릿 |
| `templates/assets/registry.yaml` | ✅ | 에셋 레지스트리 |
| `scripts/template-analyzer.py` | ✅ | PPTX → YAML 분석 (3타입 구조 지원) |

### Phase 3: 레퍼런스 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `references/custom-elements.md` | ✅ | 요소 스키마 (HTML 태그, CSS, Placeholder) |
| `references/design-system.md` | ✅ | 디자인 규칙 (타이포, 레이아웃, 검증) |
| `references/color-palettes.md` | ✅ | 컬러 팔레트 (브랜드 + 18개 범용) |

### Phase 4: 유틸리티 스크립트 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `scripts/asset-manager.py` | ✅ | 에셋 관리 CLI (추가/검색/삭제) |
| `scripts/template-manager.py` | ✅ | 템플릿 관리 CLI (목록/아카이브/삭제) |
| `scripts/style-extractor.py` | ✅ | 이미지 스타일 추출 (색상 분석) |
| `scripts/slide-crawler.py` | ✅ | 온라인 슬라이드 크롤링 |

---

## 완료 현황

1. ~~폴더 구조 생성~~ ✅
2. ~~registry.yaml 파일들 생성~~ ✅
3. ~~template-analyzer.py 스크립트 구현~~ ✅
4. ~~dongkuk 그룹 샘플 템플릿 구현~~ ✅
5. ~~Phase 3: 레퍼런스 문서 작성~~ ✅
6. ~~Phase 4: 유틸리티 스크립트 구현~~ ✅
7. ~~GUIDE.md 학습 가이드 작성~~ ✅

**모든 Phase 및 문서화 완료!**

---

## 기술 스택

- **Node.js**: pptxgenjs, playwright, sharp
- **Python**: python-pptx, markitdown, defusedxml


skills.cokac.com 에서 스킬 등록해서 배포 할 수 있음
https://www.youtube.com/watch?v=rNtpNY41h5o 코깍노 참고


이 컨텐츠를 재사용하려면 썸네일도 있어야 하고 컨텐츠의 모양을 더 자세하게 표편해야해. 각 도형의 종류와, 도형 또는 텍스트에 대한 ppt 페이지(1980x1080 크기로 치환)의 좌표(x, y), 크기(cx, cy) 스타일(투명도, 그림자 설정), 오브젝트간 상대적 거리와 계층 구조의 벡터화,  색상(다른 테마로 쉽게 바꿀 수 있는 형태; primary, secondery 등으로 표현), LLM의 디자인 품질 점수(9.5/10.0), 디자인 의도(Comparision, Timeline, FeatureSpec, Hierarchy, ... 등), 추가적인 정보로 아이콘 크기,  아이콘 종류 등을 추출해야 디자인에 대한 재사용이 가능해.



 SKILL.md 를 리펙토링 하자. 각 워크플로우별로 지시를 분리해서 관리하는 것이 좋겠어. 

 각 추출한 컨텐츠는 폴더로 분류해서 저장하는 것이 좋겠어.
 