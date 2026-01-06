# Thumbnail Generation Workflow

PPT 슬라이드의 시각적 썸네일 그리드를 생성합니다.

## Usage

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

## Features

- 기본 출력: `thumbnails.jpg`
- 대용량 덱: `thumbnails-1.jpg`, `thumbnails-2.jpg`, ...
- 기본: 5열, 그리드당 최대 30 슬라이드 (5x6)

## Options

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--cols N` | 열 수 조정 (3-6) | `--cols 4` |
| `--slides N` | 특정 슬라이드만 (0-indexed) | `--slides 0,2,5` |
| `--single` | 개별 이미지로 저장 | `--single` |

## Grid Limits by Columns

| 열 수 | 그리드당 슬라이드 |
|-------|------------------|
| 3 | 12 |
| 4 | 20 |
| 5 | 30 |
| 6 | 42 |

## Examples

```bash
# 기본 사용
python scripts/thumbnail.py presentation.pptx

# 커스텀 이름, 4열
python scripts/thumbnail.py template.pptx analysis --cols 4

# 특정 폴더에 저장
python scripts/thumbnail.py template.pptx workspace/my-grid

# 특정 슬라이드만 (0-indexed)
python scripts/thumbnail.py input.pptx output/ --slides 0,2,5

# 개별 이미지로 저장
python scripts/thumbnail.py input.pptx output/ --slides 0,2,5 --single
```

## Use Cases

- **템플릿 분석**: 슬라이드 레이아웃, 디자인 패턴 파악
- **콘텐츠 리뷰**: 전체 프레젠테이션 시각적 개요
- **네비게이션 참조**: 시각적 외관으로 특정 슬라이드 찾기
- **품질 체크**: 모든 슬라이드 서식 확인
- **콘텐츠 추출**: 특정 슬라이드 썸네일 생성

## Note

슬라이드는 0-indexed입니다 (Slide 0, Slide 1, ...).
