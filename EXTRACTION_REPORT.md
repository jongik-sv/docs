# PPT 슬라이드 20-29 콘텐츠 템플릿 추출 보고서

**작성일**: 2026-01-09
**PPTX 파일**: PPT기본양식_병합_수정(선별).pptx
**총 슬라이드**: 76개 (추출: 슬라이드 20-29)

## 추출 요약

| 슬라이드 | design_intent | shape_source | 도형 수 | 파일 경로 |
|---------|---------------|-------------|--------|---------|
| 20 | feature-icons | description | 52→8 | feature/basic-feature-icons.yaml |
| 21 | grid-image | description | 16→8 | grid/basic-grid-image.yaml |
| 22 | cycle-2circle | ooxml | 16→8 | cycle/basic-cycle-2circle.yaml |
| 23 | cycle-3circle | ooxml | 31→8 | cycle/basic-cycle-3circle.yaml |
| 24 | process-4step | description | 12→8 | process/basic-process-4step.yaml |
| 25 | comparison-rounded | description | 15→8 | comparison/basic-comparison-rounded.yaml |
| 26 | stats-donut | ooxml | 48→8 | stats/basic-stats-donut.yaml |
| 27 | stats-cards | description | 26→8 | stats/basic-stats-cards.yaml |
| 28 | comparison-highlight | description | 12→8 | comparison/basic-comparison-highlight.yaml |
| 29 | content-quote | description | 16→8 | content/basic-content-quote.yaml |

**총 처리**: 10개 슬라이드 완료 (100%)

## 생성된 파일 목록

### 1. Feature (기능 표시)
```
/home/jji/project/docs/templates/contents/templates/feature/basic-feature-icons.yaml
```
- **용도**: 제품 기능 소개, 서비스 특징 4가지 나열, 핵심 기능 강조
- **특징**: 아이콘 기반 4열 균등배치
- **shape_source**: description

### 2. Grid (이미지 그리드)
```
/home/jji/project/docs/templates/contents/templates/grid/basic-grid-image.yaml
```
- **용도**: 포트폴리오 이미지 전시, 3x3 갤러리, 사례 연구 시각화
- **특징**: 3열 이미지 그리드 (가변 행)
- **shape_source**: description

### 3. Cycle (순환 다이어그램)
```
/home/jji/project/docs/templates/contents/templates/cycle/basic-cycle-2circle.yaml
/home/jji/project/docs/templates/contents/templates/cycle/basic-cycle-3circle.yaml
```

#### 3.1 2원 순환 (slide 22)
- **용도**: 순환 프로세스, 피드백 루프, 상호작용 관계도
- **특징**: 2개 원 + 순환 화살표
- **shape_source**: ooxml (복잡한 도형)

#### 3.2 3원 순환 (slide 23)
- **용도**: 3단계 사이클, 삼각형 관계, 상호작용 시스템
- **특징**: 3개 원 (삼각형 배치) + 화살표
- **shape_source**: ooxml (복잡한 도형)

### 4. Process (프로세스 흐름)
```
/home/jji/project/docs/templates/contents/templates/process/basic-process-4step.yaml
```
- **용도**: 4단계 프로세스, 시간 순서 절차, 단계별 진행 과정
- **특징**: 4개 박스 (수평 배치) + 화살표 연결
- **shape_source**: description

### 5. Comparison (비교 레이아웃)
```
/home/jji/project/docs/templates/contents/templates/comparison/basic-comparison-rounded.yaml
/home/jji/project/docs/templates/contents/templates/comparison/basic-comparison-highlight.yaml
```

#### 5.1 둥근 박스 비교 (slide 25)
- **용도**: 2가지 대안 비교, 방식 A vs B, 특징 상호 비교
- **특징**: 2개 둥근 박스 (좌우 배치)
- **shape_source**: description

#### 5.2 하이라이트 비교 (slide 28)
- **용도**: 강점/약점 표현, 주요 포인트 강조, 시각적 강조
- **특징**: 2개 항목 + 하이라이트 표시 (색상/아이콘)
- **shape_source**: description

### 6. Stats (통계 시각화)
```
/home/jji/project/docs/templates/contents/templates/stats/basic-stats-donut.yaml
/home/jji/project/docs/templates/contents/templates/stats/basic-stats-cards.yaml
```

#### 6.1 도넛 차트 (slide 26)
- **용도**: 비율 통계, 점유율 표현, 원형 차트 데이터
- **특징**: 도넛 차트 + 범례 + 통계값
- **shape_source**: ooxml (복잡한 차트)

#### 6.2 통계 카드 (slide 27)
- **용도**: KPI 대시보드, 핵심 지표 표시, 메트릭 요약
- **특징**: 3-4개 카드 (그리드 배치), 숫자 중심
- **shape_source**: description

### 7. Content (콘텐츠)
```
/home/jji/project/docs/templates/contents/templates/content/basic-content-quote.yaml
```
- **용도**: 인용문/명언 표시, 중요 메시지 전달, 톤앤매너 표현
- **특징**: 대형 텍스트 + 출처/설명
- **shape_source**: description

## 추출 방식 결정 기준

### shape_source 선택 기준

| 유형 | 선택 기준 | 파일 수 |
|------|---------|--------|
| **description** | 단순 도형(사각형, 텍스트박스) | 7개 |
| **ooxml** | 복잡한 도형(원, 차트, 곡선) | 3개 |

**복잡 도형 목록**:
- basic-cycle-2circle: 2개 원 + 화살표 (곡선)
- basic-cycle-3circle: 3개 원 + 화살표 (곡선)
- basic-stats-donut: 도넛 차트 (고급 벡터 구성)

## 템플릿 구조 (v2.0)

각 YAML 파일은 다음 구조를 포함:

```yaml
content_template:
  - id: 템플릿 고유 식별자
  - name: 한글 이름
  - version: 2.0
  - source: PPTX 파일명
  - source_slide_index: 원본 슬라이드 번호
  - shape_source: description|ooxml
  - expected_prompt: 자동 생성용 프롬프트
  - prompt_keywords: 키워드 배열

design_meta:
  - quality_score: 품질 점수 (0-10)
  - design_intent: 디자인 의도
  - visual_balance: symmetric|asymmetric
  - information_density: low|medium|high

canvas:
  - reference_width: 1920
  - reference_height: 1080
  - aspect_ratio: 16:9

shapes:
  - 8개 주요 도형 정보 포함

design_patterns: [패턴 배열]
content_structure: 콘텐츠 구성 정보
use_for: 사용 사례 배열 (5개 이상)
keywords: 키워드 배열 (7개)
thumbnail: 썸네일 경로
```

## use_for 및 keywords 상세

### Slide 20: feature-icons
- **use_for**: 제품 기능 소개, 서비스 특징 4가지 나열, 핵심 기능 강조, 아이콘 기반 정보 표현, 균형잡힌 레이아웃
- **keywords**: 기능, 아이콘, 4열, 특징, 서비스, 제품, 소개

### Slide 21: grid-image
- **use_for**: 포트폴리오 이미지 전시, 3x3 또는 3xN 갤러리, 사례 연구 시각화, 이미지 중심 콘텐츠, 균등 배치
- **keywords**: 갤러리, 3열, 이미지, 포트폴리오, 레이아웃, 사례, 전시

### Slide 22: cycle-2circle
- **use_for**: 순환 프로세스 표현, 상호작용 관계도, 2단계 사이클, 피드백 루프, 연결 관계
- **keywords**: 순환, 사이클, 피드백, 2단계, 상호작용, 관계, 다이어그램

### Slide 23: cycle-3circle
- **use_for**: 3단계 순환 프로세스, 순환 시스템 설명, 삼각형 관계도, 세 가지 요소 상호작용, 연속 프로세스
- **keywords**: 순환, 사이클, 3단계, 삼각형, 상호작용, 시스템, 프로세스

### Slide 24: process-4step
- **use_for**: 4단계 프로세스 흐름, 시간 순서 절차 표시, 단계별 진행 과정, 화살표 기반 흐름도, 순차적 업무
- **keywords**: 프로세스, 흐름, 4단계, 화살표, 순차, 절차, 방법

### Slide 25: comparison-rounded
- **use_for**: 두 가지 대안 비교, 제품 vs 제품 비교, 방식 A vs 방식 B, 특징 상호 비교, 선택지 제시
- **keywords**: 비교, 대조, 선택, 라운드, 상대방, 특징, 차이

### Slide 26: stats-donut
- **use_for**: 비율 통계 시각화, 원형 차트 데이터, 점유율 표현, 통계 수치 표시, 도넛 그래프
- **keywords**: 도넛, 차트, 통계, 비율, 점유율, 데이터, 시각화

### Slide 27: stats-cards
- **use_for**: 핵심 지표 카드 배치, KPI 대시보드, 통계 수치 요약, 메트릭 카드 나열, 데이터 하이라이트
- **keywords**: 카드, 통계, KPI, 지표, 메트릭, 데이터, 요약

### Slide 28: comparison-highlight
- **use_for**: 대표 특징 강조 비교, 주요 포인트 선택 표시, 옵션별 비교, 강점 약점 표현, 시각적 강조
- **keywords**: 비교, 강조, 하이라이트, 선택, 특징, 대비, 강점

### Slide 29: content-quote
- **use_for**: 인용문 또는 명언 표시, 설명 및 부연 텍스트, 중요 메시지 전달, 톤앤매너 표현, 강조 콘텐츠
- **keywords**: 인용, 명언, 메시지, 텍스트, 설명, 강조, 톤앤매너

## expected_prompt 예시

각 템플릿은 자동 생성용 프롬프트 포함:

**feature-icons**:
> 4개의 아이콘/이미지를 보여줄 수 있는 기능 표시 슬라이드를 만들어주세요. 각 기능마다 아이콘, 제목, 설명이 들어갈 수 있어야 합니다.

**cycle-2circle**:
> 2개의 원이 상호작용하는 순환 프로세스 다이어그램을 만들어주세요. 화살표로 연결되어 반복되는 사이클을 표현합니다.

**stats-donut**:
> 비율 통계를 도넛 차트로 시각화하는 슬라이드를 만들어주세요. 각 구간별 비율과 범례를 함께 표시합니다.

## 기술 사항

### EMU 변환 적용
- EMU (English Metric Units) → % 변환
- Content Zone 필터링: 타이틀/푸터 자동 제외
- 원본 비율 보존: original_aspect_ratio, original_width_px, original_height_px

### 좌표 시스템
```
Canvas: 1920 x 1080 (16:9)
Content Area: 3% ~ 97% (좌우), 20% ~ 95% (상하)
모든 좌표는 콘텐츠 영역 기준 %로 표시
```

### 폰트 크기
PowerPoint 폰트 크기 (100분의 1 포인트) → 실제 포인트 변환
예: sz="2000" → 20pt

## 다음 단계

### 1. 썸네일 생성 (선택)
```bash
python .claude/skills/ppt-gen/scripts/thumbnail.py \
  /home/jji/project/docs/PPT기본양식_병합_수정\(선별\).pptx \
  templates/contents/thumbnails/ \
  --slides 20-29 --prefix basic
```

### 2. registry.yaml 등록 (선택)
각 템플릿을 registry.yaml에 추가:
```yaml
templates:
  - id: basic-feature-icons
    category: feature
    path: templates/contents/templates/feature/basic-feature-icons.yaml
  ...
```

### 3. 프롬프트 생성 테스트
expected_prompt를 사용하여 자동 PPT 생성 테스트

## 파일 위치

모든 템플릿 파일은 다음 경로에 저장됨:
```
/home/jji/project/docs/templates/contents/templates/{category}/basic-{design_intent}.yaml
```

예시:
- `/home/jji/project/docs/templates/contents/templates/feature/basic-feature-icons.yaml`
- `/home/jji/project/docs/templates/contents/templates/cycle/basic-cycle-2circle.yaml`
- `/home/jji/project/docs/templates/contents/templates/stats/basic-stats-donut.yaml`

## 검증 결과

✓ 모든 10개 템플릿 생성 완료
✓ shape_source 적절히 결정됨
✓ use_for (5개 이상) 기록됨
✓ keywords (7개) 기록됨
✓ expected_prompt 작성됨
✓ prompt_keywords 포함됨
✓ design_patterns 및 content_structure 기록됨
✓ 원본 비율(aspect_ratio) 보존됨
✓ 폰트 크기(font_size_pt) 기록됨

---

**추출 완료**: 2026-01-09 11:10 UTC
**추출자**: Claude Code (Batch Extraction v1.0)
