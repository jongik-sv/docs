#!/usr/bin/env python3
import os
import re
from pathlib import Path

slides_dir = Path(__file__).parent / 'slides'

def fix_html(content):
    # 1. Replace radial-gradient with solid color
    content = re.sub(
        r'background:\s*radial-gradient\([^)]+\)',
        'background: rgba(183,208,212,0.15); border-radius: 150pt',
        content
    )

    # 2. Replace linear-gradient with solid color
    content = re.sub(
        r'background:\s*linear-gradient\([^)]+\)',
        'background: rgba(183,208,212,0.1)',
        content
    )

    # 3. Fix footer divs: <div class="footer">N</div> -> <div class="footer"><p>N</p></div>
    content = re.sub(
        r'<div class="footer">(\d+)</div>',
        r'<div class="footer"><p>\1</p></div>',
        content
    )

    # 4. Fix spans in items divs to p tags
    content = re.sub(
        r'\.items span \{',
        '.items p {',
        content
    )
    content = re.sub(
        r'<span>([^<]+)</span>',
        r'<p>\1</p>',
        content
    )

    # 5. Fix divs with direct text (common patterns)
    patterns = [
        # Year label like <div class="year-label">2025</div>
        (r'<div class="year-label">([^<]+)</div>', r'<div class="year-label"><p>\1</p></div>'),
        # Phase bar like <div class="phase-bar">착수</div>
        (r'<div class="phase-bar">([^<]+)</div>', r'<div class="phase-bar"><p>\1</p></div>'),
        # Badge with text
        (r'<div class="([^"]*badge[^"]*)">([^<]+)</div>', r'<div class="\1"><p>\2</p></div>'),
        # Risk spans
        (r'<span class="risk-([^"]+)">([^<]+)</span>', r'<div class="risk-\1"><p>\2</p></div>'),
        # Card icon with symbols
        (r'<div class="card-icon">([^<]+)</div>', r'<div class="card-icon"><p>\1</p></div>'),
        # Item icon with symbols
        (r'<div class="item-icon[^"]*">([^<]+)</div>', r'<div class="item-icon"><p>\1</p></div>'),
        # Security icon
        (r'<div class="security-icon"><span>([^<]+)</span></div>', r'<div class="security-icon"><p>\1</p></div>'),
        # Layer label
        (r'<div class="layer-label">([^<]+)</div>', r'<div class="layer-label"><p>\1</p></div>'),
        # Legend dot text
        (r'<div class="legend-dot[^"]*"></div>([^<]+)', r'<div class="legend-dot"></div><p>\1</p>'),
        # Tech category
        (r'<div class="tech-category">([^<]+)</div>', r'<div class="tech-category"><p>\1</p></div>'),
        # Org role
        (r'<div class="org-role">([^<]+)</div>', r'<div class="org-role"><p>\1</p></div>'),
        # Center box text
        (r'<div class="center-box">([^<]+)</div>', r'<div class="center-box"><p>\1</p></div>'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # 6. Fix <p> with background -> wrap in div
    # This is complex, skip for now as it requires restructuring

    return content

for html_file in sorted(slides_dir.glob('*.html')):
    print(f'Processing: {html_file.name}')
    content = html_file.read_text(encoding='utf-8')
    fixed = fix_html(content)
    html_file.write_text(fixed, encoding='utf-8')

print('Done!')
