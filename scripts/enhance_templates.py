#!/usr/bin/env python3
"""
생성된 템플릿에 추가 필드 추가
- shape_source: 도형 생성 방식 결정
- expected_prompt: 역추론 프롬프트
- prompt_keywords: 프롬프트 핵심 키워드
"""

import yaml
from pathlib import Path
from typing import List, Dict

# 슬라이드별 상세 정보
TEMPLATE_ENHANCEMENTS = {
    'basic-feature-icons': {
        'shape_source': 'description',  # 단순 상자들은 description으로
        'expected_prompt': '4개의 아이콘/이미지를 보여줄 수 있는 기능 표시 슬라이드를 만들어주세요. 각 기능마다 아이콘, 제목, 설명이 들어갈 수 있어야 합니다.',
        'prompt_keywords': ['4열', '아이콘', '기능', '한눈에', '특징', '균등배치'],
        'design_patterns': ['grid', 'icon-based', 'feature-showcase'],
        'content_structure': {
            'main_area': '상단 2/3: 4개 기능 박스 (좌상, 우상, 좌하, 우하)',
            'text_area': '하단: 상세 설명 또는 추가 정보',
            'visual_hierarchy': '아이콘 > 제목 > 설명'
        }
    },
    'basic-grid-image': {
        'shape_source': 'description',
        'expected_prompt': '3개 열의 이미지 그리드 레이아웃을 만들어주세요. 3xN 형태로 이미지를 배치할 수 있는 템플릿입니다.',
        'prompt_keywords': ['갤러리', '3열', '이미지', '포트폴리오', '균등배치', '그리드'],
        'design_patterns': ['gallery', 'image-grid', 'portfolio'],
        'content_structure': {
            'main_area': '3열 이미지 그리드 (가변 행 수)',
            'spacing': '균등한 행/열 간격',
            'visual_hierarchy': '이미지 중심'
        }
    },
    'basic-cycle-2circle': {
        'shape_source': 'ooxml',  # 복잡한 원형 도형 → ooxml로 원본 보존
        'expected_prompt': '2개의 원이 상호작용하는 순환 프로세스 다이어그램을 만들어주세요. 화살표로 연결되어 반복되는 사이클을 표현합니다.',
        'prompt_keywords': ['순환', '사이클', '피드백', '2단계', '상호작용', '관계', '다이어그램'],
        'design_patterns': ['cycle', 'feedback-loop', 'circular-process'],
        'content_structure': {
            'main_area': '2개 원 (좌우 배치) + 화살표 (순환 방향)',
            'connections': '화살표로 연결된 순환 구조',
            'visual_hierarchy': '원 > 텍스트 > 화살표'
        }
    },
    'basic-cycle-3circle': {
        'shape_source': 'ooxml',
        'expected_prompt': '3개의 원이 삼각형을 이루며 상호작용하는 다이어그램을 만들어주세요. 3-way 상호작용이나 순환 시스템을 표현합니다.',
        'prompt_keywords': ['순환', '3단계', '삼각형', '상호작용', '시스템', '프로세스', '관계'],
        'design_patterns': ['cycle', 'triangular-process', 'three-way-interaction'],
        'content_structure': {
            'main_area': '3개 원 (삼각형 배치) + 화살표 (순환 방향)',
            'connections': '3-way 순환 연결',
            'visual_hierarchy': '원 > 텍스트 > 화살표'
        }
    },
    'basic-process-4step': {
        'shape_source': 'description',
        'expected_prompt': '4단계 순차 프로세스를 보여주는 슬라이드를 만들어주세요. 각 단계가 화살표로 연결되어 흐름을 표현합니다.',
        'prompt_keywords': ['프로세스', '4단계', '흐름', '화살표', '순차', '절차', '진행'],
        'design_patterns': ['process-flow', 'step-by-step', 'sequence'],
        'content_structure': {
            'main_area': '4개 박스 (수평 배치) + 화살표 연결',
            'progression': '좌→우 순차 흐름',
            'visual_hierarchy': '숫자/아이콘 > 제목 > 설명'
        }
    },
    'basic-comparison-rounded': {
        'shape_source': 'description',
        'expected_prompt': '2가지 옵션을 나란히 비교하는 슬라이드를 만들어주세요. 둥근 박스로 부드러운 느낌의 비교 레이아웃입니다.',
        'prompt_keywords': ['비교', '2가지', '옵션', '대안', '라운드', '특징', '차이'],
        'design_patterns': ['comparison', 'two-column', 'rounded-design'],
        'content_structure': {
            'main_area': '2개 둥근 박스 (좌우 배치)',
            'content_per_box': '제목 + 주요 특징 리스트',
            'visual_hierarchy': '제목 > 특징항목 > 설명'
        }
    },
    'basic-stats-donut': {
        'shape_source': 'ooxml',  # 복잡한 차트 → ooxml
        'expected_prompt': '비율 통계를 도넛 차트로 시각화하는 슬라이드를 만들어주세요. 각 구간별 비율과 범례를 함께 표시합니다.',
        'prompt_keywords': ['도넛', '차트', '통계', '비율', '점유율', '시각화', '데이터'],
        'design_patterns': ['chart', 'statistics', 'data-visualization'],
        'content_structure': {
            'main_area': '도넛 차트 + 범례 + 통계값',
            'chart_details': '4-5개 세그먼트, 중앙 텍스트 가능',
            'visual_hierarchy': '차트 > 수치 > 범례'
        }
    },
    'basic-stats-cards': {
        'shape_source': 'description',
        'expected_prompt': 'KPI 또는 주요 지표를 카드 형태로 배치하는 대시보드 슬라이드를 만들어주세요. 숫자와 라벨이 명확하게 표시됩니다.',
        'prompt_keywords': ['카드', '통계', 'KPI', '지표', '메트릭', '요약', '대시보드'],
        'design_patterns': ['dashboard', 'metrics', 'kpi-cards'],
        'content_structure': {
            'main_area': '3-4개 카드 (그리드 배치)',
            'per_card': '큰 숫자 + 라벨 + 부수 정보',
            'visual_hierarchy': '숫자 > 라벨 > 비교값'
        }
    },
    'basic-comparison-highlight': {
        'shape_source': 'description',
        'expected_prompt': '2가지 항목을 비교하면서 주요 강점을 하이라이트로 표시하는 슬라이드를 만들어주세요. 시각적 강조가 중요합니다.',
        'prompt_keywords': ['비교', '강조', '하이라이트', '선택', '강점', '차이', '대비'],
        'design_patterns': ['comparison', 'highlight', 'emphasis'],
        'content_structure': {
            'main_area': '2개 항목 + 강점 표시 (색상/아이콘)',
            'highlight_method': '색상, 체크마크, 또는 배경 강조',
            'visual_hierarchy': '강조 요소 > 제목 > 내용'
        }
    },
    'basic-content-quote': {
        'shape_source': 'description',
        'expected_prompt': '인용문 또는 주요 메시지를 강조 표시하는 슬라이드를 만들어주세요. 텍스트 중심의 콘텐츠입니다.',
        'prompt_keywords': ['인용', '명언', '메시지', '강조', '텍스트', '톤앤매너', '설명'],
        'design_patterns': ['quote', 'message', 'text-focus'],
        'content_structure': {
            'main_area': '대형 텍스트 (인용문 또는 메시지)',
            'supporting_text': '출처 또는 설명 문구',
            'visual_hierarchy': '인용문 > 출처 > 배경 이미지/패턴'
        }
    }
}


def enhance_yaml_file(filepath: str) -> Dict:
    """YAML 파일에 추가 필드 추가"""

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # 템플릿 ID 추출
    template_id = data['content_template']['id']

    if template_id not in TEMPLATE_ENHANCEMENTS:
        print(f"WARNING: No enhancement data for {template_id}")
        return None

    enhancement = TEMPLATE_ENHANCEMENTS[template_id]

    # 기존 content_template에 추가 필드
    data['content_template']['shape_source'] = enhancement['shape_source']
    data['content_template']['expected_prompt'] = enhancement['expected_prompt']
    data['content_template']['prompt_keywords'] = enhancement['prompt_keywords']

    # 새로운 섹션 추가
    data['design_patterns'] = enhancement['design_patterns']
    data['content_structure'] = enhancement['content_structure']

    # use_for 보강
    data['use_for'] = list(set(data.get('use_for', []) + [
        enhancement['content_structure']['main_area'].split(':')[0]
    ]))

    return data


def main():
    template_dir = Path("/home/jji/project/docs/templates/contents/templates")

    # 모든 basic-*.yaml 파일 찾기
    yaml_files = list(template_dir.rglob("basic-*.yaml"))
    print(f"Found {len(yaml_files)} template files\n")

    for yaml_file in sorted(yaml_files):
        try:
            print(f"Enhancing: {yaml_file.name}")

            enhanced_data = enhance_yaml_file(str(yaml_file))
            if enhanced_data is None:
                continue

            # 파일에 다시 저장
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(enhanced_data, f,
                         default_flow_style=False,
                         allow_unicode=True,
                         sort_keys=False)

            template_id = enhanced_data['content_template']['id']
            print(f"  ✓ shape_source: {enhanced_data['content_template']['shape_source']}")
            print(f"  ✓ Keywords: {', '.join(enhanced_data['content_template']['prompt_keywords'][:3])}")

        except Exception as e:
            print(f"  ERROR: {e}")

    print("\n" + "="*60)
    print("Enhancement complete!")
    print("="*60)


if __name__ == '__main__':
    main()
