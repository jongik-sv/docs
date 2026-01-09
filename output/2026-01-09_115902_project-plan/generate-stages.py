#!/usr/bin/env python3
"""Stage 4, 5 JSON 생성 스크립트"""
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).parent
stage3 = json.loads((base_dir / 'stage-3-matching.json').read_text())

# HTML 파일 매핑
html_files = [
    'slide-001-cover.html',
    'slide-002-toc.html',
    'slide-003-section1.html',
    'slide-004-info.html',
    'slide-005-background.html',
    'slide-006-effects.html',
    'slide-007-scope.html',
    'slide-008-section2.html',
    'slide-009-strategy.html',
    'slide-010-methodology.html',
    'slide-011-tech.html',
    'slide-012-section3.html',
    'slide-013-org.html',
    'slide-014-team.html',
    'slide-015-section4.html',
    'slide-016-schedule.html',
    'slide-017-milestone.html',
    'slide-018-section5.html',
    'slide-019-quality.html',
    'slide-020-security.html',
    'slide-021-risk.html',
    'slide-022-closing.html',
]

# Stage 4: Content
stage4 = stage3.copy()
stage4['current_stage'] = 4
stage4['slides'] = []

for i, slide in enumerate(stage3['slides']):
    new_slide = slide.copy()
    new_slide['html_file'] = f'slides/{html_files[i]}'
    new_slide['assets'] = {'logo': 'templates/documents/dongkuk-systems/assets/default/image2.png'}
    new_slide['content_bindings'] = {}
    stage4['slides'].append(new_slide)

(base_dir / 'stage-4-content.json').write_text(
    json.dumps(stage4, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print('Created: stage-4-content.json')

# Stage 5: Generation
stage5 = stage4.copy()
stage5['current_stage'] = 5
stage5['session'] = stage4['session'].copy()
stage5['session']['status'] = 'completed'
stage5['slides'] = []

for i, slide in enumerate(stage4['slides']):
    new_slide = slide.copy()
    new_slide['generated'] = True
    new_slide['pptx_slide_index'] = i
    stage5['slides'].append(new_slide)

stage5['output'] = {
    'pptx_file': '스마트물류관리시스템_수행계획서.pptx',
    'generated_at': datetime.now().isoformat(),
    'slide_count': len(stage5['slides'])
}

(base_dir / 'stage-5-generation.json').write_text(
    json.dumps(stage5, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
print('Created: stage-5-generation.json')

print('Done!')
