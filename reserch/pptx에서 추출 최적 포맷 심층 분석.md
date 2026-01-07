● PPTX에서 양식과 도형을 추출하는 최적의 포맷에 대해 심층 분석해드리겠습니다.

  추출 포맷 비교 분석

  1. 현재 접근법들

  | 포맷  | 장점                | 단점                | 적합한 용도             |
  |-------|---------------------|---------------------|-------------------------|
  | YAML  | 가독성, 편집 용이   | 복잡 도형 정보 손실 | 메타데이터, 레이아웃    |
  | SVG   | 곡선/경로 정밀 보존 | PPTX 변환 필요      | 다이어그램, 커스텀 도형 |
  | OOXML | 100% 원본 충실도    | 복잡, 편집 어려움   | 정확한 재현 필요시      |
  | JSON  | 기계 처리 용이      | YAML과 동일한 한계  | API 연동                |

  2. PPTX 내부 구조

  .pptx (ZIP)
  ├── [Content_Types].xml
  ├── _rels/
  ├── docProps/
  ├── ppt/
  │   ├── presentation.xml      # 프레젠테이션 메타데이터
  │   ├── slides/
  │   │   ├── slide1.xml        # 슬라이드별 도형 정의
  │   │   └── _rels/
  │   ├── slideLayouts/         # 레이아웃 템플릿
  │   ├── slideMasters/         # 마스터 슬라이드
  │   └── theme/                # 테마 (색상, 폰트)

  3. 권장: 계층적 하이브리드 포맷

  # 최적의 추출 포맷 v3.1
  content_template:
    id: "example-template"
    version: "3.1"

    # Layer 1: 메타데이터 (YAML)
    design_meta:
      quality_score: 9.0
      design_intent: cycle-4arrow
      render_method: hybrid  # yaml | svg | ooxml

    # Layer 2: 캔버스/레이아웃 (YAML)
    canvas:
      reference_width: 960
      reference_height: 540

    # Layer 3: 단순 도형 (YAML geometry)
    shapes:
      - id: "title-box"
        type: textbox          # 단순 → YAML
        geometry: {x: 5%, y: 5%, cx: 90%, cy: 10%}

      - id: "cycle-diagram"
        type: svg              # 복잡 → SVG
        geometry: {x: 20%, y: 25%, cx: 60%, cy: 55%}
        svg:
          path: "M 330,195 C 380,120..."

      - id: "gradient-bg"
        type: ooxml            # 정밀 효과 → OOXML
        ooxml_ref: "ppt/slides/slide1.xml#sp[1]"

    # Layer 4: 원본 OOXML 스니펫 (선택적 보존)
    ooxml_snippets:
      "gradient-bg": |
        <p:sp>
          <p:spPr>
            <a:gradFill>...</a:gradFill>
          </p:spPr>
        </p:sp>

  4. 도형 유형별 최적 포맷

  | 도형 유형                 | 최적 포맷     | 이유                          |
  |---------------------------|---------------|-------------------------------|
  | 사각형, 원, 텍스트박스    | YAML geometry | 단순, 편집 용이               |
  | 곡선 화살표, 사이클       | SVG path      | Bezier 곡선 보존              |
  | 벌집형, 방사형 다이어그램 | SVG inline    | 복잡한 배치 보존              |
  | 3D 효과, 글로우           | OOXML snippet | PPT 전용 효과                 |
  | 그라데이션 (단순)         | YAML          | {type: linear, colors: [...]} |
  | 그라데이션 (복잡)         | OOXML         | 정밀 색상 정지점              |
  | 이미지/사진               | 파일 참조     | assets/image.png              |
  | SmartArt                  | SVG + OOXML   | 구조는 SVG, 스타일은 OOXML    |

  5. 추출 워크플로우 제안

  PPTX 입력
      │
      ▼
  ┌─────────────────────────────────────┐
  │  Step 1: 구조 분석                   │
  │  - python-pptx로 도형 목록 추출      │
  │  - 도형 유형별 분류                  │
  └─────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────┐
  │  Step 2: 복잡도 판단                 │
  │  - 단순 도형 → YAML geometry         │
  │  - 복잡 도형 → SVG 변환 시도         │
  │  - 변환 실패/효과 손실 → OOXML 보존  │
  └─────────────────────────────────────┘
      │
      ▼
  ┌─────────────────────────────────────┐
  │  Step 3: 통합 YAML 생성              │
  │  - 메타데이터 + shapes[] 조합        │
  │  - svg.inline / ooxml_snippets 포함  │
  └─────────────────────────────────────┘
      │
      ▼
  content_template.yaml

  6. 구현 방안

  신규 워크플로우 파일 제안: workflows/pptx-extract.md

  ## PPTX → Content Template 추출

  ### 입력
  - .pptx 파일

  ### 출력
  - content_template.yaml (하이브리드 포맷)

  ### 도구
  - python-pptx: 구조 파싱
  - svg.js: 복잡 도형 → SVG 변환
  - lxml: OOXML 스니펫 추출

  7. 결론

  최적의 포맷: YAML + SVG + OOXML 하이브리드

  | 계층          | 포맷          | 내용                  |
  |---------------|---------------|-----------------------|
  | 메타데이터    | YAML          | ID, 버전, 디자인 의도 |
  | 레이아웃      | YAML          | 캔버스, 배치          |
  | 단순 도형     | YAML geometry | x%, y%, cx%, cy%      |
  | 복잡 도형     | SVG inline    | path, viewBox         |
  | PPT 전용 효과 | OOXML snippet | 원본 XML 보존         |

  이 방식으로 편집 용이성(YAML), 정밀도(SVG), 완전한 재현(OOXML)을 모두 확보할 수 있습니다.     

  ---
  새로운 추출 워크플로우(pptx-extract.md)를 생성할까요?
  ⎿  Stop says: 요청완료
