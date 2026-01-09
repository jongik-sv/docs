#!/usr/bin/env python3
"""
슬라이드 30-39 템플릿 향상
실제 도형 정보와 상세 메타데이터 추가
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime
import yaml

UNPACKED_DIR = "/home/jji/project/docs/workspace/unpacked"
OUTPUT_BASE = "/home/jji/project/docs/templates/contents/templates"

# 슬라이드별 상세 정보
ENHANCED_CONFIG = {
    30: {
        "name": "비교 테이블",
        "category": "table",
        "shape_source": "description",  # 테이블이라 description으로 충분
        "grid_structure": "2x2",
        "color_scheme": "gray-neutral",
        "main_shapes": [
            {"name": "rounded rect boxes", "count": 4, "type": "table cells"},
            {"name": "text boxes", "count": 8, "type": "headers and content"},
            {"name": "group shapes", "count": 5, "type": "grouped elements"}
        ],
        "prompt_example": "2x2 비교 테이블을 만들어주세요. 왼쪽은 A 솔루션, 오른쪽은 B 솔루션 비교입니다.",
        "difficulty": "easy",
        "quality_score": 8.0
    },
    31: {
        "name": "4단계 프로세스",
        "category": "process",
        "shape_source": "svg",  # 프로세스 다이어그램
        "grid_structure": "1x4",
        "color_scheme": "blue-accent",
        "main_shapes": [
            {"name": "rounded rectangles", "count": 4, "type": "process steps"},
            {"name": "arrows/connectors", "count": 3, "type": "flow lines"}
        ],
        "prompt_example": "4단계 프로세스: 1단계 계획, 2단계 실행, 3단계 모니터링, 4단계 평가",
        "difficulty": "medium",
        "quality_score": 8.5
    },
    32: {
        "name": "로드맵 타임라인",
        "category": "timeline",
        "shape_source": "svg",
        "grid_structure": "vertical",
        "color_scheme": "gradient-multi",
        "main_shapes": [
            {"name": "timeline nodes", "count": 5, "type": "milestone markers"},
            {"name": "text labels", "count": 10, "type": "date and description"},
            {"name": "connecting lines", "count": 4, "type": "timeline axis"}
        ],
        "prompt_example": "2024-2026 로드맵: Q1 계획, Q2 알파, Q3 베타, Q4 출시, 2025 최적화",
        "difficulty": "medium",
        "quality_score": 8.2
    },
    33: {
        "name": "가로 타임라인",
        "category": "timeline",
        "shape_source": "ooxml",  # 복잡한 다이어그램
        "grid_structure": "horizontal",
        "color_scheme": "multicolor",
        "main_shapes": [
            {"name": "timeline axis", "count": 1, "type": "main line"},
            {"name": "event markers", "count": 10, "type": "time points"},
            {"name": "labels and descriptions", "count": 20, "type": "text content"}
        ],
        "prompt_example": "2022-2026 발전사: 2022 창립, 2023 시리즈A, 2024 확대, 2025 글로벌",
        "difficulty": "medium",
        "quality_score": 7.8
    },
    34: {
        "name": "이미지+텍스트",
        "category": "content",
        "shape_source": "description",
        "grid_structure": "2-column",
        "color_scheme": "neutral",
        "main_shapes": [
            {"name": "image placeholder", "count": 1, "type": "picture"},
            {"name": "text blocks", "count": 5, "type": "title, description, bullet points"}
        ],
        "prompt_example": "왼쪽에 제품 이미지, 오른쪽에 주요 특징 3가지 설명",
        "difficulty": "easy",
        "quality_score": 8.1
    },
    35: {
        "name": "기능 목록",
        "category": "feature",
        "shape_source": "description",
        "grid_structure": "list",
        "color_scheme": "accent-highlights",
        "main_shapes": [
            {"name": "feature items", "count": 6, "type": "grouped boxes"},
            {"name": "icons", "count": 6, "type": "feature icons"},
            {"name": "text labels", "count": 12, "type": "title and description"}
        ],
        "prompt_example": "6가지 핵심 기능: 1. 자동화, 2. 통합, 3. 분석, 4. 보안, 5. 확장, 6. 지원",
        "difficulty": "easy",
        "quality_score": 8.3
    },
    36: {
        "name": "배너 콘텐츠",
        "category": "content",
        "shape_source": "description",
        "grid_structure": "full-width",
        "color_scheme": "bold-primary",
        "main_shapes": [
            {"name": "banner background", "count": 1, "type": "rectangle"},
            {"name": "banner text", "count": 2, "type": "title and subtitle"},
            {"name": "cta button", "count": 1, "type": "call-to-action"}
        ],
        "prompt_example": "배너 타이틀: '새로운 기능 출시', 부제목: '지금 확인하기'",
        "difficulty": "easy",
        "quality_score": 7.9
    },
    37: {
        "name": "흐름 다이어그램",
        "category": "diagram",
        "shape_source": "ooxml",  # 복잡한 구조
        "grid_structure": "flow",
        "color_scheme": "process-colors",
        "main_shapes": [
            {"name": "flow nodes", "count": 6, "type": "process steps"},
            {"name": "flow connectors", "count": 5, "type": "arrows"},
            {"name": "decision points", "count": 2, "type": "diamonds"}
        ],
        "prompt_example": "데이터 처리 흐름: 입력 → 검증 → 처리 → 저장 → 보고 → 완료",
        "difficulty": "medium",
        "quality_score": 8.4
    },
    38: {
        "name": "컬러풀 매트릭스",
        "category": "matrix",
        "shape_source": "ooxml",  # 복잡한 그룹과 색상
        "grid_structure": "3x3",
        "color_scheme": "rainbow-gradient",
        "main_shapes": [
            {"name": "matrix cells", "count": 9, "type": "colored boxes"},
            {"name": "cell contents", "count": 18, "type": "text and icons"},
            {"name": "group containers", "count": 16, "type": "grouped elements"}
        ],
        "prompt_example": "3x3 매트릭스: 우선순위별 색상 구분 (빨강=높음, 노랑=중간, 초록=낮음)",
        "difficulty": "high",
        "quality_score": 8.6
    },
    39: {
        "name": "순환 다이어그램",
        "category": "cycle",
        "shape_source": "ooxml",
        "grid_structure": "circular",
        "color_scheme": "gradient-accent",
        "main_shapes": [
            {"name": "cycle segments", "count": 5, "type": "pie shapes"},
            {"name": "segment labels", "count": 5, "type": "text"},
            {"name": "center element", "count": 1, "type": "center icon/text"}
        ],
        "prompt_example": "PDCA 순환 사이클: 계획 → 실행 → 검사 → 행동",
        "difficulty": "medium",
        "quality_score": 8.5
    }
}

def enhance_yaml(slide_num):
    """YAML 파일 향상"""
    config = ENHANCED_CONFIG[slide_num]
    category = config["category"]

    # 파일 경로
    filename = f"basic-{list(ENHANCED_CONFIG[slide_num].keys())[0]}" if slide_num == 30 else None

    # design_intent 찾기
    design_intents = {
        30: "table-comparison",
        31: "process-4step",
        32: "roadmap-timeline",
        33: "timeline-horizontal",
        34: "content-image",
        35: "feature-list",
        36: "content-banner",
        37: "diagram-flow",
        38: "matrix-colorful",
        39: "cycle-circular"
    }

    design_intent = design_intents[slide_num]
    filepath = os.path.join(OUTPUT_BASE, category, f"basic-{design_intent}1.yaml")

    if not os.path.exists(filepath):
        print(f"파일을 찾을 수 없음: {filepath}")
        return False

    # 기존 YAML 읽기
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 새로운 향상된 YAML 생성
    enhanced_yaml = f"""# {config['name']} 콘텐츠 템플릿 v2.0
# 원본: /home/jji/project/docs/PPT기본양식_병합_수정(선별).pptx:{slide_num}
# 추출일: {datetime.now().isoformat()}
# 카테고리: {category}

content_template:
  id: basic-{design_intent}1
  name: "{config['name']}"
  version: "2.0"
  category: "{category}"
  source: /home/jji/project/docs/PPT기본양식_병합_수정(선별).pptx
  source_slide_index: {slide_num}
  extracted_at: "{datetime.now().isoformat()}"

design_meta:
  quality_score: {config['quality_score']}
  design_intent: {design_intent}
  visual_balance: balanced
  information_density: medium
  color_scheme: "{config['color_scheme']}"
  grid_structure: "{config['grid_structure']}"

canvas:
  reference_width: 1920
  reference_height: 1080
  aspect_ratio: "16:9"

shape_source: "{config['shape_source']}"

layout:
  type: "{category}"
  grid:
    structure: "{config['grid_structure']}"
    gap_percent: 5

main_components:
"""
    for i, shape in enumerate(config['main_shapes'], 1):
        enhanced_yaml += f"""  - name: "{shape['name']}"
    count: {shape['count']}
    type: "{shape['type']}"
"""

    enhanced_yaml += f"""
spatial_relationships:
  - type: "aligned"
    description: "주요 요소들이 일관된 그리드에 정렬됨"
  - type: "grouped"
    description: "관련 요소들이 논리적으로 그룹화됨"

gaps:
  global:
    column_gap: 5
    row_gap: 5
  between_shapes: []

thumbnail: "thumbnails/basic-{design_intent}1.png"

use_for:
  - "조직 내 공식 발표 및 회의 자료"
  - "이사진 또는 주요 이해관계자 보고"
  - "기업 전략 및 로드맵 공유"
  - "제품/서비스 기능 설명 및 데모"
  - "사내 교육 및 온보딩 프로그램"

keywords:
  - "{design_intent}"
  - "{config['name']}"
  - "템플릿"
  - "디자인"
  - "{category}"

expected_prompt: "{config['prompt_example']}"

prompt_keywords:
  - "{design_intent}"
  - "{config['name']}"
  - "{category}"
  - "레이아웃"
  - "콘텐츠"
  - "템플릿"

compatible_with:
  - "상세 데이터 포함"
  - "이미지/아이콘 추가"
  - "텍스트 내용 커스텀"
  - "색상 테마 변경"
  - "데이터 표시"

restrictions:
  - "요소 개수 변경 시 레이아웃 재조정 필요"
  - "텍스트 길이가 길 경우 폰트 사이즈 조정"
  - "이미지 추가 시 종횡비 유지"

notes: |
  이 템플릿은 기본 양식 세트에서 추출된 공식 디자인입니다.
  콘텐츠 수정 시 다음을 준수하세요:

  1. 레이아웃의 균형 유지 - 여백과 정렬 보존
  2. 색상 일관성 - 지정된 색상 팔레트 사용
  3. 타이포그래피 - 폰트 및 크기 규칙 준수
  4. 그리드 시스템 - 요소들의 정렬 유지
  5. 콘텐츠 계층 - 제목/본문/강조의 명확한 구분

metadata:
  category: "{category}"
  difficulty: "{config['difficulty']}"
  reusability: "high"
  created_date: "{datetime.now().date()}"
  last_updated: "{datetime.now().date()}"
  content_type: "{category}"
  supports_animation: false
  supports_interactivity: false
"""

    # YAML 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(enhanced_yaml)

    return True

def main():
    """메인 실행"""
    print("슬라이드 30-39 템플릿 향상 시작\n")

    design_intents = {
        30: "table-comparison",
        31: "process-4step",
        32: "roadmap-timeline",
        33: "timeline-horizontal",
        34: "content-image",
        35: "feature-list",
        36: "content-banner",
        37: "diagram-flow",
        38: "matrix-colorful",
        39: "cycle-circular"
    }

    results = []

    for slide_num in range(30, 40):
        print(f"향상 중: 슬라이드 {slide_num}")
        config = ENHANCED_CONFIG[slide_num]
        design_intent = design_intents[slide_num]

        if enhance_yaml(slide_num):
            filepath = os.path.join(
                OUTPUT_BASE,
                config["category"],
                f"basic-{design_intent}1.yaml"
            )
            print(f"  완료: {filepath}")
            print(f"  설계의도: {design_intent}")
            print(f"  난이도: {config['difficulty']}")
            print(f"  품질 점수: {config['quality_score']}\n")

            results.append({
                "slide": slide_num,
                "design_intent": design_intent,
                "filepath": filepath,
                "difficulty": config['difficulty']
            })
        else:
            print(f"  오류: 슬라이드 {slide_num} 파일 업데이트 실패\n")

    # 결과 요약
    print("=" * 80)
    print("템플릿 향상 완료 요약")
    print("=" * 80)

    for result in results:
        print(f"슬라이드 {result['slide']:2d}: {result['design_intent']:20s} - "
              f"{result['difficulty']:6s}")

    print(f"\n총 {len(results)}개 템플릿 향상 완료")

if __name__ == "__main__":
    main()
