#!/usr/bin/env python3
"""
Extract slides 0-9 from PPT as content templates
"""

import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from datetime import datetime
import json

# Configuration
PPTX_PATH = "/home/jji/project/docs/PPT기본양식_병합_수정(선별).pptx"
UNPACKED_DIR = "/home/jji/project/docs/workspace/unpacked"
OUTPUT_DIR = "/home/jji/project/docs/templates/contents/templates"
ASPECT_RATIO = "16:9"

# EMU conversion constants
EMU_PER_INCH = 914400
PX_PER_INCH = 96
SLIDE_WIDTH_EMU = 12192000   # 1920px
SLIDE_HEIGHT_EMU = 6858000   # 1080px

# Slide configuration
SLIDES_CONFIG = {
    0: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 콘텐츠 레이아웃",
        "use_for": [
            "좌우 2열 구조의 텍스트 콘텐츠",
            "비교 설명 구조",
            "병렬 정보 제시",
            "대조 분석",
            "양측 요약 정보"
        ],
        "keywords": ["2열", "텍스트", "병렬", "좌우", "비교"],
        "prompt_keywords": ["두 열", "좌우 배치", "텍스트 비교", "병렬 정보"]
    },
    1: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 콘텐츠",
        "use_for": [
            "좌우 2열 구조의 콘텐츠 배치",
            "대칭적 정보 구성",
            "좌측-우측 비교",
            "양측 항목 나열",
            "병렬 설명"
        ],
        "keywords": ["2열", "텍스트", "콘텐츠", "병렬", "대칭"],
        "prompt_keywords": ["두 열 텍스트", "좌우 대칭", "병렬 배치", "콘텐츠 비교"]
    },
    2: {
        "category": "content",
        "design_intent": "content-cta",
        "name": "텍스트 + CTA 버튼 레이아웃",
        "use_for": [
            "행동 유도 (CTA) 포함 슬라이드",
            "제안 및 인터랙션",
            "버튼 클릭 유도",
            "가입/신청 페이지",
            "콜투액션 표시"
        ],
        "keywords": ["CTA", "버튼", "텍스트", "행동", "유도"],
        "prompt_keywords": ["행동 유도", "CTA 버튼", "클릭 유도", "콜투액션", "상호작용"]
    },
    3: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 레이아웃",
        "use_for": [
            "좌우 2열 텍스트 배치",
            "대조 정보 제시",
            "양측 설명",
            "병렬 항목 나열",
            "좌우 균형 맞춘 구성"
        ],
        "keywords": ["2열", "텍스트", "대조", "좌우", "균형"],
        "prompt_keywords": ["두 열 배치", "좌우 텍스트", "대조 구조", "병렬 정보", "균형잡힌 레이아웃"]
    },
    4: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 콘텐츠 구성",
        "use_for": [
            "좌우 분할 구조의 내용 배치",
            "이원 정보 제시",
            "좌측-우측 항목 대응",
            "텍스트 중심 구성",
            "칼럼 형식 레이아웃"
        ],
        "keywords": ["2열", "콘텐츠", "분할", "좌우", "칼럼"],
        "prompt_keywords": ["좌우 분할", "2열 구성", "병렬 콘텐츠", "텍스트 배치", "칼럼 레이아웃"]
    },
    5: {
        "category": "grid",
        "design_intent": "grid-3col",
        "name": "3열 그리드 레이아웃",
        "use_for": [
            "3열 그리드 구조",
            "카드형 항목 배치",
            "균등 분할 표현",
            "항목 비교 표시",
            "시각적 균형"
        ],
        "keywords": ["3열", "그리드", "카드", "균등", "분할"],
        "prompt_keywords": ["3열 그리드", "카드 배치", "균등 분할", "항목 표시", "그리드 구조"]
    },
    6: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 아이콘 그리드",
        "use_for": [
            "4열 아이콘 기반 그리드",
            "아이콘 + 텍스트 조합",
            "시각적 요소 강조",
            "기능/특징 표시",
            "다중 항목 표현"
        ],
        "keywords": ["4열", "아이콘", "그리드", "시각", "항목"],
        "prompt_keywords": ["아이콘 그리드", "4열 배치", "아이콘 + 텍스트", "기능 표시", "시각적 배치"]
    },
    7: {
        "category": "grid",
        "design_intent": "grid-4col",
        "name": "4열 텍스트 그리드",
        "use_for": [
            "4열 텍스트 기반 그리드",
            "균등한 항목 분배",
            "다중 정보 표현",
            "항목 나열",
            "격자 형식 구성"
        ],
        "keywords": ["4열", "텍스트", "그리드", "항목", "균등"],
        "prompt_keywords": ["4열 텍스트", "그리드 배치", "항목 나열", "격자 구성", "균등 분할"]
    },
    8: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 원형 아이콘 그리드",
        "use_for": [
            "4열 원형 아이콘",
            "순환 구조 표현",
            "아이콘 중심 디자인",
            "원형 요소 활용",
            "시각적 임팩트"
        ],
        "keywords": ["4열", "원형", "아이콘", "그리드", "순환"],
        "prompt_keywords": ["원형 아이콘", "4열 그리드", "순환 구조", "아이콘 배치", "원형 요소"]
    },
    9: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 원형 변형 아이콘",
        "use_for": [
            "4열 변형 아이콘 그리드",
            "스타일 변형 활용",
            "다양한 아이콘 표현",
            "창의적 구성",
            "특수 그리드 레이아웃"
        ],
        "keywords": ["4열", "변형", "아이콘", "원형", "그리드"],
        "prompt_keywords": ["변형 아이콘", "4열 배치", "창의적 구성", "스타일 변형", "특수 그리드"]
    }
}

def parse_slide_xml(slide_index):
    """Parse slide XML and extract shape information"""
    slide_path = Path(UNPACKED_DIR) / "ppt" / "slides" / f"slide{slide_index + 1}.xml"

    try:
        tree = ET.parse(str(slide_path))
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"Error parsing slide {slide_index}: {e}")
        return None

def extract_shapes(root):
    """Extract shape information from slide XML"""
    shapes = []

    # Define namespaces
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    # Extract all shapes
    for i, shape in enumerate(root.findall('.//p:sp', ns)):
        shape_info = {
            'id': f'shape-{i}',
            'index': i,
            'z_order': i
        }

        # Get name
        name_elem = shape.find('.//p:cNvPr', ns)
        if name_elem is not None:
            shape_info['name'] = name_elem.get('name', f'Shape {i}')

        # Get position and size
        xfrm = shape.find('.//a:xfrm', ns)
        if xfrm is not None:
            off = xfrm.find('a:off', ns)
            ext = xfrm.find('a:ext', ns)

            if off is not None and ext is not None:
                x_emu = int(off.get('x', 0))
                y_emu = int(off.get('y', 0))
                cx_emu = int(ext.get('cx', 0))
                cy_emu = int(ext.get('cy', 0))

                # Convert to percentage
                shape_info['x_emu'] = x_emu
                shape_info['y_emu'] = y_emu
                shape_info['cx_emu'] = cx_emu
                shape_info['cy_emu'] = cy_emu

        # Get text information
        txBody = shape.find('.//p:txBody', ns)
        if txBody is not None:
            shape_info['has_text'] = True

            # Count paragraphs
            paragraphs = txBody.findall('.//a:p', ns)
            shape_info['paragraph_count'] = len(paragraphs)

            # Get font size (from first run property)
            rPr = txBody.find('.//a:rPr', ns)
            if rPr is not None:
                sz = rPr.get('sz')
                if sz:
                    # Convert from 1/100 pt to pt
                    shape_info['font_size_pt'] = int(sz) / 100

        shapes.append(shape_info)

    return shapes

def create_yaml_template(slide_index, shapes):
    """Create YAML template for slide"""
    config = SLIDES_CONFIG.get(slide_index, {})
    category = config.get('category', 'content')
    design_intent = config.get('design_intent', 'generic')

    template = {
        'content_template': {
            'id': f"basic-{design_intent}{slide_index}",
            'name': config.get('name', f'Slide {slide_index} Template'),
            'version': '2.0',
            'source': str(PPTX_PATH),
            'source_slide_index': slide_index,
            'extracted_at': datetime.now().isoformat(),
        },
        'design_meta': {
            'quality_score': 8.5,
            'design_intent': design_intent,
            'visual_balance': 'symmetric' if 'content' in category else 'asymmetric',
            'information_density': 'medium',
        },
        'canvas': {
            'reference_width': 1920,
            'reference_height': 1080,
            'aspect_ratio': ASPECT_RATIO,
        },
        'shapes': [],
        'gaps': {
            'global': {
                'column_gap': 3.0,
                'row_gap': 2.5,
            },
            'between_shapes': []
        },
        'spatial_relationships': [],
        'groups': [],
        'use_for': config.get('use_for', []),
        'keywords': config.get('keywords', []),
        'expected_prompt': f"Create a {config.get('name', 'slide')} layout based on this template",
        'prompt_keywords': config.get('prompt_keywords', []),
    }

    # Add shape information (simplified)
    for i, shape in enumerate(shapes[:5]):  # Limit to first 5 shapes for clarity
        if 'cx_emu' in shape and shape['cx_emu'] > 0:
            shape_obj = {
                'id': shape['id'],
                'name': shape.get('name', f'Shape {i}'),
                'type': 'textbox' if shape.get('has_text') else 'rectangle',
                'z_index': shape.get('z_order', i),
                'geometry': {
                    'x': '?',  # Placeholder
                    'y': '?',
                    'cx': '?',
                    'cy': '?',
                    'rotation': 0,
                    'original_aspect_ratio': round(shape.get('cx_emu', 1) / max(shape.get('cy_emu', 1), 1), 3),
                },
            }

            if shape.get('has_text'):
                shape_obj['text'] = {
                    'has_text': True,
                    'placeholder_type': 'BODY',
                    'alignment': 'left',
                    'font_size_ratio': shape.get('font_size_pt', 14) / 1080,
                    'original_font_size_pt': shape.get('font_size_pt', 14),
                    'font_weight': 'normal',
                }

            template['shapes'].append(shape_obj)

    return template

def main():
    """Main extraction function"""
    print("Starting slide extraction...")

    extracted_files = []

    for slide_idx in range(10):
        print(f"\nProcessing slide {slide_idx}...")

        # Parse XML
        root = parse_slide_xml(slide_idx)
        if root is None:
            continue

        # Extract shapes
        shapes = extract_shapes(root)
        print(f"  Found {len(shapes)} shapes")

        # Create YAML template
        template = create_yaml_template(slide_idx, shapes)

        # Determine output path
        category = SLIDES_CONFIG[slide_idx]['category']
        design_intent = SLIDES_CONFIG[slide_idx]['design_intent']
        output_path = Path(OUTPUT_DIR) / category / f"basic-{design_intent}{slide_idx}.yaml"

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write YAML
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"  Saved to: {output_path}")
        extracted_files.append(str(output_path))

    # Print summary
    print(f"\n\nExtraction complete!")
    print(f"Generated {len(extracted_files)} template files:")
    for f in extracted_files:
        print(f"  {f}")

    return extracted_files

if __name__ == "__main__":
    main()
