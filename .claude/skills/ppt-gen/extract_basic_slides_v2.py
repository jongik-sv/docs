#!/usr/bin/env python3
"""
Extract slides 0-9 from PPT as detailed content templates (v2)
"""

import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

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

# Content zones for filtering
CONTENT_TOP_RATIO = 0.15  # 15% from top (title area)
CONTENT_BOTTOM_RATIO = 0.92  # 92% from bottom (footer area)

# Slide detailed configuration
SLIDES_CONFIG = {
    0: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 콘텐츠 레이아웃",
        "description": "좌우 대칭 구조의 2열 텍스트 콘텐츠 배치 템플릿",
        "use_for": [
            "좌우 2열 구조의 텍스트 콘텐츠 배치",
            "비교 분석 및 대조 설명",
            "병렬 정보 제시 (좌측, 우측)",
            "대조 가능한 항목 설명",
            "양측 관점 또는 요약 정보"
        ],
        "keywords": ["2열", "텍스트", "병렬", "좌우", "비교", "대칭"],
        "prompt_keywords": ["두 열 텍스트 배치", "좌우 대칭", "텍스트 비교", "병렬 정보", "양측 내용"],
        "expected_prompt": "좌우 2열 구조로 텍스트 콘텐츠를 배치하는 레이아웃",
        "shape_sources": "description"  # Simple layout
    },
    1: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 콘텐츠",
        "description": "2열 구조의 텍스트 기반 콘텐츠 배치",
        "use_for": [
            "좌우 2열 구조의 콘텐츠 배치",
            "대칭적이고 균형잡힌 정보 구성",
            "좌측 항목과 우측 항목의 비교",
            "양측 내용 병렬 나열",
            "텍스트 중심의 정보 표현"
        ],
        "keywords": ["2열", "텍스트", "콘텐츠", "병렬", "대칭", "균형"],
        "prompt_keywords": ["두 열 텍스트", "좌우 대칭 배치", "병렬 배치", "콘텐츠 비교", "균형잡힌 구성"],
        "expected_prompt": "2열 텍스트 콘텐츠를 균형있게 배치하는 레이아웃",
        "shape_sources": "description"
    },
    2: {
        "category": "content",
        "design_intent": "content-cta",
        "name": "텍스트 + CTA 버튼 레이아웃",
        "description": "텍스트와 행동 유도(CTA) 버튼을 포함한 콘텐츠 슬라이드",
        "use_for": [
            "행동 유도(CTA) 버튼이 포함된 슬라이드",
            "사용자 상호작용 유도 (클릭, 가입 등)",
            "제안 및 인터랙션이 필요한 페이지",
            "버튼 클릭 유도를 통한 다음 단계 진행",
            "콜투액션(Call To Action) 명확히 표시"
        ],
        "keywords": ["CTA", "버튼", "텍스트", "행동", "유도", "상호작용"],
        "prompt_keywords": ["행동 유도 버튼", "CTA 버튼 포함", "클릭 유도", "콜투액션", "상호작용 요소"],
        "expected_prompt": "텍스트와 CTA 버튼으로 구성된 행동 유도 레이아웃",
        "shape_sources": "description"
    },
    3: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 텍스트 레이아웃",
        "description": "대조적 정보를 표현하는 2열 텍스트 구성",
        "use_for": [
            "좌우 2열 텍스트 배치",
            "대조적인 정보 및 항목 제시",
            "양측 설명 및 상세 정보",
            "항목별 병렬 나열",
            "좌우 균형을 맞춘 콘텐츠 구성"
        ],
        "keywords": ["2열", "텍스트", "대조", "좌우", "균형", "배치"],
        "prompt_keywords": ["두 열 텍스트 배치", "좌우 텍스트", "대조 구조", "병렬 정보", "균형잡힌 레이아웃"],
        "expected_prompt": "좌우 2열로 대조적 텍스트 정보를 표현하는 레이아웃",
        "shape_sources": "description"
    },
    4: {
        "category": "content",
        "design_intent": "content-2col",
        "name": "2열 콘텐츠 구성",
        "description": "분할된 2열 구조의 종합 콘텐츠 배치",
        "use_for": [
            "좌우 분할 구조의 내용 배치",
            "이원적 정보 제시 및 비교",
            "좌측-우측 항목 대응 표현",
            "텍스트 중심의 상세 구성",
            "칼럼 형식의 신문 스타일 레이아웃"
        ],
        "keywords": ["2열", "콘텐츠", "분할", "좌우", "칼럼", "배치"],
        "prompt_keywords": ["좌우 분할 구조", "2열 콘텐츠", "병렬 콘텐츠", "텍스트 배치", "칼럼형 레이아웃"],
        "expected_prompt": "좌우 분할된 2열 콘텐츠 구성 레이아웃",
        "shape_sources": "description"
    },
    5: {
        "category": "grid",
        "design_intent": "grid-3col",
        "name": "3열 그리드 레이아웃",
        "description": "3열 균등 분할 그리드 카드 레이아웃",
        "use_for": [
            "3열 그리드 구조의 카드형 항목 배치",
            "카드형 컨텐츠의 균등 분할 표현",
            "3개 항목의 균형있는 시각적 표현",
            "항목별 카드 기반 정보 비교",
            "시각적 균형과 대칭성 강조"
        ],
        "keywords": ["3열", "그리드", "카드", "균등", "분할", "항목"],
        "prompt_keywords": ["3열 그리드", "카드형 배치", "균등 분할", "항목 표시", "카드 그리드"],
        "expected_prompt": "3열 그리드로 항목을 균등하게 배치하는 카드형 레이아웃",
        "shape_sources": "description"
    },
    6: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 아이콘 그리드",
        "description": "4열 구조의 아이콘과 텍스트 조합 그리드",
        "use_for": [
            "4열 아이콘 기반 그리드 배치",
            "아이콘과 텍스트 라벨의 조합",
            "시각적 요소를 강조한 그리드",
            "기능 또는 특징 아이콘 표시",
            "다중 항목의 아이콘 기반 표현"
        ],
        "keywords": ["4열", "아이콘", "그리드", "시각", "항목", "라벨"],
        "prompt_keywords": ["아이콘 그리드", "4열 아이콘 배치", "아이콘 + 텍스트", "기능 표시", "시각적 그리드"],
        "expected_prompt": "4열 아이콘 그리드로 주요 기능이나 항목을 표시하는 레이아웃",
        "shape_sources": "description"
    },
    7: {
        "category": "grid",
        "design_intent": "grid-4col",
        "name": "4열 텍스트 그리드",
        "description": "4열 구조의 텍스트 기반 항목 그리드",
        "use_for": [
            "4열 텍스트 기반 그리드 배치",
            "균등한 항목 분배 및 나열",
            "다중 정보의 격자형 표현",
            "항목별 텍스트 나열",
            "격자 형식의 구조화된 콘텐츠 구성"
        ],
        "keywords": ["4열", "텍스트", "그리드", "항목", "균등", "배치"],
        "prompt_keywords": ["4열 텍스트 그리드", "항목 나열", "격자형 배치", "균등 분할", "텍스트 그리드"],
        "expected_prompt": "4열 텍스트 그리드로 항목을 체계적으로 배치하는 레이아웃",
        "shape_sources": "description"
    },
    8: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 원형 아이콘 그리드",
        "description": "4열 구조의 원형 아이콘 그리드",
        "use_for": [
            "4열 원형 아이콘 시각화",
            "순환 구조 또는 프로세스 표현",
            "아이콘 중심의 시각적 디자인",
            "원형 요소를 활용한 그리드",
            "시각적 임팩트가 강한 아이콘 배치"
        ],
        "keywords": ["4열", "원형", "아이콘", "그리드", "순환", "시각"],
        "prompt_keywords": ["원형 아이콘", "4열 원형 그리드", "순환 구조", "아이콘 배치", "원형 요소"],
        "expected_prompt": "4열 원형 아이콘 그리드로 프로세스나 단계를 시각화하는 레이아웃",
        "shape_sources": "description"
    },
    9: {
        "category": "grid",
        "design_intent": "grid-icon",
        "name": "4열 변형 아이콘 그리드",
        "description": "4열 구조의 변형된 아이콘 그리드 레이아웃",
        "use_for": [
            "4열 변형 아이콘 그리드 배치",
            "스타일 변형을 활용한 아이콘 표현",
            "다양한 아이콘 스타일 표현",
            "창의적이고 특수한 그리드 구성",
            "특수 목적의 아이콘 배치"
        ],
        "keywords": ["4열", "변형", "아이콘", "원형", "그리드", "스타일"],
        "prompt_keywords": ["변형 아이콘", "4열 변형 그리드", "창의적 구성", "스타일 변형", "특수 그리드"],
        "expected_prompt": "4열 변형 아이콘 그리드로 창의적인 항목 표현을 하는 레이아웃",
        "shape_sources": "description"
    }
}

def parse_slide_xml(slide_index: int) -> ET.Element:
    """Parse slide XML and extract root element"""
    slide_path = Path(UNPACKED_DIR) / "ppt" / "slides" / f"slide{slide_index + 1}.xml"

    try:
        tree = ET.parse(str(slide_path))
        return tree.getroot()
    except Exception as e:
        print(f"Error parsing slide {slide_index}: {e}")
        return None

def emu_to_percent(value_emu: int, is_width: bool = True) -> float:
    """Convert EMU to percentage"""
    if is_width:
        return (value_emu / SLIDE_WIDTH_EMU) * 100
    else:
        return (value_emu / SLIDE_HEIGHT_EMU) * 100

def extract_shapes_detailed(root: ET.Element, slide_index: int) -> List[Dict[str, Any]]:
    """Extract detailed shape information from slide"""
    shapes = []

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    # Get all shapes
    all_elements = root.findall('.//p:sp', ns)
    all_elements.extend(root.findall('.//p:cxnSp', ns))

    for i, shape in enumerate(all_elements):
        shape_info = {'index': i, 'z_order': i}

        # Get name
        name_elem = shape.find('.//p:cNvPr', ns)
        if name_elem is not None:
            shape_info['name'] = name_elem.get('name', f'Shape {i}')

        # Get placeholder type
        ph_elem = shape.find('.//p:ph', ns)
        if ph_elem is not None:
            ph_type = ph_elem.get('type', 'body')
            shape_info['placeholder_type'] = ph_type.upper()

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

                # Calculate percentages
                x_pct = emu_to_percent(x_emu, is_width=True)
                y_pct = emu_to_percent(y_emu, is_width=False)
                cx_pct = emu_to_percent(cx_emu, is_width=True)
                cy_pct = emu_to_percent(cy_emu, is_width=False)

                shape_info['geometry'] = {
                    'x_emu': x_emu,
                    'y_emu': y_emu,
                    'cx_emu': cx_emu,
                    'cy_emu': cy_emu,
                    'x_pct': round(x_pct, 2),
                    'y_pct': round(y_pct, 2),
                    'cx_pct': round(cx_pct, 2),
                    'cy_pct': round(cy_pct, 2),
                    'center_y_pct': round(y_pct + cy_pct / 2, 2),
                }

                # Aspect ratio
                if cy_emu > 0:
                    aspect_ratio = cx_emu / cy_emu
                    shape_info['aspect_ratio'] = round(aspect_ratio, 3)

        # Get text information
        txBody = shape.find('.//p:txBody', ns)
        if txBody is not None:
            shape_info['has_text'] = True

            # Get text content (sample)
            text_content = []
            for para in txBody.findall('.//a:p', ns):
                for run in para.findall('.//a:r', ns):
                    t_elem = run.find('a:t', ns)
                    if t_elem is not None and t_elem.text:
                        text_content.append(t_elem.text)

            if text_content:
                shape_info['text_sample'] = ''.join(text_content)[:50]  # First 50 chars

            # Get font size
            rPr_list = txBody.findall('.//a:rPr', ns)
            if rPr_list:
                for rPr in rPr_list:
                    sz = rPr.get('sz')
                    if sz:
                        shape_info['font_size_pt'] = int(sz) / 100
                        break

        # Get shape type
        prstGeom = shape.find('.//a:prstGeom', ns)
        if prstGeom is not None:
            shape_info['shape_type'] = prstGeom.get('prst', 'rect')

        shapes.append(shape_info)

    return shapes

def should_include_shape(shape_info: Dict) -> bool:
    """Determine if shape should be included in template"""
    # Skip footer and page number placeholders
    if 'placeholder_type' in shape_info:
        if shape_info['placeholder_type'] in ['SLDNUM', 'FTR', 'DT']:
            return False

    # Skip shapes with very small height (likely decorative)
    if 'geometry' in shape_info:
        if shape_info['geometry']['cy_pct'] < 1.0:
            return False

    # Skip shapes in title area (top 15%)
    if 'geometry' in shape_info:
        center_y = shape_info['geometry']['center_y_pct']
        if center_y < 10:  # In title area
            return False

    return True

def create_yaml_template_detailed(slide_index: int, shapes: List[Dict]) -> Dict:
    """Create detailed YAML template"""
    config = SLIDES_CONFIG[slide_index]
    category = config['category']
    design_intent = config['design_intent']

    # Filter relevant shapes
    relevant_shapes = [s for s in shapes if should_include_shape(s)]

    template = {
        'content_template': {
            'id': f"basic-{design_intent}{slide_index}",
            'name': config['name'],
            'description': config['description'],
            'version': '2.0',
            'source': str(PPTX_PATH),
            'source_slide_index': slide_index,
            'extracted_at': datetime.now().isoformat(),
        },
        'design_meta': {
            'quality_score': 8.5,
            'design_intent': design_intent,
            'visual_balance': 'symmetric' if 'content' in category else 'asymmetric',
            'information_density': 'medium' if '2col' in design_intent else 'high',
            'layout_type': 'text-based' if 'content' in category else 'grid-based',
        },
        'canvas': {
            'reference_width': 1920,
            'reference_height': 1080,
            'aspect_ratio': ASPECT_RATIO,
        },
        'shapes': [],
        'gaps': {
            'global': {
                'column_gap': 3.5 if 'col' in design_intent else 2.0,
                'row_gap': 2.5 if '3col' in design_intent or '4col' in design_intent else 3.0,
            },
            'between_shapes': []
        },
        'spatial_relationships': [],
        'groups': [],
        'thumbnail': f"thumbnails/basic-{design_intent}{slide_index}.png",
        'use_for': config['use_for'],
        'keywords': config['keywords'],
        'expected_prompt': config['expected_prompt'],
        'prompt_keywords': config['prompt_keywords'],
    }

    # Add shape information
    for shape in relevant_shapes[:8]:  # Limit to 8 important shapes
        if 'geometry' in shape:
            shape_obj = {
                'id': f"shape-{shape['index']}",
                'name': shape.get('name', f"Shape {shape['index']}"),
                'type': shape.get('shape_type', 'rect'),
                'z_index': shape['z_order'],
                'geometry': {
                    'x': f"{shape['geometry']['x_pct']}%",
                    'y': f"{shape['geometry']['y_pct']}%",
                    'cx': f"{shape['geometry']['cx_pct']}%",
                    'cy': f"{shape['geometry']['cy_pct']}%",
                    'rotation': 0,
                    'original_aspect_ratio': shape.get('aspect_ratio', 1.0),
                }
            }

            if shape.get('has_text'):
                shape_obj['text'] = {
                    'has_text': True,
                    'placeholder_type': shape.get('placeholder_type', 'BODY'),
                    'alignment': 'left',
                    'font_size_ratio': shape.get('font_size_pt', 14) / 1080,
                    'original_font_size_pt': shape.get('font_size_pt', 14),
                    'font_weight': 'normal',
                }

            template['shapes'].append(shape_obj)

    return template

def main():
    """Main extraction function"""
    print("Starting detailed slide extraction (v2)...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    extracted_files = []

    for slide_idx in range(10):
        print(f"Processing slide {slide_idx}...", end=" ")

        # Parse XML
        root = parse_slide_xml(slide_idx)
        if root is None:
            print("FAILED")
            continue

        # Extract detailed shapes
        shapes = extract_shapes_detailed(root, slide_idx)
        relevant = [s for s in shapes if should_include_shape(s)]
        print(f"({len(shapes)} shapes, {len(relevant)} relevant)")

        # Create YAML template
        template = create_yaml_template_detailed(slide_idx, shapes)

        # Determine output path
        category = SLIDES_CONFIG[slide_idx]['category']
        design_intent = SLIDES_CONFIG[slide_idx]['design_intent']
        output_path = Path(OUTPUT_DIR) / category / f"basic-{design_intent}{slide_idx}.yaml"

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write YAML
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"  -> Saved: {output_path.relative_to(Path(OUTPUT_DIR).parent)}")
        extracted_files.append(str(output_path))

    # Print summary
    print(f"\n{'='*70}")
    print(f"Extraction complete!")
    print(f"Generated {len(extracted_files)} template files:")
    print(f"{'='*70}")

    for category in sorted(set(SLIDES_CONFIG[i]['category'] for i in range(10))):
        files = [f for f in extracted_files if f'/{category}/' in f]
        if files:
            print(f"\n{category.upper()} ({len(files)} files):")
            for f in sorted(files):
                print(f"  {Path(f).name}")

    return extracted_files

if __name__ == "__main__":
    main()
