# 전문가 수준 PPT 자동 생성 서비스 - 연구 보고서 및 아키텍처 설계

**작성일**: 2026-01-06
**목적**: project-plan.md와 같은 문서를 입력받아 전문가가 디자인한 것처럼 보이는 PPT를 자동 생성하는 서비스 아키텍처 설계

---

## 연구 개요

**연구 범위**:
- Beautiful.ai, Gamma.app, Tome.app 등 상용 서비스 분석
- 학술 연구 (PPTAgent, SlideTailor, Auto-Slides, DocPres)
- PPT 생성 도구/라이브러리
- 템플릿 데이터베이스화 방법

---

## 1. 상용 서비스 분석

### 1.1 Beautiful.ai

**핵심 기술: DesignerBot + Smart Slides**

| 구성요소 | 기능 |
|---------|------|
| **DesignerBot** | OpenAI 기반 생성형 AI, DALL-E 이미지 생성 통합 |
| **Smart Slides** | 실시간 자동 정렬/크기조정/리포맷, 디자인 가드레일 |
| **Brand Kit** | 로고, 컬러, 폰트, 레이아웃 중앙 관리 |

**디자인 원칙 (Dieter Rams 10원칙 기반)**:
- Typography: Post Grotesk 폰트 패밀리, 명확한 계층 구조
- Color: RGB 3원색 기반 현대적 재해석, 감정 심리학 적용
- Layout: 미니멀리즘, 충분한 여백, 자동 정렬

**콘텐츠-디자인 매핑**:
- 멀티모달 입력 (텍스트, 문서, URL)
- 콘텐츠 타입별 자동 템플릿 선택
- 콘텐츠 계층 → 시각적 계층 매핑

### 1.2 Gamma.app

**핵심 특징: 20+ AI 모델 동시 운영**

- 일일 100만+ AI 생성 프레젠테이션
- 일일 600만 AI 이미지 생성
- 이미지 생성 모델 선택 가능 (Flux, Imagen, GPT Image, Recraft v3, Ideogram 3.0)

**기술 스택**:
- Full TypeScript
- AIJSX (자체 AI 프롬프팅 프레임워크)
- Vercel AI SDK
- 카드 기반 반응형 레이아웃

**Smart Layouts**: 콘텐츠 타입에 따른 전문 포맷 자동 선택, 원클릭 컬럼 조정

### 1.3 Tome.app

**핵심 철학: 스토리텔링 우선 + 유연성**

**타일 기반 아키텍처**:
- 전통적 슬라이드 대신 반응형 타일 시스템
- 다중 디바이스 호환 (반응형 디자인)
- 리치 미디어 지원 (비디오, GIF, Figma/Miro 임베드)

**AI 레이아웃 가이드 전략**:
> "비결정론적 시스템 설계 시, 볼링 레인에 범퍼를 추가하듯 가드레일과 지침을 제공해야 한다"

- 레이아웃 타입별 목적 학습
- 유연성 허용하되 품질 보장하는 제약 조건

---

## 2. 학술 연구 기반 파이프라인 분석

### 2.1 PPTAgent (EMNLP 2025, ICIP-CAS)

**혁신**: 편집 기반 2단계 접근법

```
Stage I: Presentation Analysis
├── 레퍼런스 PPT 분석
├── 슬라이드 클러스터링 (ViT 임베딩)
└── 콘텐츠 스키마 추출

Stage II: Presentation Generation
├── 아웃라인 생성 (CoT 프롬프팅)
├── 레퍼런스 슬라이드 선택
└── 반복적 편집 API 호출
```

**핵심 API**:
- `del_span()`, `del_image()` - 요소 삭제
- `clone_paragraph()` - 단락 복제
- `replace_span()`, `replace_image()` - 콘텐츠 교체

**평가 프레임워크 PPTEval**:
| 차원 | 평가 항목 |
|-----|---------|
| Content | 텍스트 간결성, 문법, 이미지 관련성, 정확성 |
| Design | 색상 조화, 레이아웃 가독성, 시각적 계층, 요소 간격 |
| Coherence | 논리적 구조, 점진적 발전, 내러티브 흐름 |

### 2.2 SlideTailor (AAAI 2026, NUS-NLP)

**혁신**: 암묵적 선호도 학습

```
Stage 1: Implicit Preference Distillation
├── 예시 논문-슬라이드 쌍에서 선호도 추출
├── 템플릿 PPT 파일 분석
└── 구조화된 콘텐츠/미적 선호도 프로파일 생성

Stage 2: Preference-Guided Slide Planning
├── "Chain-of-Speech" 메커니즘 (시각+구두 발표 정렬)
└── 사용자 선호도에 따른 콘텐츠 재구성

Stage 3: Slide Realization
├── 템플릿 레이아웃에 의미론적 매칭
├── 레이아웃 인식 코드 생성
└── 편집 가능성 유지하며 템플릿 미학 보존
```

### 2.3 Auto-Slides (Westlake University + UC Merced)

**6-에이전트 파이프라인**:

```
1. PDF Parser → marker-pdf + OCR로 콘텐츠 추출
2. Presentation Planner → 교육학적 최적화 구조 생성
3. Verification Agent → 콘텐츠 커버리지 검증
4. Repair Agent → 이슈 자동 수정
5. TEX Generator → LaTeX Beamer 코드 생성
6. Interactive Editor → 자연어 대화 기반 수정
```

### 2.4 DocPres (Adobe, 2024)

**5단계 분해 전략** (긴 문서 처리):

1. **Hierarchical Document Overview**: 서브섹션 → 섹션 → 전체 문서 재귀적 요약
2. **Outline Generation**: K개 슬라이드 제목 생성 (CoT)
3. **Slide-to-Section Mapping**: 편집 거리 매칭 (>90% 임계값)
4. **Slide Content Generation**: 제목 + 섹션 텍스트 + 이전 슬라이드 컨텍스트
5. **Image Selection**: CLIP 임베딩으로 이미지 랭킹 (>80% 코사인 유사도)

---

## 3. 전문가 디자인 원칙의 코드화

### 3.1 그리드 시스템

**12-컬럼 그리드** (2, 3, 4, 6으로 균등 분할 가능):
- 시각적 리듬과 반복
- 일관된 정렬과 간격
- 조화롭고 세련된 디자인

**그리드 타입**:
| 타입 | 용도 |
|-----|-----|
| Manuscript Grid | 텍스트 중심 슬라이드 |
| Column Grid | 콘텐츠 섹션 구분 |
| Modular Grid | 데이터/차트 슬라이드 |
| Hierarchical Grid | 중요도 기반 배치 |

### 3.2 타이포그래피 계층

```
H1 (제목): 48px, Bold
H2 (부제목): 36px, Semi-bold
H3 (섹션): 28px, Medium
Body: 18-24px, Regular
Caption: 14px, Light

Line Height: 1.125-1.200x 폰트 크기
폰트 수 제한: 최대 2-3개
```

### 3.3 컬러 시스템

**60-30-10 규칙**:
- 60% 기본색 (배경, 주요 영역)
- 30% 보조색 (지원 요소)
- 10% 강조색 (CTA, 하이라이트)

**컬러 심리학**:
| 색상 | 연상 |
|-----|-----|
| Blue | 신뢰, 전문성, 의존성 |
| Red | 흥분, 긴급성 |
| Green | 성장, 안정, 자연 |
| Orange/Yellow | 에너지, 낙관 |

**접근성**: WCAG AA 최소 4.5:1 대비율

### 3.4 시각적 계층

**기법**:
1. **Size**: 큰 요소가 시선 집중
2. **Contrast**: 요소 간 명확한 차이
3. **Position**: 좌상단/중앙이 높은 우선순위
4. **Color**: 제목은 강렬, 보조는 뮤트
5. **Weight**: 폰트 굵기 차이
6. **Spacing**: 관계없는 요소는 멀리 배치

**읽기 패턴**:
- F-Pattern: 뉴스, 문서 (좌상→우→좌하)
- Z-Pattern: 마케팅, 미니멀 (대각선)

### 3.5 디자인 토큰 시스템

```javascript
// 토큰 명명 규칙 (BEM 스타일)
token.category.property.state

// 예시
color.primary.base        // #0066CC
color.text.subtle         // #666666
spacing.margin.large      // 32px
typography.heading.h1     // { size: 48px, weight: 700 }
```

**이점**:
- 디자인-코드 간 소통 표준화
- 일괄 변경 가능 (상속)
- 버전 관리 및 추적
- 하드코딩 제거

---

## 4. 기술 스택 및 도구

### 4.1 PPT 생성 라이브러리

| 라이브러리 | 언어 | 특징 | 추천 용도 |
|-----------|-----|------|----------|
| **python-pptx** | Python | 가장 포괄적, 라운드트립 지원 | 서버사이드 생성 |
| **PptxGenJS** | JS | 브라우저/Node.js, 제로 의존성 | 웹앱, 리액트 |
| **Slidev** | Vue.js | 마크다운 기반, 인터랙티브 | 개발자 발표 |
| **Marp** | Markdown | 단순, CSS 테마 | 빠른 생성 |

### 4.2 python-pptx 핵심 API

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# 프레젠테이션 생성
prs = Presentation()

# 슬라이드 추가
slide_layout = prs.slide_layouts[1]  # Title and Content
slide = prs.slides.add_slide(slide_layout)

# 텍스트 스타일링
title = slide.shapes.title
title.text = "슬라이드 제목"
title.text_frame.paragraphs[0].font.size = Pt(44)
title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 102, 204)

# 저장
prs.save('output.pptx')
```

### 4.3 PptxGenJS 핵심 패턴

```javascript
import pptxgen from "pptxgenjs";

// 마스터 슬라이드 정의 (브랜드 일관성)
pres.defineSlideMaster({
  title: "CORPORATE_BRAND",
  background: { color: "001F3F" },
  objects: [
    { image: { x: 11.3, y: 6.4, w: 1.67, h: 0.75, path: "logo.png" } },
    { text: { text: "회사명", options: { x: 0.5, y: 6.5 } } }
  ]
});

// 마스터 적용
let slide = pres.addSlide({ masterName: "CORPORATE_BRAND" });
```

### 4.4 OOXML (Office Open XML) 구조

```
presentation.pptx (ZIP)
├── ppt/
│   ├── presentation.xml      # 루트 프레젠테이션
│   ├── slides/
│   │   ├── slide1.xml        # 슬라이드 콘텐츠
│   │   └── _rels/            # 관계 정의
│   ├── slideMasters/         # 마스터 슬라이드
│   ├── slideLayouts/         # 레이아웃 템플릿
│   ├── theme/theme1.xml      # 테마 (색상, 폰트)
│   └── media/                # 이미지, 비디오
├── docProps/                 # 메타데이터
└── [Content_Types].xml       # MIME 타입
```

---

## 5. 기존 PPT 데이터베이스화 방법

### 5.1 PPT 파일 파싱 및 분석

**추출 대상 요소**:

| 카테고리 | 추출 항목 |
|---------|---------|
| **구조** | 슬라이드 수, 레이아웃 타입, 마스터 참조 |
| **텍스트** | 폰트 패밀리/크기/색상, 정렬, 계층 |
| **컬러** | 팔레트 (기본/보조/강조), RGB/HSL 값 |
| **레이아웃** | 그리드 패턴, 마진/패딩, 요소 위치 |
| **이미지** | 파일명, 크기, 위치, 압축 방식 |
| **애니메이션** | 트랜지션, 타이밍, 트리거 |

### 5.2 디자인 패턴 추출 파이프라인

```
[PPTX 파일]
     ↓
[Layer 1: 파싱]
├── python-pptx로 구조 추출
├── XML 직접 파싱 (고급 속성)
└── 이미지/미디어 추출
     ↓
[Layer 2: 특징 추출]
├── 컬러 팔레트 추출 (K-means 클러스터링)
├── 타이포그래피 분석
├── 레이아웃 패턴 인식 (DLA 모델)
└── 디자인 요소 분류
     ↓
[Layer 3: 인코딩]
├── 벡터 임베딩 생성 (Vision Transformer)
├── 컬러 공간 변환 (RGB → Lab)
├── 유사도 메트릭 계산
└── 벡터 DB 인덱싱
     ↓
[Layer 4: 저장]
├── 관계형 DB (메타데이터, 스타 스키마)
├── 벡터 DB (임베딩, 유사도 검색)
└── 자산 스토리지 (이미지, 바이너리)
```

### 5.3 컬러 팔레트 추출 알고리즘

**K-Means 클러스터링** (가장 일반적):
```python
from sklearn.cluster import KMeans
import numpy as np

def extract_palette(image, n_colors=5):
    # 이미지를 RGB 픽셀 배열로 변환
    pixels = image.reshape(-1, 3)

    # K-means 클러스터링
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    # 중심점 = 대표 색상
    palette = kmeans.cluster_centers_.astype(int)
    return palette
```

**Lab 색공간 권장**: 인간 지각에 균일 (Delta E 2000 기준)

### 5.4 레이아웃 분석 모델

**최신 학술 연구 (2024-2025)**:

| 모델 | 특징 | 성능 |
|-----|-----|-----|
| **DLAFormer** | E2E Transformer, 레이아웃 계층 탐지 | 97%+ 정확도 |
| **DocLayout-YOLO** | 속도-정확도 균형 | 8-14ms/페이지 |
| **LayoutLLM** | LLM 기반 레이아웃 이해 | 다양한 문서 타입 |
| **PP-DocLayout** | 통합 레이아웃 탐지 | GPU 8.1ms, CPU 14.5ms |

### 5.5 템플릿 데이터베이스 스키마

```yaml
Template:
  identity:
    template_id: UUID
    name: string
    category: string  # corporate, academic, creative
    subcategory: string
    version: string

  design_properties:
    color_palette:
      primary: "#0066CC"
      secondary: "#333333"
      accent: "#FF6600"
    typography:
      heading_font: "Pretendard"
      body_font: "Noto Sans KR"
      scale: [48, 36, 24, 18, 14]
    spacing:
      base_unit: 8  # px
      margins: [40, 40, 40, 40]

  layout_elements:
    layouts: [title, content, two_column, image_left, data]
    grid_system: 12-column
    aspect_ratio: "16:9"

  quality_metrics:
    color_harmony_score: 0.85
    typography_consistency: 0.92
    accessibility_level: "WCAG AA"
    visual_balance_score: 0.88

  relationships:
    theme_id: ref(Theme)
    parent_template_id: ref(Template)  # 상속
    derived_templates: [ref(Template)]
```

### 5.6 유사도 검색 시스템

**벡터 임베딩 접근법**:
1. 템플릿/슬라이드 이미지 → CNN/ViT로 벡터 변환
2. 색상, 형태, 텍스처, 레이아웃 특징 추출
3. 벡터 DB 인덱싱 (Weaviate, Milvus, Pinecone)
4. 거리 메트릭으로 유사도 쿼리

**거리 메트릭**:
- **Cosine Similarity**: 방향 정렬 (문서/디자인 유사도에 최적)
- **Euclidean Distance**: 픽셀 레벨 비교
- **Dot Product**: 고차원 벡터 빠른 근사

**클러스터링**:
- **K-means**: 중심 기반 파티션 (컬러 팔레트용)
- **Hierarchical**: 덴드로그램 시각화
- **DBSCAN**: 밀도 기반, 이상치 탐지

---

## 6. 권장 아키텍처

### 6.1 시스템 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  [문서 입력]        [템플릿 선택]        [브랜드 가이드]         │
│  - Markdown         - 기존 PPT           - 로고, 컬러            │
│  - Word/PDF         - 템플릿 DB          - 폰트, 스타일          │
│  - 텍스트 프롬프트   - AI 추천                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   PARSER     │ →  │   PLANNER    │ →  │  GENERATOR   │       │
│  │              │    │              │    │              │       │
│  │ - 문서 파싱   │    │ - 아웃라인    │    │ - 콘텐츠 생성 │       │
│  │ - 구조 추출   │    │ - 슬라이드수  │    │ - 레이아웃   │       │
│  │ - 이미지 추출 │    │ - 흐름 설계   │    │ - 스타일링   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                   │
│                              ↓                                    │
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  VALIDATOR   │ →  │   REFINER    │ →  │  RENDERER    │       │
│  │              │    │              │    │              │       │
│  │ - 품질 검증   │    │ - 피드백 반영 │    │ - PPTX 생성  │       │
│  │ - 디자인 체크 │    │ - 수정 적용   │    │ - PDF 변환   │       │
│  │ - 접근성     │    │ - 최적화     │    │ - 미리보기   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       SUPPORT SYSTEMS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  TEMPLATE DB    │  │  DESIGN ENGINE  │  │  ASSET MANAGER  │  │
│  │                 │  │                 │  │                 │  │
│  │ - 템플릿 저장    │  │ - 디자인 토큰   │  │ - 이미지 라이브러리│ │
│  │ - 유사도 검색    │  │ - 그리드 시스템  │  │ - 아이콘 세트    │  │
│  │ - 클러스터링     │  │ - 타이포그래피  │  │ - AI 이미지 생성 │  │
│  │ - 벡터 임베딩    │  │ - 컬러 팔레트   │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 상세 파이프라인

#### Stage 1: Document Parsing

```python
class DocumentParser:
    def parse(self, input_doc):
        """
        입력 문서를 구조화된 콘텐츠로 변환

        Returns:
            {
                "title": "프로젝트 수행계획서",
                "sections": [
                    {
                        "heading": "1. 프로젝트 개요",
                        "level": 1,
                        "content": [...],
                        "subsections": [...]
                    }
                ],
                "tables": [...],
                "images": [...],
                "metadata": {...}
            }
        """
```

#### Stage 2: Presentation Planning (LLM)

```python
PLANNING_PROMPT = """
문서를 분석하여 프레젠테이션 아웃라인을 생성하세요.

규칙:
1. 슬라이드당 최대 5개 불릿 포인트
2. 불릿당 최대 10단어
3. 논리적 흐름 유지 (도입 → 본론 → 결론)
4. 데이터/차트가 있으면 별도 슬라이드

출력 형식 (JSON):
{
    "slides": [
        {
            "type": "title" | "content" | "two_column" | "data" | "image",
            "title": "슬라이드 제목",
            "content": [...],
            "layout_hint": "template_id 또는 레이아웃 타입",
            "visual_elements": ["chart", "image", "icon"]
        }
    ]
}
"""
```

#### Stage 3: Design System Application

```python
class DesignSystem:
    def __init__(self, brand_config):
        self.tokens = {
            "colors": {
                "primary": brand_config.primary_color,
                "secondary": brand_config.secondary_color,
                "accent": brand_config.accent_color,
                "text": {"dark": "#333333", "light": "#FFFFFF"}
            },
            "typography": {
                "heading": {"font": "Pretendard", "weights": [700, 600]},
                "body": {"font": "Noto Sans KR", "weights": [400, 500]}
            },
            "spacing": {
                "base": 8,  # px
                "scale": [0.5, 1, 1.5, 2, 3, 4, 6, 8]  # base 배수
            }
        }

    def apply_to_slide(self, slide, layout_type):
        """슬라이드에 디자인 시스템 적용"""
```

#### Stage 4: PPTX Generation

```python
class PPTXGenerator:
    def generate(self, slide_specs, design_system):
        prs = Presentation()

        for spec in slide_specs:
            # 레이아웃 선택
            layout = self.select_layout(spec["type"])
            slide = prs.slides.add_slide(layout)

            # 콘텐츠 배치
            self.place_content(slide, spec["content"], design_system)

            # 스타일 적용
            self.apply_styling(slide, design_system)

        return prs
```

#### Stage 5: Quality Validation (PPTEval 기반)

```python
class QualityValidator:
    def evaluate(self, presentation):
        scores = {
            "content": self.eval_content(presentation),
            "design": self.eval_design(presentation),
            "coherence": self.eval_coherence(presentation)
        }

        # 임계값 미달 시 피드백 생성
        if min(scores.values()) < 3.0:
            return self.generate_improvement_suggestions(scores)

        return {"status": "pass", "scores": scores}
```

### 6.3 기술 스택 권장

| 영역 | 기술 | 이유 |
|-----|-----|-----|
| **PPTX 생성** | python-pptx | 가장 포괄적, Python 에코시스템 |
| **LLM** | GPT-4o / Claude 3.5 | 최고 품질 콘텐츠 생성 |
| **레이아웃 분석** | DocLayout-YOLO | 속도/정확도 균형 |
| **벡터 임베딩** | Vision Transformer (ViT) | 문서 이해에 최적 |
| **벡터 DB** | Weaviate / Milvus | 오픈소스, 확장성 |
| **관계형 DB** | PostgreSQL + jsonb | 유연한 스키마 |
| **이미지 생성** | DALL-E 3 / Midjourney | 고품질 비주얼 |
| **API** | FastAPI | Python 네이티브, ML 파이프라인 |

---

## 7. 구현 로드맵

### Phase 1: 기초 인프라 (MVP)
- [ ] 문서 파싱 모듈 (Markdown → 구조화 데이터)
- [ ] python-pptx 기반 기본 생성기
- [ ] 단순 템플릿 시스템 (5개 레이아웃)
- [ ] LLM 아웃라인 생성

### Phase 2: 디자인 시스템
- [ ] 디자인 토큰 시스템 구축
- [ ] 그리드 기반 레이아웃 엔진
- [ ] 타이포그래피 자동 계층화
- [ ] 컬러 팔레트 자동 생성

### Phase 3: 템플릿 데이터베이스
- [ ] PPT 파싱 및 특징 추출
- [ ] 벡터 임베딩 생성
- [ ] 유사도 검색 시스템
- [ ] 템플릿 추천 엔진

### Phase 4: 고급 기능
- [ ] AI 이미지 생성 통합
- [ ] 실시간 프리뷰
- [ ] 협업 편집
- [ ] 브랜드 키트 관리

### Phase 5: 품질 최적화
- [ ] PPTEval 기반 자동 평가
- [ ] 피드백 루프 통합
- [ ] A/B 테스트 시스템
- [ ] 사용자 선호도 학습

---

## 8. 핵심 인사이트 및 권장사항

### 8.1 성공 요인

1. **템플릿 기반 생성이 End-to-End보다 우수**
   - 시각적 일관성 보장
   - 더 빠른 생성
   - LLM 환각 감소

2. **다단계 분해가 단일 프롬프트보다 효과적**
   - 긴 문서 컨텍스트 관리
   - 각 단계 특화 최적화
   - 오류 복구 용이

3. **암묵적 선호도 학습 (SlideTailor)**
   - 명시적 지시보다 예시 기반 학습
   - 사용자 노력 감소
   - 출력 일관성 향상

4. **디자인 가드레일 필수**
   - AI의 비결정론적 특성 제어
   - 품질 하한선 보장
   - 전문가 수준 유지

### 8.2 주의사항

- PPT의 OOXML 형식은 복잡하고 중복적 → 라이브러리 활용 필수
- LLM은 공간적 레이아웃 이해에 한계 → VLM 보조 또는 템플릿 기반
- 자동 생성은 "초안" 수준 → 인간 검토/수정 루프 필요
- 접근성 (WCAG) 준수 자동 검증 포함 권장

---

## 9. 구현 계획 (Claude Code 도구/Skills)

### 9.1 확정된 요구사항

| 항목 | 결정 |
|-----|-----|
| **기술 스택** | Python + python-pptx |
| **템플릿 DB 수준** | Level 2: 디자인 패턴 분석 (벡터 임베딩, 유사도 검색) |
| **타겟 사용자** | 기업/비즈니스 (제안서, 보고서, 사업계획서) |
| **AI 통합** | 콘텐츠 추출은 별도, PPT 생성에 집중 |
| **구현 형태** | Claude Code Skills + 도구 |

### 9.2 개발할 Claude Code Skills

#### Skill 1: `/pptx` - PPT 생성 메인 스킬

```yaml
name: pptx
description: |
  구조화된 콘텐츠를 전문가 수준의 PPT로 변환.
  디자인 시스템 적용, 템플릿 매칭, PPTX 파일 생성.

workflow:
  1. 입력 콘텐츠 분석 (JSON/Markdown 구조)
  2. 템플릿 DB에서 유사 디자인 검색
  3. 디자인 토큰 적용
  4. python-pptx로 PPTX 생성
  5. 품질 검증 및 출력
```

#### Skill 2: `/ppt-template-analyze` - 템플릿 분석 스킬

```yaml
name: ppt-template-analyze
description: |
  기존 PPT 파일을 분석하여 디자인 패턴 추출.
  컬러, 폰트, 레이아웃, 스타일을 데이터베이스화.

workflow:
  1. PPTX 파일 파싱 (python-pptx)
  2. 디자인 요소 추출 (컬러, 폰트, 레이아웃)
  3. 슬라이드 이미지 캡처 및 벡터화
  4. 메타데이터 JSON 저장
  5. 벡터 DB 인덱싱
```

#### Skill 3: `/ppt-design-system` - 디자인 시스템 관리

```yaml
name: ppt-design-system
description: |
  브랜드 디자인 시스템 생성 및 관리.
  컬러 팔레트, 타이포그래피, 스페이싱 규칙 정의.

features:
  - 브랜드 가이드라인에서 토큰 자동 생성
  - 기존 PPT에서 디자인 시스템 추출
  - 디자인 토큰 JSON 내보내기
```

### 9.3 핵심 모듈 구조

```
workspace/
├── pptx_generator/
│   ├── __init__.py
│   ├── core/
│   │   ├── generator.py        # PPTX 생성 엔진
│   │   ├── design_system.py    # 디자인 토큰 시스템
│   │   └── layout_engine.py    # 레이아웃 배치 엔진
│   ├── parsers/
│   │   ├── pptx_parser.py      # 기존 PPT 분석
│   │   └── content_parser.py   # 입력 콘텐츠 파싱
│   ├── templates/
│   │   ├── template_db.py      # 템플릿 데이터베이스
│   │   ├── similarity.py       # 유사도 검색
│   │   └── embeddings.py       # 벡터 임베딩
│   └── utils/
│       ├── colors.py           # 컬러 유틸리티
│       ├── typography.py       # 타이포그래피
│       └── validators.py       # 품질 검증
├── data/
│   ├── templates/              # 템플릿 PPT 파일
│   ├── embeddings/             # 벡터 임베딩 저장
│   └── design_systems/         # 디자인 시스템 JSON
└── skills/
    ├── pptx.md                 # 메인 스킬
    ├── ppt-template-analyze.md # 분석 스킬
    └── ppt-design-system.md    # 디자인 시스템 스킬
```

### 9.4 핵심 코드 설계

#### Generator Core (generator.py)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from typing import List, Dict, Any

class PPTXGenerator:
    def __init__(self, design_system: Dict):
        self.design_system = design_system
        self.prs = Presentation()

    def generate(self, slides_spec: List[Dict]) -> Presentation:
        """
        슬라이드 스펙을 받아 PPTX 생성

        Args:
            slides_spec: [
                {
                    "type": "title",
                    "title": "프로젝트 수행계획서",
                    "subtitle": "스마트 물류관리 시스템"
                },
                {
                    "type": "content",
                    "title": "프로젝트 개요",
                    "bullets": ["항목1", "항목2", "항목3"]
                }
            ]
        """
        for spec in slides_spec:
            slide = self._create_slide(spec)
            self._apply_design_system(slide)

        return self.prs

    def _create_slide(self, spec: Dict) -> Any:
        layout_map = {
            "title": 0,      # Title Slide
            "content": 1,    # Title and Content
            "two_column": 3, # Two Content
            "blank": 6       # Blank
        }
        layout = self.prs.slide_layouts[layout_map.get(spec["type"], 1)]
        slide = self.prs.slides.add_slide(layout)
        self._populate_content(slide, spec)
        return slide

    def _apply_design_system(self, slide):
        """디자인 토큰을 슬라이드에 적용"""
        tokens = self.design_system["tokens"]
        # 컬러, 폰트, 스페이싱 적용
        ...
```

#### Template Analyzer (pptx_parser.py)

```python
from pptx import Presentation
from pptx.util import Pt
from collections import defaultdict
import json

class PPTXAnalyzer:
    def analyze(self, pptx_path: str) -> Dict:
        """
        PPT 파일을 분석하여 디자인 패턴 추출

        Returns:
            {
                "metadata": {...},
                "color_palette": ["#0066CC", "#333333", ...],
                "typography": {
                    "heading": {"font": "...", "size": 44},
                    "body": {"font": "...", "size": 18}
                },
                "layouts": [...],
                "slides_summary": [...]
            }
        """
        prs = Presentation(pptx_path)
        return {
            "metadata": self._extract_metadata(prs),
            "color_palette": self._extract_colors(prs),
            "typography": self._extract_typography(prs),
            "layouts": self._analyze_layouts(prs),
            "slides_summary": self._summarize_slides(prs)
        }

    def _extract_colors(self, prs) -> List[str]:
        """모든 슬라이드에서 사용된 컬러 추출"""
        colors = set()
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "fill") and shape.fill.type:
                    # 컬러 추출 로직
                    ...
        return list(colors)
```

#### Similarity Search (similarity.py)

```python
import numpy as np
from typing import List, Dict, Tuple

class TemplateSimilarity:
    def __init__(self, embeddings_path: str):
        self.embeddings = self._load_embeddings(embeddings_path)

    def find_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        쿼리 임베딩과 가장 유사한 템플릿 찾기

        Returns:
            [(template_id, similarity_score), ...]
        """
        similarities = []
        for template_id, embedding in self.embeddings.items():
            score = self._cosine_similarity(query_embedding, embedding)
            similarities.append((template_id, score))

        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

### 9.5 구현 우선순위

| 우선순위 | 모듈 | 설명 |
|---------|-----|-----|
| **P0** | generator.py | 기본 PPTX 생성 엔진 |
| **P0** | design_system.py | 디자인 토큰 시스템 |
| **P1** | pptx_parser.py | 기존 PPT 분석 |
| **P1** | layout_engine.py | 레이아웃 배치 |
| **P2** | embeddings.py | 벡터 임베딩 생성 |
| **P2** | similarity.py | 유사도 검색 |
| **P3** | validators.py | 품질 검증 (PPTEval) |

---

## 참고 자료

### 상용 서비스
- Beautiful.ai: https://www.beautiful.ai
- Gamma.app: https://gamma.app
- Tome.app: https://tome.app

### 학술 연구
- PPTAgent (EMNLP 2025): https://arxiv.org/abs/2501.03936
- SlideTailor (AAAI 2026): https://arxiv.org/abs/2512.20292
- Auto-Slides: https://auto-slides.github.io
- DocPres (Adobe): https://arxiv.org/abs/2406.06556

### 기술 문서
- python-pptx: https://python-pptx.readthedocs.io
- PptxGenJS: https://gitbrent.github.io/PptxGenJS
- Office Open XML: https://learn.microsoft.com/en-us/office/open-xml
