#!/usr/bin/env python3
"""
PPTX Template Analyzer (3타입 구조 지원)

PPTX 파일을 분석하여 그룹 폴더 구조에 맞는 템플릿 파일들을 생성합니다.

Usage:
    python template-analyzer.py input.pptx 제안서1 --group dongkuk --name "제안서 (기본)"

Output:
    - templates/documents/{group}/config.yaml (없으면 생성)
    - templates/documents/{group}/{template-id}.yaml (양식 파일)
    - templates/documents/{group}/registry.yaml (자동 업데이트)

Examples:
    # 새 그룹에 첫 템플릿 등록
    python template-analyzer.py proposal.pptx 제안서1 --group dongkuk --name "제안서 (기본)"

    # 기존 그룹에 템플릿 추가
    python template-analyzer.py report.pptx 보고서1 --group dongkuk --name "보고서 (기본)" --type report
"""

import argparse
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import re
import yaml


# OOXML 네임스페이스
NAMESPACES = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def extract_theme(pptx_path: str) -> dict:
    """theme1.xml에서 색상, 폰트 추출"""
    theme = {
        'name': '',
        'colors': {},
        'fonts': {}
    }

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # theme1.xml 찾기
        theme_files = [f for f in zf.namelist() if 'theme' in f and f.endswith('.xml')]
        if not theme_files:
            return theme

        theme_file = theme_files[0]
        with zf.open(theme_file) as f:
            tree = ET.parse(f)
            root = tree.getroot()

            # 테마 이름
            theme_elem = root.find('.//a:theme', NAMESPACES)
            if theme_elem is not None:
                theme['name'] = theme_elem.get('name', '')

            # 색상 스키마
            clr_scheme = root.find('.//a:clrScheme', NAMESPACES)
            if clr_scheme is not None:
                color_mapping = {
                    'dk1': 'dark_text',
                    'lt1': 'light_bg',
                    'dk2': 'primary',
                    'lt2': 'gray',
                    'accent1': 'accent1',
                    'accent2': 'accent2',
                    'accent3': 'accent3',
                    'accent4': 'secondary',
                    'accent5': 'accent5',
                    'accent6': 'accent6',
                }

                for color_name, field_name in color_mapping.items():
                    color_elem = clr_scheme.find(f'a:{color_name}', NAMESPACES)
                    if color_elem is not None:
                        # srgbClr 또는 sysClr에서 색상 추출
                        srgb = color_elem.find('.//a:srgbClr', NAMESPACES)
                        if srgb is not None:
                            theme['colors'][field_name] = f"#{srgb.get('val', '')}"
                        else:
                            sys_clr = color_elem.find('.//a:sysClr', NAMESPACES)
                            if sys_clr is not None:
                                theme['colors'][field_name] = f"#{sys_clr.get('lastClr', '')}"

            # 폰트 스키마
            font_scheme = root.find('.//a:fontScheme', NAMESPACES)
            if font_scheme is not None:
                # 주요 폰트 (제목용)
                major_font = font_scheme.find('.//a:majorFont/a:latin', NAMESPACES)
                if major_font is not None:
                    theme['fonts']['title'] = major_font.get('typeface', '')

                # 보조 폰트 (본문용)
                minor_font = font_scheme.find('.//a:minorFont/a:latin', NAMESPACES)
                if minor_font is not None:
                    theme['fonts']['body'] = minor_font.get('typeface', '')

    return theme


def get_slide_count(pptx_path: str) -> int:
    """슬라이드 개수 반환"""
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_files = [f for f in zf.namelist() if re.match(r'ppt/slides/slide\d+\.xml', f)]
        return len(slide_files)


def analyze_slide(pptx_path: str, slide_num: int) -> dict:
    """개별 슬라이드 분석"""
    slide_info = {
        'index': slide_num,
        'placeholders': [],
        'has_title': False,
        'has_body': False,
        'text_count': 0,
        'image_count': 0,
    }

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        slide_file = f'ppt/slides/slide{slide_num + 1}.xml'
        if slide_file not in zf.namelist():
            return slide_info

        with zf.open(slide_file) as f:
            tree = ET.parse(f)
            root = tree.getroot()

            # 플레이스홀더 분석
            shapes = root.findall('.//p:sp', NAMESPACES)
            for shape in shapes:
                ph = shape.find('.//p:ph', NAMESPACES)
                if ph is not None:
                    ph_type = ph.get('type', 'body')
                    ph_idx = ph.get('idx', '')

                    placeholder = {
                        'type': ph_type,
                        'idx': ph_idx if ph_idx else None,
                    }

                    # 텍스트 내용 확인
                    text_body = shape.find('.//p:txBody', NAMESPACES)
                    if text_body is not None:
                        texts = text_body.findall('.//a:t', NAMESPACES)
                        text_content = ' '.join([t.text or '' for t in texts]).strip()
                        if text_content:
                            placeholder['sample_text'] = text_content[:50]

                    slide_info['placeholders'].append(placeholder)

                    if ph_type in ['title', 'ctrTitle']:
                        slide_info['has_title'] = True
                    elif ph_type == 'body':
                        slide_info['has_body'] = True

                # 텍스트 카운트
                if shape.find('.//a:t', NAMESPACES) is not None:
                    slide_info['text_count'] += 1

            # 이미지 카운트
            pics = root.findall('.//p:pic', NAMESPACES)
            slide_info['image_count'] = len(pics)

    return slide_info


def classify_layout(slide_info: dict, slide_num: int, total_slides: int) -> str:
    """슬라이드 레이아웃 카테고리 분류"""
    has_title = slide_info['has_title']
    has_body = slide_info['has_body']
    ph_types = [p['type'] for p in slide_info['placeholders']]

    # 첫 슬라이드 = 표지
    if slide_num == 0:
        return 'cover'

    # 목차 감지: 번호+텍스트 패턴
    sample_texts = [p.get('sample_text', '') for p in slide_info['placeholders']]
    toc_patterns = ['01', '02', '목차', 'Contents', 'Index']
    if any(pattern in ' '.join(sample_texts) for pattern in toc_patterns):
        return 'toc'

    # 섹션 구분: 제목만 있고 본문 없음, 이미지도 없음
    if has_title and not has_body and slide_info['image_count'] == 0 and slide_info['text_count'] <= 2:
        return 'section'

    # 본문+불릿
    if has_body:
        return 'content_bullets'

    # 자유 영역: 제목만, 넓은 빈 공간
    if has_title and not has_body:
        return 'content_free'

    # 기본값
    return 'content_wide'


def get_use_for(category: str) -> str:
    """카테고리별 use_for 설명"""
    use_for_map = {
        'cover': '문서 제목, 발표 표지, 작성자 정보',
        'toc': '목차, Contents, 챕터 구성, 페이지 안내',
        'section': '섹션 구분, 챕터 시작',
        'content_bullets': '설명, 개요, 리스트 나열, 본문 슬라이드',
        'content_free': '차트, 표, 다이어그램, 이미지, 자유 레이아웃',
        'content_wide': '긴 텍스트, 단순 정보, Action Title 불필요한 콘텐츠',
    }
    return use_for_map.get(category, '일반 콘텐츠')


def get_keywords(category: str) -> list:
    """카테고리별 키워드"""
    keywords_map = {
        'cover': ['표지', '제목', '타이틀', '커버', '시작'],
        'toc': ['목차', 'Contents', '인덱스', '구성'],
        'section': ['섹션', '챕터', '구분'],
        'content_bullets': ['설명', '개요', '리스트', '본문', '내용', '불릿'],
        'content_free': ['차트', '표', '그래프', '다이어그램', '이미지', '시각화'],
        'content_wide': ['텍스트', '정보', '단순', '설명문', '긴글'],
    }
    return keywords_map.get(category, ['콘텐츠'])


def analyze_layouts(pptx_path: str) -> list:
    """모든 슬라이드 레이아웃 분석"""
    layouts = []
    slide_count = get_slide_count(pptx_path)

    for i in range(slide_count):
        slide_info = analyze_slide(pptx_path, i)
        category = classify_layout(slide_info, i, slide_count)

        layout = {
            'index': i,
            'category': category,
            'use_for': get_use_for(category),
            'keywords': get_keywords(category),
            'placeholders': []
        }

        for ph in slide_info['placeholders']:
            placeholder = {
                'type': ph['type'],
            }
            if ph.get('idx'):
                placeholder['idx'] = int(ph['idx']) if ph['idx'].isdigit() else ph['idx']
            layouts[-1]['placeholders'].append(placeholder) if layouts else None

        layout['placeholders'] = [
            {'type': p['type'], 'idx': int(p['idx']) if p.get('idx') and str(p['idx']).isdigit() else p.get('idx')}
            for p in slide_info['placeholders']
        ]

        layouts.append(layout)

    return layouts


def get_slide_size(pptx_path: str) -> dict:
    """슬라이드 크기 추출"""
    size = {'width_emu': 9144000, 'height_emu': 6858000}  # 기본값 (4:3)

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        pres_file = 'ppt/presentation.xml'
        if pres_file in zf.namelist():
            with zf.open(pres_file) as f:
                tree = ET.parse(f)
                root = tree.getroot()

                sld_sz = root.find('.//p:sldSz', NAMESPACES)
                if sld_sz is not None:
                    size['width_emu'] = int(sld_sz.get('cx', 9144000))
                    size['height_emu'] = int(sld_sz.get('cy', 6858000))

    return size


def calculate_aspect_ratio(width: int, height: int) -> str:
    """종횡비 계산"""
    ratio = width / height
    if abs(ratio - 16/9) < 0.01:
        return '16:9'
    elif abs(ratio - 4/3) < 0.01:
        return '4:3'
    elif abs(ratio - 16/10) < 0.01:
        return '16:10'
    else:
        return f'{width}:{height}'


def ensure_group_folder(base_dir: Path, group_id: str) -> Path:
    """그룹 폴더 구조 생성"""
    group_dir = base_dir / group_id
    assets_dir = group_dir / 'assets' / 'default'

    group_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    return group_dir


def load_or_create_config(group_dir: Path, group_id: str, theme: dict) -> dict:
    """config.yaml 로드 또는 생성"""
    config_path = group_dir / 'config.yaml'

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    # 새 config 생성
    config = {
        'group': {
            'id': group_id,
            'name': group_id,  # 사용자가 나중에 수정
        },
        'theme': {
            'colors': theme.get('colors', {}),
            'fonts': theme.get('fonts', {}),
        },
        'companies': [
            {'id': 'default', 'name': f'{group_id} (기본)'}
        ]
    }

    # 저장
    yaml_str = f"""# {group_id} 그룹 설정
# 자동 생성: {datetime.now().strftime('%Y-%m-%d')}

"""
    yaml_str += yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False)

    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(yaml_str)

    print(f"  config.yaml 생성: {config_path}")
    return config


def update_registry(group_dir: Path, template_id: str, name: str,
                    template_type: str, description: str) -> None:
    """registry.yaml 업데이트"""
    registry_path = group_dir / 'registry.yaml'

    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f) or {}
    else:
        registry = {'templates': []}

    # 기존 템플릿 확인
    templates = registry.get('templates', [])
    existing_ids = [t['id'] for t in templates]

    if template_id in existing_ids:
        # 업데이트
        for t in templates:
            if t['id'] == template_id:
                t['name'] = name
                t['type'] = template_type
                t['description'] = description
                t['updated'] = datetime.now().strftime('%Y-%m-%d')
        print(f"  registry.yaml 업데이트: {template_id}")
    else:
        # 추가
        templates.append({
            'id': template_id,
            'name': name,
            'file': f'{template_id}.yaml',
            'type': template_type,
            'description': description,
            'created': datetime.now().strftime('%Y-%m-%d'),
        })
        print(f"  registry.yaml 추가: {template_id}")

    registry['templates'] = templates

    # 저장
    yaml_str = f"""# 문서 템플릿 레지스트리
# 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}

"""
    yaml_str += yaml.dump(registry, allow_unicode=True, default_flow_style=False, sort_keys=False)

    with open(registry_path, 'w', encoding='utf-8') as f:
        f.write(yaml_str)


def generate_document_yaml(template_id: str, name: str, source: str,
                           layouts: list, slide_size: dict) -> str:
    """문서 템플릿 YAML 생성 (양식 파일)"""
    aspect_ratio = calculate_aspect_ratio(slide_size['width_emu'], slide_size['height_emu'])

    # 슬라이드 구조 생성
    slides = []
    for layout in layouts:
        slide = {
            'index': layout['index'],
            'category': layout['category'],
            'use_for': layout['use_for'],
        }
        if layout.get('placeholders'):
            slide['placeholders'] = layout['placeholders']
        slides.append(slide)

    data = {
        'document': {
            'id': template_id,
            'name': name,
            'source': source,
            'aspect_ratio': aspect_ratio,
            'slide_size': slide_size,
        },
        'slides': slides,
        'selection_guide': {
            'cover': 0,
            'toc': next((l['index'] for l in layouts if l['category'] == 'toc'), 1),
            'bullets': next((l['index'] for l in layouts if l['category'] == 'content_bullets'), 2),
            'chart': next((l['index'] for l in layouts if l['category'] == 'content_free'), 3),
        },
        'best_practices': [
            '슬라이드당 핵심 메시지 1개',
            '연속 3장 이상 동일 레이아웃 금지',
            '불릿은 최대 4개 권장',
        ]
    }

    yaml_str = f"""# {name}
# 자동 생성: {datetime.now().strftime('%Y-%m-%d %H:%M')}
# 원본: {source}

"""
    yaml_str += yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    return yaml_str


def main():
    parser = argparse.ArgumentParser(
        description='PPTX 템플릿 분석기 (3타입 구조)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python template-analyzer.py proposal.pptx 제안서1 --group dongkuk
  python template-analyzer.py report.pptx 보고서1 --group dongkuk --type report
        """
    )
    parser.add_argument('pptx_path', help='입력 PPTX 파일 경로')
    parser.add_argument('template_id', help='템플릿 ID (예: 제안서1, 보고서1)')
    parser.add_argument('--group', required=True, help='그룹 ID (예: dongkuk)')
    parser.add_argument('--name', help='템플릿 표시 이름', default=None)
    parser.add_argument('--type', dest='template_type', default='general',
                        choices=['proposal', 'report', 'plan', 'general'],
                        help='템플릿 타입 (proposal, report, plan, general)')
    parser.add_argument('--base-dir', default='templates/documents/',
                        help='기본 출력 디렉토리')
    parser.add_argument('--description', help='템플릿 설명', default=None)

    args = parser.parse_args()

    pptx_path = args.pptx_path
    template_id = args.template_id
    group_id = args.group
    name = args.name or template_id
    template_type = args.template_type
    base_dir = Path(args.base_dir)

    print(f"PPTX 템플릿 분석기")
    print(f"=" * 40)
    print(f"입력: {pptx_path}")
    print(f"그룹: {group_id}")
    print(f"템플릿: {template_id}")
    print()

    # 1. 그룹 폴더 생성
    print("[1/5] 그룹 폴더 확인...")
    group_dir = ensure_group_folder(base_dir, group_id)
    print(f"  폴더: {group_dir}")

    # 2. PPTX 분석
    print("\n[2/5] PPTX 분석...")
    theme = extract_theme(pptx_path)
    print(f"  테마: {theme.get('name', 'Unknown')}")
    print(f"  색상: {len(theme.get('colors', {}))}개")
    print(f"  폰트: {theme.get('fonts', {})}")

    layouts = analyze_layouts(pptx_path)
    print(f"  슬라이드: {len(layouts)}개")
    for layout in layouts:
        print(f"    [{layout['index']}] {layout['category']}")

    slide_size = get_slide_size(pptx_path)
    aspect_ratio = calculate_aspect_ratio(slide_size['width_emu'], slide_size['height_emu'])
    print(f"  종횡비: {aspect_ratio}")

    # 3. config.yaml 처리
    print("\n[3/5] config.yaml 처리...")
    load_or_create_config(group_dir, group_id, theme)

    # 4. 양식.yaml 생성
    print("\n[4/5] 양식 파일 생성...")
    yaml_content = generate_document_yaml(
        template_id, name, pptx_path, layouts, slide_size
    )
    template_path = group_dir / f"{template_id}.yaml"
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print(f"  저장: {template_path}")

    # 5. registry.yaml 업데이트
    print("\n[5/5] registry.yaml 업데이트...")
    description = args.description or f"{name} 문서 템플릿"
    update_registry(group_dir, template_id, name, template_type, description)

    print("\n" + "=" * 40)
    print("완료!")
    print(f"  그룹 폴더: {group_dir}")
    print(f"  템플릿: {template_path}")


if __name__ == '__main__':
    main()
