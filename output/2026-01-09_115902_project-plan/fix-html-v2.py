#!/usr/bin/env python3
"""HTML 슬라이드 수정 스크립트 v2
- Footer에 작성자 정보 추가
- 로고 추가 (내지 슬라이드)
- 검증 오류 수정
"""
import re
from pathlib import Path

slides_dir = Path(__file__).parent / 'slides'

# 섹션 슬라이드 (로고 제외)
SECTION_SLIDES = {'slide-001', 'slide-003', 'slide-008', 'slide-012', 'slide-015', 'slide-018', 'slide-022'}

def fix_html(content, filename):
    slide_id = filename.replace('.html', '')
    is_section = any(slide_id.startswith(s) for s in SECTION_SLIDES)

    # 1. Footer 스타일 추가/수정
    footer_style = '''
    .footer-wrap { position: absolute; bottom: 15pt; right: 30pt; display: flex; align-items: center; gap: 20pt; }
    .footer-info { font-size: 9pt; color: #B6B6B6; }
    .footer-page { font-size: 9pt; color: #B6B6B6; }
    .logo-img { height: 18pt; opacity: 0.7; }'''

    # 기존 footer 스타일 제거하고 새 스타일 추가
    content = re.sub(r'\.footer \{[^}]+\}', '', content)
    content = re.sub(r'(</style>)', footer_style + r'\n  \1', content)

    # 2. Footer HTML 수정
    # 페이지 번호 추출
    match = re.search(r'<div class="footer"><p>(\d+)</p></div>', content)
    if match:
        page_num = match.group(1)
        if is_section:
            # 섹션 슬라이드: 페이지 번호만
            new_footer = f'''<div class="footer-wrap">
    <p class="footer-page">{page_num}</p>
  </div>'''
        else:
            # 내지 슬라이드: 로고 + 작성자 + 페이지 번호
            new_footer = f'''<div class="footer-wrap">
    <img class="logo-img" src="../../../templates/documents/dongkuk-systems/assets/default/image2.png" alt="logo" />
    <p class="footer-info">작성_테크솔루션</p>
    <p class="footer-page">{page_num}</p>
  </div>'''
        content = re.sub(r'<div class="footer"><p>\d+</p></div>', new_footer, content)

    # 3. 추가 검증 오류 수정

    # 3-1. <p class="xxx-badge"> 배경 수정 -> div wrapper
    # 배경이 있는 p 태그를 div로 감싸기
    badge_pattern = r'<p class="([^"]*badge[^"]*)"[^>]*>([^<]+)</p>'
    def replace_badge(m):
        cls = m.group(1)
        text = m.group(2)
        return f'<div class="{cls}-wrap"><p class="{cls}">{text}</p></div>'
    content = re.sub(badge_pattern, replace_badge, content)

    # 3-2. milestone-output 수정 (p에 배경 있음)
    content = re.sub(
        r'<p class="milestone-output">([^<]+)</p>',
        r'<div class="milestone-output-wrap"><p class="milestone-output-text">\1</p></div>',
        content
    )

    # 3-3. 특수문자만 있는 div 수정
    special_chars = ['!', '✓', '+', '→', '●', '○', '◆', '★', '⚙', '✔', '✕']
    for char in special_chars:
        pattern = rf'<div class="([^"]+)">{re.escape(char)}</div>'
        content = re.sub(pattern, rf'<div class="\1"><p>{char}</p></div>', content)

    # HTML 엔티티도 처리
    entities = ['&#10003;', '&#9881;', '&#9733;', '&#128274;', '&#128272;', '&#128737;', '&#128270;', '&#128196;']
    for ent in entities:
        pattern = rf'<div class="([^"]+)">{re.escape(ent)}</div>'
        content = re.sub(pattern, rf'<div class="\1"><p>{ent}</p></div>', content)

    # 3-4. 중앙 영역의 텍스트 div 수정 (Agile-Waterfall 등)
    content = re.sub(
        r'<div class="method-center">([^<]+)</div>',
        r'<div class="method-center"><p>\1</p></div>',
        content
    )

    return content

def fix_slide_022(content):
    """slide-022 overflow 수정"""
    # bg-circle 크기 줄이기
    content = re.sub(
        r'\.bg-circle1 \{[^}]*width: 350pt; height: 350pt;[^}]*\}',
        '.bg-circle1 { position: absolute; top: -50pt; right: -50pt; width: 200pt; height: 200pt; background: rgba(75,101,128,0.3); border-radius: 100pt; }',
        content
    )
    content = re.sub(
        r'\.bg-circle2 \{[^}]*width: 250pt; height: 250pt;[^}]*\}',
        '.bg-circle2 { position: absolute; bottom: -40pt; left: -40pt; width: 150pt; height: 150pt; background: rgba(183,208,212,0.2); border-radius: 75pt; }',
        content
    )
    return content

for html_file in sorted(slides_dir.glob('*.html')):
    print(f'Processing: {html_file.name}')
    content = html_file.read_text(encoding='utf-8')
    content = fix_html(content, html_file.name)

    if 'slide-022' in html_file.name:
        content = fix_slide_022(content)

    html_file.write_text(content, encoding='utf-8')

print('Done!')
