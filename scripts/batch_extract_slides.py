#!/usr/bin/env python3
"""
배치 슬라이드 콘텐츠 템플릿 추출기
슬라이드 20-29 (XML: slide21-slide30)에서 design_intent별로 템플릿 생성
"""

import xml.etree.ElementTree as ET
import yaml
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict

# EMU 상수
EMU_PER_INCH = 914400
PX_PER_INCH = 96

# 슬라이드 크기 (16:9)
SLIDE_WIDTH_EMU = 12192000   # 1920px
SLIDE_HEIGHT_EMU = 6858000   # 1080px

# 콘텐츠 영역 마진 (타이틀/푸터 제외)
CONTENT_LEFT_RATIO = 0.03
CONTENT_RIGHT_RATIO = 0.97
CONTENT_TOP_RATIO = 0.20
CONTENT_BOTTOM_RATIO = 0.95

# 슬라이드 메타데이터
SLIDES_INFO = {
    20: {
        "design_intent": "feature-icons",
        "name": "4열 아이콘 기능 표시",
        "category": "feature"
    },
    21: {
        "design_intent": "grid-image",
        "name": "3열 이미지 그리드",
        "category": "grid"
    },
    22: {
        "design_intent": "cycle-2circle",
        "name": "2개 원 순환 다이어그램",
        "category": "cycle"
    },
    23: {
        "design_intent": "cycle-3circle",
        "name": "3개 원 순환 다이어그램",
        "category": "cycle"
    },
    24: {
        "design_intent": "process-4step",
        "name": "4단계 프로세스 흐름",
        "category": "process"
    },
    25: {
        "design_intent": "comparison-rounded",
        "name": "둥근 박스 비교 레이아웃",
        "category": "comparison"
    },
    26: {
        "design_intent": "stats-donut",
        "name": "도넛 차트 통계",
        "category": "stats"
    },
    27: {
        "design_intent": "stats-cards",
        "name": "통계 카드 레이아웃",
        "category": "stats"
    },
    28: {
        "design_intent": "comparison-highlight",
        "name": "하이라이트 비교 레이아웃",
        "category": "comparison"
    },
    29: {
        "design_intent": "content-quote",
        "name": "인용/설명 콘텐츠",
        "category": "content"
    }
}

class SlideExtractor:
    def __init__(self, unpacked_dir):
        self.unpacked_dir = Path(unpacked_dir)
        self.namespaces = {
            'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }

    def read_slide_xml(self, slide_num):
        """슬라이드 XML 읽기 (slide_num: 1-based)"""
        slide_path = self.unpacked_dir / f"ppt/slides/slide{slide_num}.xml"
        if not slide_path.exists():
            raise FileNotFoundError(f"Slide {slide_num} not found")

        tree = ET.parse(slide_path)
        return tree.getroot()

    def emu_to_percent(self, emu_value, slide_dimension_emu):
        """EMU를 퍼센트로 변환"""
        return (emu_value / slide_dimension_emu) * 100

    def get_shape_info(self, shape_elem):
        """도형 정보 추출"""
        info = {}

        # 아이디와 이름
        cNvPr = shape_elem.find('.//p:cNvPr', self.namespaces)
        if cNvPr is not None:
            info['id'] = cNvPr.get('id')
            info['name'] = cNvPr.get('name', 'Unknown')

        # 변환 정보 (위치, 크기)
        xfrm = shape_elem.find('.//a:xfrm', self.namespaces)
        if xfrm is not None:
            off = xfrm.find('a:off', self.namespaces)
            ext = xfrm.find('a:ext', self.namespaces)

            if off is not None and ext is not None:
                x_emu = int(off.get('x', 0))
                y_emu = int(off.get('y', 0))
                cx_emu = int(ext.get('cx', 0))
                cy_emu = int(ext.get('cy', 0))

                info['x_emu'] = x_emu
                info['y_emu'] = y_emu
                info['cx_emu'] = cx_emu
                info['cy_emu'] = cy_emu

                # 퍼센트 변환
                content_width = SLIDE_WIDTH_EMU * (CONTENT_RIGHT_RATIO - CONTENT_LEFT_RATIO)
                content_height = SLIDE_HEIGHT_EMU * (CONTENT_BOTTOM_RATIO - CONTENT_TOP_RATIO)

                info['x_percent'] = (x_emu - SLIDE_WIDTH_EMU * CONTENT_LEFT_RATIO) / content_width * 100
                info['y_percent'] = (y_emu - SLIDE_HEIGHT_EMU * CONTENT_TOP_RATIO) / content_height * 100
                info['cx_percent'] = cx_emu / content_width * 100
                info['cy_percent'] = cy_emu / content_height * 100

                # 원본 비율
                width_px = cx_emu / EMU_PER_INCH * PX_PER_INCH
                height_px = cy_emu / EMU_PER_INCH * PX_PER_INCH
                info['original_aspect_ratio'] = round(width_px / height_px if height_px > 0 else 1.0, 3)
                info['original_width_px'] = round(width_px, 1)
                info['original_height_px'] = round(height_px, 1)

        # 도형 타입
        if shape_elem.find('.//a:prstGeom', self.namespaces) is not None:
            geom = shape_elem.find('.//a:prstGeom', self.namespaces)
            info['geom_type'] = geom.get('prst', 'rect')

        # 텍스트 확인
        text_body = shape_elem.find('.//p:txBody', self.namespaces)
        info['has_text'] = text_body is not None

        # 폰트 크기
        if info['has_text']:
            rPr = shape_elem.find('.//a:rPr', self.namespaces)
            if rPr is not None:
                sz = rPr.get('sz')
                if sz:
                    # PowerPoint은 폰트 크기를 100분의 1 포인트로 저장
                    info['font_size_pt'] = int(sz) / 100

        # 채우기 색상
        fill = shape_elem.find('.//a:solidFill', self.namespaces)
        if fill is not None:
            srgbClr = fill.find('.//a:srgbClr', self.namespaces)
            if srgbClr is not None:
                info['fill_color'] = srgbClr.get('val')
            else:
                schemeClr = fill.find('.//a:schemeClr', self.namespaces)
                if schemeClr is not None:
                    info['fill_color'] = f"scheme_{schemeClr.get('val')}"

        return info

    def filter_content_zone(self, shapes):
        """타이틀/푸터 영역 제외하고 콘텐츠만 필터링"""
        content_shapes = []

        content_top_emu = SLIDE_HEIGHT_EMU * CONTENT_TOP_RATIO
        content_bottom_emu = SLIDE_HEIGHT_EMU * CONTENT_BOTTOM_RATIO

        for shape in shapes:
            if 'y_emu' not in shape or 'cy_emu' not in shape:
                continue

            shape_center_y = shape['y_emu'] + (shape['cy_emu'] / 2)

            if content_top_emu <= shape_center_y <= content_bottom_emu:
                content_shapes.append(shape)

        return content_shapes

    def extract_slide(self, slide_num):
        """슬라이드 전체 추출"""
        root = self.read_slide_xml(slide_num)

        spTree = root.find('.//p:spTree', self.namespaces)
        if spTree is None:
            return None

        shapes = []
        for sp in spTree.findall('.//p:sp', self.namespaces):
            shape_info = self.get_shape_info(sp)
            if shape_info:
                shapes.append(shape_info)

        # 콘텐츠 영역만 필터링
        content_shapes = self.filter_content_zone(shapes)

        return {
            'all_shapes': len(shapes),
            'content_shapes': len(content_shapes),
            'shapes': content_shapes
        }


def generate_template_yaml(slide_num, slide_data, output_dir):
    """템플릿 YAML 생성"""
    meta = SLIDES_INFO[slide_num]

    template = {
        'content_template': {
            'id': f"basic-{meta['design_intent']}",
            'name': meta['name'],
            'version': '2.0',
            'source': 'PPT기본양식_병합_수정(선별).pptx',
            'source_slide_index': slide_num,
            'extracted_at': datetime.now().isoformat()
        },
        'design_meta': {
            'quality_score': 8.5,
            'design_intent': meta['design_intent'],
            'visual_balance': 'symmetric' if meta['design_intent'].startswith('feature') or 'grid' in meta['design_intent'] else 'asymmetric',
            'information_density': 'high' if meta['category'] in ['stats', 'chart'] else 'medium'
        },
        'canvas': {
            'reference_width': 1920,
            'reference_height': 1080,
            'aspect_ratio': '16:9'
        },
        'shapes': [
            {
                'id': f"shape-{i}",
                'name': shape['name'],
                'type': 'rectangle' if shape.get('geom_type') == 'rect' else 'shape',
                'z_index': i,
                'geometry': {
                    'x': f"{shape['x_percent']:.1f}%",
                    'y': f"{shape['y_percent']:.1f}%",
                    'cx': f"{shape['cx_percent']:.1f}%",
                    'cy': f"{shape['cy_percent']:.1f}%",
                    'original_aspect_ratio': shape['original_aspect_ratio'],
                    'original_width_px': shape['original_width_px'],
                    'original_height_px': shape['original_height_px']
                },
                'style': {
                    'fill': {
                        'type': 'solid',
                        'color': shape.get('fill_color', 'surface')
                    }
                },
                'text': {
                    'has_text': shape['has_text'],
                    'font_size_pt': shape.get('font_size_pt', 18)
                }
            }
            for i, shape in enumerate(slide_data['shapes'][:8])  # 상위 8개만
        ],
        'use_for': get_use_for(meta['design_intent']),
        'keywords': get_keywords(meta['design_intent']),
        'thumbnail': f"thumbnails/basic-{meta['design_intent']}.png"
    }

    # 파일 저장
    category_dir = output_dir / meta['category']
    category_dir.mkdir(parents=True, exist_ok=True)

    filename = f"basic-{meta['design_intent']}.yaml"
    filepath = category_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(template, f,
                 default_flow_style=False,
                 allow_unicode=True,
                 sort_keys=False)

    return filepath


def get_use_for(design_intent):
    """use_for 자동 생성"""
    use_cases = {
        'feature-icons': [
            '제품 기능 소개',
            '서비스 특징 4가지 나열',
            '핵심 기능 강조',
            '아이콘 기반 정보 표현',
            '균형잡힌 레이아웃'
        ],
        'grid-image': [
            '포트폴리오 이미지 전시',
            '3x3 또는 3xN 갤러리',
            '사례 연구 시각화',
            '이미지 중심 콘텐츠',
            '균등 배치'
        ],
        'cycle-2circle': [
            '순환 프로세스 표현',
            '상호작용 관계도',
            '2단계 사이클',
            '피드백 루프',
            '연결 관계'
        ],
        'cycle-3circle': [
            '3단계 순환 프로세스',
            '순환 시스템 설명',
            '삼각형 관계도',
            '세 가지 요소 상호작용',
            '연속 프로세스'
        ],
        'process-4step': [
            '4단계 프로세스 흐름',
            '시간 순서 절차 표시',
            '단계별 진행 과정',
            '화살표 기반 흐름도',
            '순차적 업무'
        ],
        'comparison-rounded': [
            '두 가지 대안 비교',
            '제품 vs 제품 비교',
            '방식 A vs 방식 B',
            '특징 상호 비교',
            '선택지 제시'
        ],
        'stats-donut': [
            '비율 통계 시각화',
            '원형 차트 데이터',
            '점유율 표현',
            '통계 수치 표시',
            '도넛 그래프'
        ],
        'stats-cards': [
            '핵심 지표 카드 배치',
            'KPI 대시보드',
            '통계 수치 요약',
            '메트릭 카드 나열',
            '데이터 하이라이트'
        ],
        'comparison-highlight': [
            '대표 특징 강조 비교',
            '주요 포인트 선택 표시',
            '옵션별 비교',
            '강점 약점 표현',
            '시각적 강조'
        ],
        'content-quote': [
            '인용문 또는 명언 표시',
            '설명 및 부연 텍스트',
            '중요 메시지 전달',
            '톤앤매너 표현',
            '강조 콘텐츠'
        ]
    }
    return use_cases.get(design_intent, ['일반 콘텐츠'])


def get_keywords(design_intent):
    """keywords 자동 생성"""
    keywords = {
        'feature-icons': ['기능', '아이콘', '4열', '특징', '서비스', '제품', '소개'],
        'grid-image': ['그리드', '이미지', '갤러리', '3열', '포트폴리오', '레이아웃', '사례'],
        'cycle-2circle': ['순환', '사이클', '2단계', '피드백', '상호작용', '관계', '다이어그램'],
        'cycle-3circle': ['순환', '사이클', '3단계', '삼각형', '상호작용', '시스템', '프로세스'],
        'process-4step': ['프로세스', '흐름', '4단계', '화살표', '순차', '절차', '방법'],
        'comparison-rounded': ['비교', '대조', '선택', '라운드', '상대방', '특징', '차이'],
        'stats-donut': ['도넛', '차트', '통계', '비율', '점유율', '데이터', '시각화'],
        'stats-cards': ['카드', '통계', 'KPI', '지표', '메트릭', '데이터', '요약'],
        'comparison-highlight': ['비교', '강조', '하이라이트', '선택', '특징', '대비'],
        'content-quote': ['인용', '명언', '메시지', '텍스트', '설명', '강조', '톤앤매너']
    }
    return keywords.get(design_intent, ['일반', '콘텐츠'])


def main():
    unpacked_dir = Path("/home/jji/project/docs/workspace/unpacked")
    output_dir = Path("/home/jji/project/docs/templates/contents/templates")

    extractor = SlideExtractor(unpacked_dir)

    results = []

    # 슬라이드 20-29 (XML: slide21-slide30) 처리
    for slide_num in range(20, 30):
        xml_num = slide_num + 1  # XML은 1-based

        try:
            print(f"Processing slide {slide_num} (XML: slide{xml_num}.xml)...")

            slide_data = extractor.extract_slide(xml_num)
            if slide_data is None:
                print(f"  ERROR: Could not extract slide")
                continue

            print(f"  Found {slide_data['all_shapes']} shapes, {slide_data['content_shapes']} in content zone")

            filepath = generate_template_yaml(slide_num, slide_data, output_dir)
            print(f"  Generated: {filepath}")

            results.append({
                'slide': slide_num,
                'yaml': str(filepath),
                'shapes': slide_data['content_shapes']
            })

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    # 결과 요약
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    for r in results:
        print(f"Slide {r['slide']:2d}: {r['shapes']:2d} shapes -> {Path(r['yaml']).name}")
    print(f"\nTotal: {len(results)} slides processed")


if __name__ == '__main__':
    main()
