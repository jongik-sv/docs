# ppt-extract

PPT/이미지에서 재사용 가능한 템플릿과 스타일을 추출하는 Claude Code 스킬.

## 개요

| 항목 | 값 |
|------|---|
| 스킬 타입 | Claude Code Skill |
| 버전 | 1.0 |
| 의존 스킬 | ppt-create (thumbnail.py 사용) |

## 워크플로우

### 1. content-extract (콘텐츠 템플릿 추출)

**트리거**: "이 슬라이드 저장해줘", "콘텐츠 추출해줘"

**처리 흐름 (v4.0 콘텐츠-오브젝트 분리)**:
1. PPT 슬라이드 분석
2. 디자인 의도 파악 (40가지 카테고리)
3. **콘텐츠 분리**: 배치(zones) + 레이아웃(layout) 추출
4. **오브젝트 분리**: 복잡한 도형은 별도 오브젝트 파일로 추출
   - OOXML 도형 → `objects/` 폴더
   - 간단한 도형 → `object_desc` (설명만)
5. YAML 템플릿 생성 (v4.0 스키마)
6. 썸네일 생성
7. registry.yaml 업데이트
8. objects/registry.yaml 업데이트 (오브젝트 추출 시)

**v4.0 콘텐츠-오브젝트 분리 스키마**:
```yaml
# 콘텐츠 템플릿 (배치 중심)
content_template:
  id: process-visual1
  version: "4.0"

  content:
    layout:
      type: radial
      center: {x: 50%, y: 50%}

    zones:
      - id: main-diagram
        type: placeholder
        geometry: {x: 10%, y: 20%, cx: 80%, cy: 60%}
        placeholder_type: DIAGRAM

        # 동적 오브젝트 선택
        object_hint:
          category: [cycle, process]
          element_count: 4-6
        object_default: "objects/cycle/6segment.yaml"
```

**출력물**:
- `templates/contents/templates/{category}/{id}.yaml` (콘텐츠)
- `templates/contents/objects/{category}/{id}.yaml` (오브젝트)
- `templates/contents/thumbnails/{category}/{id}.png`

---

### 2. image-extract (이미지 레이아웃 추출) - NEW

**트리거**: "이 이미지 레이아웃 추출해줘", "이 디자인 템플릿으로 저장"

**입력 소스**:
- PPT 슬라이드 스크린샷
- Dribbble/Behance 디자인 이미지
- 와이어프레임 이미지
- 경쟁사 PPT 캡처

**처리 흐름**:
1. 이미지 분석 (LLM Vision)
2. 레이아웃 구조 파악:
   - 영역 분할 (zones)
   - 요소 배치 (geometry)
   - 디자인 의도 분류
3. 색상 팔레트 추출 (선택)
4. v4.0 콘텐츠 템플릿 생성
5. 썸네일로 원본 이미지 저장
6. registry.yaml 업데이트

**style-extract와 차이점**:

| 워크플로우 | 추출 대상 | 출력물 |
|-----------|----------|--------|
| `image-extract` | **레이아웃/구조** | 콘텐츠 템플릿 YAML |
| `style-extract` | **색상/무드** | 테마 YAML |

**출력물**:
- `templates/contents/templates/{category}/{id}.yaml`
- `templates/contents/thumbnails/{category}/{id}.png` (원본 이미지)

**사용 예시**:
```
사용자: "이 이미지 레이아웃 추출해줘" [Dribbble PPT 디자인 이미지]

Claude:
이미지를 분석하겠습니다.

분석 결과:
- 레이아웃: 2열 비교 구조
- 디자인 의도: comparison-2col
- 요소: 좌측 패널(제목+설명), 우측 패널(제목+설명)
- 색상: 파란색/회색 계열

콘텐츠 템플릿 생성 중...

저장 완료:
- 파일: templates/contents/templates/comparison/comparison-image1.yaml
- 썸네일: templates/contents/thumbnails/comparison/comparison-image1.png
```

---

### 3. document-extract (문서 템플릿 추출)

**트리거**: "이 PPT를 양식으로 등록해줘", "문서 템플릿 추출"

**처리 흐름**:
1. 전체 PPT 구조 분석
2. 그룹/회사 정보 입력
3. 테마 추출 (색상, 폰트)
4. 슬라이드별 카테고리 분류
5. 문서 템플릿 YAML 생성
6. 에셋 복사 (로고 등)

**출력물**:
- `templates/documents/{group}/config.yaml`
- `templates/documents/{group}/registry.yaml`
- `templates/documents/{group}/{name}.yaml`
- `templates/documents/{group}/assets/`

---

### 3. style-extract (이미지 스타일 추출)

**트리거**: "이 이미지 스타일로", "스타일 추출해줘"

**처리 흐름**:
1. 이미지 분석 (LLM Vision 또는 CLI)
2. 색상 추출 (5-6개)
3. 역할 분류 (primary, secondary, accent, background, text)
4. 테마 파일 생성 또는 업데이트

**출력물**:
- `templates/themes/{name}.yaml`

---

## 스크립트

| 스크립트 | 줄수 | 역할 |
|---------|------|------|
| `template-analyzer.py` | 528 | PPTX → YAML 분석 |
| `style-extractor.py` | 383 | 이미지 색상 추출 |
| `slide-crawler.py` | 516 | 온라인 슬라이드 크롤링 |

---

## 디자인 의도 카테고리 (40가지)

- **Cover**: cover-centered, cover-photo, cover-minimal
- **TOC**: toc-list, toc-grid, toc-timeline
- **Section**: section-number, section-icon
- **Comparison**: comparison-2col, pros-cons, before-after
- **Process**: process-linear, process-circular, process-honeycomb
- **Stats**: stats-cards, stats-chart, stats-infographic
- **Grid**: grid-icon, grid-image, grid-feature
- **Diagram**: cycle, venn, matrix, hierarchy, flow
- **Timeline**: timeline-horizontal, timeline-vertical
- **Quote**: quote-centered, quote-with-image
- **Closing**: closing-thankyou, closing-contact

---

## 사용 예시

### v4.0 콘텐츠-오브젝트 분리 추출

```
사용자: "이 슬라이드 저장해줘" [PPT 첨부 - 6단계 순환 다이어그램]

Claude:
슬라이드를 분석하겠습니다.

분석 결과:
- 디자인 의도: cycle-6segment
- 카테고리: cycle
- 품질 점수: 9.2
- 복잡한 도형 감지: 6개 세그먼트 (OOXML 추출 필요)

콘텐츠-오브젝트 분리 중...

저장 완료:
1. 콘텐츠 템플릿:
   - 파일: templates/contents/templates/cycle/cycle-6segment1.yaml
   - 내용: 레이아웃(radial) + zones(6개 세그먼트 위치)

2. 오브젝트 파일:
   - 파일: templates/contents/objects/cycle/6segment-colorful.yaml
   - 타입: ooxml
   - 내용: 6개 세그먼트 path 정의

3. 레지스트리 업데이트:
   - contents/registry.yaml 업데이트
   - objects/registry.yaml 업데이트

4. 썸네일:
   - templates/contents/thumbnails/cycle/cycle-6segment1.png
```

### 간단한 도형 (설명만 추출)

```
사용자: "이 슬라이드 저장해줘" [PPT 첨부 - 2열 비교]

Claude:
슬라이드를 분석하겠습니다.

분석 결과:
- 디자인 의도: comparison-2col
- 카테고리: comparison
- 품질 점수: 9.0
- 복잡한 도형: 없음 (단순 사각형)

콘텐츠만 추출합니다 (오브젝트 불필요):

저장 완료:
1. 콘텐츠 템플릿:
   - 파일: templates/contents/templates/comparison/comparison-2col1.yaml
   - zones 내용:
     - left-panel: object_desc: "둥근 모서리 사각형, primary 배경"
     - right-panel: object_desc: "둥근 모서리 사각형, secondary 배경"

2. 오브젝트 파일: 생성 안 함 (간단한 도형)
```

---

## 의존성

**Python**:
- python-pptx
- pyyaml
- Pillow
- colorthief
- beautifulsoup4 (slide-crawler)
- playwright (slide-crawler)

**참조**:
- `ppt-create/scripts/thumbnail.py` (썸네일 생성)
