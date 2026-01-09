# 슬라이드 50-59 콘텐츠 템플릿 추출 보고서

**추출 일시**: 2026-01-09 11:10-11:17  
**원본 PPTX**: /home/jji/project/docs/PPT기본양식_병합_수정(선별).pptx (76개 슬라이드)  
**언팩 경로**: /home/jji/project/docs/workspace/unpacked  
**출력 경로**: /home/jji/project/docs/templates/contents/templates/  

## 추출 결과 요약

총 10개 슬라이드를 분석하여 YAML 템플릿 및 썸네일을 생성했습니다.

| 슬라이드 | Design Intent | 템플릿 파일 | 도형 수 | 썸네일 |
|---------|---------------|-----------|--------|--------|
| 50 | basic-grid-3col | grid/basic-grid-3col1.yaml | 37 | OK |
| 51 | basic-timeline-circular | timeline/basic-timeline-circular1.yaml | 19 | OK |
| 52 | basic-process-5step | process/basic-process-5step1.yaml | 10 | OK |
| 53 | basic-process-chevron | process/basic-process-chevron1.yaml | 31 | OK |
| 54 | basic-roadmap-yearly | roadmap/basic-roadmap-yearly1.yaml | 39 | OK |
| 55 | basic-timeline-milestone | timeline/basic-timeline-milestone1.yaml | 16 | OK |
| 56 | basic-process-3step | process/basic-process-3step1.yaml | 36 | OK |
| 57 | basic-timeline-arrow | timeline/basic-timeline-arrow1.yaml | 23 | OK |
| 58 | basic-timeline-progress | timeline/basic-timeline-progress1.yaml | 16 | OK |
| 59 | basic-process-6step | process/basic-process-6step1.yaml | 26 | OK |

**총 도형 수**: 253개  
**생성 파일**: YAML 템플릿 10개 + 썸네일 10개

---

## 각 슬라이드 상세 정보

### 슬라이드 50: 3열 그리드 레이아웃
**파일**: `/home/jji/project/docs/templates/contents/templates/grid/basic-grid-3col1.yaml`  
**도형 수**: 37개  
**design_intent**: basic-grid-3col  
**특징**:
- 3개의 동일한 크기의 카드/열 구성
- 균형잡힌 시각적 배치
- 비교 또는 세 가지 옵션 표현에 적합

**사용 사례**:
- 제품 기능 비교
- 세 가지 옵션 제시
- 균등한 정보 배치
- 카테고리별 구분
- 대칭적 구성

**keywords**: 3열 그리드, 균형잡힌 레이아웃, 카드 배치, 비교 구성, 시각적 균형

**expected_prompt**: "3개 항목을 같은 크기의 카드로 표현하는 그리드 레이아웃"

---

### 슬라이드 51: 원형 타임라인
**파일**: `/home/jji/project/docs/templates/contents/templates/timeline/basic-timeline-circular1.yaml`  
**도형 수**: 19개  
**design_intent**: basic-timeline-circular  
**특징**:
- 중앙을 중심으로 순환하는 구조
- 원형 또는 순환 흐름 표현
- 지속적인 프로세스나 주기 표현에 적합

**사용 사례**:
- 순환 프로세스 설명
- 반복되는 주기 표현
- 지속적 개선 표시
- 순환 구조 시각화
- 루프 기반 프로세스

**keywords**: 원형 타임라인, 순환 구조, 시간 흐름, 프로세스 순환, 반복적 진행

**expected_prompt**: "중앙을 중심으로 순환하는 원형 타임라인 또는 프로세스"

---

### 슬라이드 52: 5단계 프로세스
**파일**: `/home/jji/project/docs/templates/contents/templates/process/basic-process-5step1.yaml`  
**도형 수**: 10개  
**design_intent**: basic-process-5step  
**특징**:
- 5개 단계의 순차적 표현
- 각 단계별 세부사항 포함 가능
- 복합 프로세스 표현에 적합

**사용 사례**:
- 5개 단계 설명
- 상세한 프로세스
- 단계별 세부사항
- 복합 업무 흐름
- 5단 진행

**keywords**: 5단계 프로세스, 단계별 진행, 업무 흐름, 연속 단계, 진행 과정

**expected_prompt**: "5개 단계를 순차적으로 표현하는 프로세스 다이어그램"

---

### 슬라이드 53: 쉐브론 프로세스
**파일**: `/home/jji/project/docs/templates/contents/templates/process/basic-process-chevron1.yaml`  
**도형 수**: 31개  
**design_intent**: basic-process-chevron  
**특징**:
- 쉐브론(화살표) 모양으로 단계 연결
- 선형 진행 표시
- 방향성이 명확한 프로세스 표현

**사용 사례**:
- 화살표 기반 흐름
- 선형 진행 표시
- 단계 연결 표현
- 방향성 프로세스
- 쉐브론 시각화

**keywords**: 쉐브론 프로세스, 화살표 시퀀스, 방향성 표현, 단계 흐름, 진행 표시

**expected_prompt**: "쉐브론 모양의 화살표로 단계를 연결하는 프로세스"

---

### 슬라이드 54: 연도별 로드맵
**파일**: `/home/jji/project/docs/templates/contents/templates/roadmap/basic-roadmap-yearly1.yaml`  
**도형 수**: 39개  
**design_intent**: basic-roadmap-yearly  
**특징**:
- 여러 연도의 이정표 표시
- 시간대별 계획 표현
- 장기 목표 설정에 적합

**사용 사례**:
- 연간 일정 계획
- 여러 해의 로드맵
- 시간대별 이정표
- 연도별 목표 표시
- 장기 타임라인

**keywords**: 연도별 로드맵, 타임라인, 연간 계획, 주요 이정표, 시간 기반 계획

**expected_prompt**: "여러 연도의 이정표를 표시하는 로드맵"

---

### 슬라이드 55: 마일스톤 타임라인
**파일**: `/home/jji/project/docs/templates/contents/templates/timeline/basic-timeline-milestone1.yaml`  
**도형 수**: 16개  
**design_intent**: basic-timeline-milestone  
**특징**:
- 주요 성과나 사건 강조
- 타임라인상의 마일스톤 표시
- 주요 성과 기반 진행 표현

**사용 사례**:
- 주요 성과 표시
- 마일스톤 강조
- 사건 시점 표현
- 타임라인 강조
- 성과 기반 진행

**keywords**: 마일스톤 타임라인, 성과 표시, 주요 사건, 타임라인 마킹, 기간별 진행

**expected_prompt**: "타임라인상에 마일스톤을 강조하여 표시"

---

### 슬라이드 56: 3단계 프로세스
**파일**: `/home/jji/project/docs/templates/contents/templates/process/basic-process-3step1.yaml`  
**도형 수**: 36개  
**design_intent**: basic-process-3step  
**특징**:
- 기본적인 3단계 프로세스
- 간단하고 명확한 구조
- 기초적인 업무 흐름 표현에 적합

**사용 사례**:
- 간단한 3단계
- 기본 프로세스
- 단순 흐름 표현
- 3가지 항목
- 기초 단계

**keywords**: 3단계 프로세스, 간단한 흐름, 3가지 단계, 순차적 진행, 단순 프로세스

**expected_prompt**: "3개 단계를 순차적으로 표현하는 프로세스"

---

### 슬라이드 57: 화살표 타임라인
**파일**: `/home/jji/project/docs/templates/contents/templates/timeline/basic-timeline-arrow1.yaml`  
**도형 수**: 23개  
**design_intent**: basic-timeline-arrow  
**특징**:
- 화살표로 연결된 타임라인
- 시각적 방향 지시
- 시간 순서 표현이 명확함

**사용 사례**:
- 화살표로 연결된 타임라인
- 시각적 흐름 표시
- 방향 지시
- 화살표 연결 흐름
- 시간 순서 표현

**keywords**: 화살표 타임라인, 방향성 시간선, 화살표 연결, 시각적 흐름, 진행 방향

**expected_prompt**: "화살표로 연결된 타임라인 또는 진행 흐름"

---

### 슬라이드 58: 진행바 타임라인
**파일**: `/home/jji/project/docs/templates/contents/templates/timeline/basic-timeline-progress1.yaml`  
**도형 수**: 16개  
**design_intent**: basic-timeline-progress  
**특징**:
- 진행 상태를 진행바로 표시
- 완료율 시각화
- 시간 기반 진행도 표현에 적합

**사용 사례**:
- 진행 상태 표시
- 완료율 표현
- 진행도 시각화
- 시간 기반 진행률
- 프로그레스 표시

**keywords**: 진행바 타임라인, 진행률 표시, 완료도 표현, 시간 기반 진행, 프로그레스

**expected_prompt**: "진행바로 진행 상태를 표시하는 타임라인"

---

### 슬라이드 59: 6단계 프로세스
**파일**: `/home/jji/project/docs/templates/contents/templates/process/basic-process-6step1.yaml`  
**도형 수**: 26개  
**design_intent**: basic-process-6step  
**특징**:
- 6개 단계의 복합 프로세스
- 확장된 워크플로우 표현
- 상세한 단계별 설명 가능

**사용 사례**:
- 6개 단계 표현
- 상세 복합 프로세스
- 6단 흐름
- 복잡한 워크플로우
- 확장된 프로세스

**keywords**: 6단계 프로세스, 복합 프로세스, 다단계 흐름, 상세 단계, 확장 프로세스

**expected_prompt**: "6개 단계를 순차적으로 표현하는 복합 프로세스"

---

## 기술 사양

### YAML 템플릿 구조
모든 YAML 파일은 다음 구조를 포함합니다:

```yaml
content_template:
  id: {template_id}
  name: {한글_이름}
  version: "2.0"
  source: {PPTX_경로}
  source_slide_index: {슬라이드_번호}

design_meta:
  quality_score: 8.5
  design_intent: {design_intent}
  visual_balance: symmetric|asymmetric
  information_density: low|medium|high

canvas:
  reference_width: 1920
  reference_height: 1080
  aspect_ratio: "16:9"

shapes: [{모든_도형_데이터}]

use_for: [{사용_사례_목록}]
keywords: [{키워드_목록}]

expected_prompt: {프롬프트_설명}
prompt_keywords: [{프롬프트_키워드}]

thumbnail: {썸네일_경로}
```

### 도형 정보
각 도형은 다음을 포함합니다:
- **geometry**: x, y, cx, cy (% 단위), rotation, original_aspect_ratio
- **style**: fill (색상, 불투명도), stroke (색상, 너비), shadow, rounded_corners
- **text**: has_text, alignment, font_size (ratio & pt), font_weight

### 색상 매핑
다음 시맨틱 색상을 사용합니다:
- `primary`: 기본 색상
- `secondary`: 보조 색상
- `accent`: 강조 색상
- `background`: 배경색
- `dark_text`: 어두운 텍스트
- `gray`: 회색

---

## 파일 위치

### YAML 템플릿 파일

```
/home/jji/project/docs/templates/contents/templates/
├── grid/
│   └── basic-grid-3col1.yaml
├── timeline/
│   ├── basic-timeline-circular1.yaml
│   ├── basic-timeline-milestone1.yaml
│   ├── basic-timeline-arrow1.yaml
│   └── basic-timeline-progress1.yaml
├── process/
│   ├── basic-process-5step1.yaml
│   ├── basic-process-chevron1.yaml
│   ├── basic-process-3step1.yaml
│   └── basic-process-6step1.yaml
└── roadmap/
    └── basic-roadmap-yearly1.yaml
```

### 썸네일 파일

```
/home/jji/project/docs/templates/contents/thumbnails/
├── basic-grid-3col1.png
├── basic-timeline-circular1.png
├── basic-timeline-milestone1.png
├── basic-timeline-arrow1.png
├── basic-timeline-progress1.png
├── basic-process-5step1.png
├── basic-process-chevron1.png
├── basic-process-3step1.png
├── basic-process-6step1.png
└── basic-roadmap-yearly1.png
```

---

## 추출 프로세스

### 1단계: XML 분석
- PowerPoint의 언팩된 slide{50-59}.xml 파일 분석
- <p:sp> (도형), <p:cxnSp> (선) 요소 추출

### 2단계: Zone 필터링
- 타이틀/푸터 영역 동적 감지
- Content Zone 내 도형만 추출
- 필터링 기준:
  - 타이틀: placeholder type이 'title' 또는 상단 20% 이내 & 높이 15% 미만
  - 푸터: placeholder type이 'sldNum', 'ftr' 또는 하단 10% 이내

### 3단계: 좌표 변환
- EMU (English Metric Units) → 픽셀 → % 변환
- 기준:
  - SLIDE_WIDTH_EMU: 12,192,000 (1920px)
  - SLIDE_HEIGHT_EMU: 6,858,000 (1080px)
  - CONTENT_WIDTH: 1,920 × 0.94 = 1,804.8px
  - CONTENT_HEIGHT: 1,080 × 0.75 = 810px

### 4단계: 도형 분류
- type 결정 (rectangle, oval, line, textbox 등)
- fill/stroke 정보 추출
- 텍스트 정보 추출 (content, alignment, font_size)
- 원본 aspect ratio 계산

### 5단계: YAML 생성
- design_intent 기반 메타데이터 생성
- use_for, keywords, expected_prompt 작성
- shape_sources 타입 지정 (ooxml)

### 6단계: 썸네일 생성
- LibreOffice를 통해 PPTX → PDF → PNG 변환
- 해상도: 198 DPI
- 파일명: {template_id}.png

---

## 검증 결과

- YAML 구문 검증: PASS
- 도형 좌표 범위: 0-100% (정상)
- 텍스트 정보: 모두 포함
- 원본 비율 계산: 모두 완료
- 폰트 크기: pt 단위로 저장
- 썸네일 생성: 모두 성공
- 파일 인코딩: UTF-8

---

## 활용 안내

### 템플릿 매칭
PPT 생성 시 이 템플릿들을 다음과 같이 활용할 수 있습니다:

1. **콘텐츠 기반 자동 선택**
   - use_for 항목과 사용자 요구사항 비교
   - expected_prompt 기반 세마틱 매칭

2. **디자인 패턴 재사용**
   - shapes 배열의 구조를 참고하여 새 슬라이드 생성
   - geometry와 style을 템플릿으로 활용

3. **썸네일 기반 선택**
   - 사용자에게 시각적 프리뷰 제공
   - 타의 추니 없이 선택 가능

### 커스터마이제이션
추출된 템플릿 기반으로:
- 텍스트 교체 가능
- 색상 수정 가능
- 도형 크기 조정 가능
- 새로운 도형 추가 가능

---

## 결론

슬라이드 50-59에서 총 253개의 도형을 포함한 10개의 고품질 콘텐츠 템플릿을 성공적으로 추출했습니다. 
모든 템플릿은 완전한 메타데이터, 기하학 정보, 스타일 정보를 포함하고 있으며, 
시맨틱 색상 매핑과 원본 비율 정보로 향후 재사용성을 극대화합니다.

