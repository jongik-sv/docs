# Professional AI PPT Generation Service: Architecture & Methodology

## 1. Executive Summary

본 문서는 `project-plan.md`와 같은 텍스트 입력을 전문가 수준의 디자인을 갖춘 PPT로 변환하기 위한 서비스 아키텍처와 방법론을 제안합니다. 단순히 슬라이드를 생성하는 것을 넘어, **"Senior Product Designer"**의 미학(Apple, Stripe 스타일)을 시스템적으로 구현하는 데 초점을 맞춥니다.

---

## 2. 벤치마킹 분석 (Beautiful.ai & Skywork)

### Beautiful.ai: Design-First & Smart Slides

- **방법론**: 사용자가 콘텐츠를 입력하면 레이아웃이 실시간으로 적응하는 "Smart Slides" 기술 사용.
- **핵심 아키텍처**: 디자인 규칙(여백, 정렬, 폰트 스케일)이 코드화되어 있어 사용자의 조작 실수를 원천 차단.
- **교훈**: 자유로운 배치를 허용하기보다, 검증된 디자인 템플릿에 콘텐츠를 매핑하는 방식이 전문가 수준의 결과물을 보장함.

### Skywork AI: Research-First & AI Agents

- **방법론**: 단순 요약이 아닌 심층 연구를 통해 내러티브(Storytelling)를 구성하고, 브랜드 가이드라인을 자동 적용.
- **핵심 아키텍처**: 멀티 에이전트 시스템이 컨셉 도출, 구조 설계, 디자인 적용을 단계별로 수행.
- **교훈**: PPT는 시각적 결과물 이전에 논리적 구조(Information Architecture)가 탄탄해야 하며, 이를 위해 AI 에이전트의 역할 분담이 중요함.

---

## 3. 제안 아키텍처: 4-Layer Presentation Engine

전문가급 디자인을 위해 시스템을 4개의 계층으로 분리하여 관리합니다.

### Layer 1: Design System (감성 엔진)

- **Style Tokens**: 색상(Primary, Secondary, Accent), 타이포그래피(폰트 스케일, 자간, 행간), 그림자(Shadow), 둥글기(Radius) 정의.
- **Designer Persona**: "Senior Product Designer" 페르소나를 주입하여 충분한 여백(Whitespace)과 미니멀한 색상 배합을 강제함.

### Layer 2: Component Library (시각 빌딩 블록)

- **Custom Shapes**: 기본 플레이스홀더 대신 `python-pptx`를 이용해 Rounded Rectangle, Chevron, Grid Card 등을 직접 드로잉.
- **Interactive Logic**: 콘텐츠의 양에 따라 폰트 크기와 카드 개수가 자동 조절되는 논리 포함.

### Layer 3: Structured Data Interface (DSL)

- **JSON Source of Truth**: 마크다운을 직접 PPT로 변환하지 않고, 중간 단계인 구조화된 JSON(DSL)으로 변환.
- **Intent Mapping**: 슬라이드 내용을 분석하여 '비교', '프로세스', '갤러리' 등 최적의 레이아웃 ID에 매핑.

### Layer 4: Asset Generation Pipeline

- **AI Visuals**: Gemini 혹은 전문 이미지 생성 모델을 연동하여 히어로 이미지와 커스텀 아이콘 생성.
- **SVG Capture**: 브라우저 기반 렌더링을 통해 고해상도 PNG/SVG를 추출하여 PPT에 삽입, PPT 기본 도형의 한계를 극복.

---

## 4. 기존 PPT 데이터베이스화 방법론

전문가가 만든 PPT의 디자인 자산을 시스템이 학습하고 활용할 수 있도록 데이터베이스화하는 전략입니다.

### 4.1. 구조적 역공학 (Structural Reverse Engineering)

- **PPTX XML 분석**: `.pptx` 파일은 ZIP 압축 파일이며, `ppt/slideLayouts/`와 `ppt/slideMasters/` 폴더 내의 XML 파일에 레이아웃 정보가 담겨 있음.
- **자산 추출 자동화**:
  - XML 파싱을 통해 도형의 좌표(`x`, `y`), 크기(`cx`, `cy`), 스타일(Hex Code, 투명도, 그림자 설정) 추출.
  - 슬라이드 내 오브젝트 간의 상대적 거리와 계층 구조(Hierarchy)를 벡터화.

### 4.2. 데이터베이스 스키마 구성

| 필드명            | 설명                        | 예시                                              |
| ----------------- | --------------------------- | ------------------------------------------------- |
| `layout_type`     | 디자인 의도 분류            | `Comparison`, `Timeline`, `FeatureSpec`           |
| `visual_tokens`   | 색상 및 폰트 정보           | `{"bg": "#FFFFFF", "accent": "#0284C7"}`          |
| `geometry_map`    | 구성 요소 배치 좌표 정보    | `[{"type": "header", "rect": [10, 10, 100, 20]}]` |
| `aesthetic_score` | 디자인 품질 점수 (LLM 평가) | `9.5/10.0`                                        |

### 4.3. 활용 프로세스

1. 기성 전문가 PPT를 대량 수집.
2. 각 슬라이드의 레이아웃과 스타일 정보를 정규화하여 벡터 DB에 저장.
3. 새로운 콘텐츠 생성 시, 유사한 의도를 가진 '전문가 레이아웃'을 검색하여 디자인 가이드로 참조.

---

## 5. 실행 프로세스 및 도구

1.  **Input Parsing**: `project-plan.md`를 분석하여 슬라이드별 핵심 메시지 추출 (Tool: LLM - Gemini).
2.  **Design Mapping**: 추출된 메시지의 속성(데이터, 프로세스, 일반 텍스트)에 따라 DB에서 최적의 레이아웃 선정.
3.  **Code-based Generation**: `python-pptx` 라이브러리를 통해 레이어별 디자인 적용.
4.  **Polish**: AI 이미지 및 메쉬 그라데이션을 배경으로 삽입하여 "사람이 디자인한 것 같은" 마무리.

---

## 6. 결론

최고 수준의 PPT 생성 서비스는 단순히 텍스트를 옮기는 도구가 아니라, **전문 디자이너의 논리와 감각을 코드로 규격화(Standardization)**한 시스템이어야 합니다. 제안된 4계층 아키텍처와 PPT 레이아웃 데이터베이스화 전략은 이를 실현하기 위한 가장 확실한 방법론입니다.
