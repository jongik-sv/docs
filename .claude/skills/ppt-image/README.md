# ppt-image

이미지/썸네일 생성 및 아이콘 처리를 담당하는 Claude Code 스킬.

## 개요

| 항목 | 값 |
|------|---|
| 스킬 타입 | Claude Code Skill |
| 버전 | 1.0 |
| 의존 스킬 | ppt-create (thumbnail.py 참조) |

## 워크플로우

### 1. thumbnail (썸네일 생성)

**트리거**: "썸네일 만들어줘", "PPT 미리보기 생성"

**처리 흐름**:
1. PPT 파일 열기
2. LibreOffice → PDF 변환
3. Poppler → 이미지 변환
4. 그리드 또는 개별 이미지 생성

**출력물**:
- 그리드 이미지 (`*_thumbnails.jpg`)
- 개별 슬라이드 이미지 (`slide_*.png`)

**옵션**:
- `--grid`: 그리드 형태로 출력 (기본)
- `--single`: 개별 슬라이드 이미지
- `--slides N`: 처음 N개 슬라이드만

---

## 스크립트

| 스크립트 | 줄수 | 역할 |
|---------|------|------|
| `image-prompt-generator.js` | 289 | AI 이미지 프롬프트 생성 |
| `rasterize-icon.js` | 168 | SVG → PNG 래스터화 |

**참조 스크립트** (ppt-create에서):
- `thumbnail.py` (777줄) - 썸네일 생성

---

## 이미지 프롬프트 생성

`image-prompt-generator.js`는 슬라이드 콘텐츠에 맞는 AI 이미지 생성 프롬프트를 작성합니다.

### 템플릿 (templates/assets/image-prompt-templates.yaml)

```yaml
templates:
  hero:
    base: "Professional, impactful hero image"
    modifiers: ["high contrast", "bold composition"]
    aspect_ratio: "16:9"

  background:
    base: "Subtle, elegant background pattern"
    modifiers: ["minimal", "soft gradients"]

  tech:
    base: "Modern technology visualization"
    modifiers: ["futuristic", "clean lines", "blue tones"]

industry_styles:
  tech: ["sleek", "innovative", "digital"]
  finance: ["professional", "trustworthy", "geometric"]
  healthcare: ["clean", "caring", "medical"]
```

### 사용 예시

```bash
node image-prompt-generator.js --type hero --industry tech --keywords "AI,클라우드"
```

**출력**:
```
Professional, impactful hero image for presentation.
Style: sleek, innovative, digital.
Keywords: AI, cloud computing, technology.
Aspect ratio: 16:9.
Negative: text, watermark, low quality.
```

---

## 아이콘 래스터화

`rasterize-icon.js`는 react-icons 라이브러리의 SVG 아이콘을 PNG로 변환합니다.

### 사용 예시

```bash
node rasterize-icon.js --icon "fa/FaBrain" --size 128 --color "#1E5128"
```

**출력**:
- `icons/FaBrain_128_1E5128.png`

### 지원 아이콘 라이브러리

- FontAwesome (`fa/`)
- Heroicons (`hi/`)
- Ant Design (`ai/`)
- Material Design (`md/`)
- Bootstrap Icons (`bs/`)

---

## 미구현 기능 (TODO)

### AI 이미지 생성 연동

MCP를 통한 AI 이미지 생성 서비스 연동:

| 서비스 | 상태 | 설명 |
|--------|------|------|
| DALL-E | ❌ 미구현 | OpenAI 이미지 생성 |
| Midjourney | ❌ 미구현 | Discord API 연동 |
| Stable Diffusion | ❌ 미구현 | 로컬/API 연동 |

**계획된 파이프라인**:
```
이미지 프롬프트 생성
         ↓
AI 이미지 서비스 호출 (MCP)
         ↓
이미지 다운로드
         ↓
PPT에 삽입
```

---

## 의존성

**Node.js**:
- sharp - 이미지 처리
- react-icons - 아이콘 라이브러리

**Python** (thumbnail.py):
- Pillow - 이미지 처리

**시스템**:
- LibreOffice (soffice) - PPTX → PDF
- Poppler (pdftoppm) - PDF → 이미지

---

## 사용 예시

```
사용자: "이 PPT 썸네일 만들어줘" [PPT 첨부]

Claude:
썸네일을 생성하겠습니다.

처리 중...
- PPTX → PDF 변환
- PDF → 이미지 변환
- 그리드 이미지 생성

완료!
파일: presentation_thumbnails.jpg
슬라이드: 10개
```
