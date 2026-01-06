# HTML to PowerPoint Workflow

템플릿 없이 새 PPT를 생성합니다. HTML을 PowerPoint로 변환합니다.

## Triggers

- "PPT 만들어줘"
- "프레젠테이션 생성해줘"
- "슬라이드 만들어줘"

## Design Principles

**CRITICAL**: PPT 생성 전 디자인 분석 필수:

1. **주제 고려**: 프레젠테이션 주제, 톤, 분위기
2. **브랜딩 확인**: 회사/조직 언급 시 브랜드 색상 고려
3. **팔레트 매칭**: 주제에 맞는 색상 선택
4. **접근법 설명**: 코드 작성 전 디자인 선택 설명

### Requirements

- 코드 작성 전 디자인 접근법 설명
- 웹 안전 폰트만 사용: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- 명확한 시각적 계층 구조
- 가독성 보장: 충분한 대비, 적절한 텍스트 크기
- 일관성 유지: 패턴, 간격, 시각 언어 반복

### Color Palette Selection

**창의적 색상 선택**:
- 기본값을 넘어 생각하기
- 다양한 각도 고려: 주제, 산업, 분위기, 타겟 오디언스
- 3-5개 색상 구성 (주색 + 보조색 + 강조색)
- 대비 확보: 배경과 텍스트 가독성

**예시 팔레트** (참고용):

| 이름 | 색상 |
|------|------|
| Classic Blue | #1C2833, #2E4053, #AAB7B8, #F4F6F6 |
| Teal & Coral | #5EA8A7, #277884, #FE4447, #FFFFFF |
| Warm Blush | #A49393, #EED6D3, #E8B4B8, #FAF7F2 |
| Black & Gold | #BF9A4A, #000000, #F4F6F6 |
| Forest Green | #191A19, #4E9F3D, #1E5128, #FFFFFF |

## Workflow

### 1. MANDATORY - Read Full Guide

**반드시** 상세 가이드 전체를 읽으세요:

```
Read .claude/skills/ppt-gen/html2pptx.md (전체 파일)
```

이 가이드에는 다음이 포함됩니다:
- HTML 슬라이드 생성 규칙
- html2pptx.js 라이브러리 사용법
- PptxGenJS API (차트, 테이블, 이미지)
- 색상 규칙 (# 제외)

### 2. Create HTML Slides

각 슬라이드별 HTML 파일 생성:
- 16:9: `width: 720pt; height: 405pt`
- 텍스트는 반드시 `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` 태그 내
- `class="placeholder"`: 차트/테이블 영역
- 그라디언트/아이콘은 PNG로 먼저 래스터라이즈

### 3. Convert to PowerPoint

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';

const { slide, placeholders } = await html2pptx('slide1.html', pptx);

// 차트 추가 (placeholder 영역에)
if (placeholders.length > 0) {
    slide.addChart(pptx.charts.BAR, chartData, placeholders[0]);
}

await pptx.writeFile('output.pptx');
```

### 4. Visual Validation

```bash
python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4
```

썸네일 이미지 검토:
- **텍스트 잘림**: 헤더, 도형, 슬라이드 가장자리에 의한 잘림
- **텍스트 겹침**: 다른 텍스트나 도형과 겹침
- **위치 문제**: 슬라이드 경계나 다른 요소와 너무 가까움
- **대비 문제**: 배경과 텍스트 대비 부족

문제 발견 시 HTML 수정 후 재생성.

## Layout Tips

차트/테이블 포함 슬라이드:
- **2열 레이아웃 (권장)**: 전체 너비 헤더 + 아래 2열 (텍스트 | 차트)
- **전체 슬라이드 레이아웃**: 차트/테이블이 슬라이드 전체 차지
- **절대 세로 스택 금지**: 텍스트 아래 차트/테이블 배치 금지

## Visual Design Options

### Geometric Patterns
- 대각선 섹션 구분선
- 비대칭 열 너비 (30/70, 40/60)
- 90도/270도 회전 텍스트 헤더
- 원형/육각형 이미지 프레임

### Border Treatments
- 한쪽 면만 두꺼운 테두리 (10-20pt)
- 코너 브라켓
- 헤더 밑줄 강조 (3-5pt)

### Typography
- 극단적 크기 대비 (72pt 헤드라인 vs 11pt 본문)
- 대문자 헤더 + 넓은 자간
- Courier New: 데이터/기술 콘텐츠

## Dependencies

이미 설치된 라이브러리:
- pptxgenjs, playwright, sharp
- react-icons, react, react-dom
