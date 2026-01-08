# ppt-create

PPT 생성 및 수정을 담당하는 핵심 Claude Code 스킬.
공유 유틸리티(thumbnail.py, ooxml/)를 포함하여 다른 스킬에서 참조할 수 있음.

## 개요

| 항목 | 값 |
|------|---|
| 스킬 타입 | Claude Code Skill |
| 버전 | 1.0 |
| 역할 | PPT 생성 + 공유 유틸리티 제공 |

## 워크플로우

### 1. html2pptx (새 PPT 생성)

**트리거**: "PPT 만들어줘", "프레젠테이션 생성해줘"

**처리 흐름 (v4.0 동적 오브젝트 선택)**:
1. 콘텐츠 분석 → 슬라이드 구조 설계
2. 테마 선택 (deepgreen, brandnew, default)
3. **Template Priority Rule 적용**:
   - registry.yaml 검색
   - 매칭 결과 테이블 생성 (필수)
   - 템플릿 YAML 로드
4. **동적 오브젝트 선택** (v4.0 신규):
   - zones[] 순회
   - `object_hint` 있으면 objects/registry.yaml 검색
   - 최적 오브젝트 선택 또는 `object_default` 사용
   - `object_desc`만 있으면 설명 기반 렌더링
5. HTML 슬라이드 생성 (720×405px)
6. html2pptx.js 실행
7. 썸네일 검증

**동적 오브젝트 선택 흐름**:
```
콘텐츠 템플릿 로드
     ↓
zones[] 순회
     │
     ├─ object_hint 있음?
     │       ↓ YES
     │   objects/registry.yaml 검색
     │       │
     │       ├─ 매칭 성공 → 선택된 오브젝트 사용
     │       └─ 매칭 실패 → object_default 폴백
     │
     ├─ object_default만 있음?
     │       ↓ YES
     │   기본 오브젝트 사용
     │
     └─ object_desc만 있음?
             ↓ YES
         LLM이 설명 기반 렌더링
     ↓
오브젝트 렌더링
     │
     ├─ type: ooxml → OOXML 직접 삽입
     ├─ type: svg → SVG 변환 후 삽입
     ├─ type: image → 이미지 삽입
     └─ type: description → 설명 기반 렌더링
     ↓
HTML/PPTX 생성
```

**출력물**:
- `*.pptx` 파일

---

### 2. template (템플릿 기반 생성)

**트리거**: "동국제강 양식으로", "템플릿으로 PPT 만들어줘"

**처리 흐름**:
1. 문서 템플릿 로드 (`documents/{group}/`)
2. config.yaml → 테마 적용
3. 슬라이드 카테고리 매핑
4. rearrange.py → 슬라이드 구성
5. inventory.py → 텍스트 추출
6. replace.py → 텍스트 교체

**출력물**:
- `*.pptx` 파일 (브랜드 적용)

---

### 3. ooxml (기존 PPT 수정)

**트리거**: "이 PPT 수정해줘", "슬라이드 내용 바꿔줘"

**처리 흐름**:
1. unpack.py → PPTX 언팩
2. XML 파일 직접 편집
3. validate.py → 검증
4. pack.py → PPTX 리팩

**출력물**:
- 수정된 `*.pptx` 파일

---

## 스크립트

### 핵심 스크립트

| 스크립트 | 줄수 | 역할 |
|---------|------|------|
| `html2pptx.js` | 1,065 | HTML → PPTX 변환 |
| `inventory.py` | 1,020 | 텍스트 추출 |
| `replace.py` | 385 | 텍스트 교체 |
| `rearrange.py` | 231 | 슬라이드 재배열 |
| `migrate-templates.py` | 157 | 템플릿 마이그레이션 |

### 공유 유틸리티 (다른 스킬에서 참조)

| 스크립트 | 줄수 | 역할 | 사용 스킬 |
|---------|------|------|----------|
| `thumbnail.py` | 777 | 썸네일 생성 | ppt-extract, ppt-image |

### OOXML 리소스

```
ooxml/
├── scripts/
│   ├── unpack.py     # PPTX → ZIP 언팩
│   ├── pack.py       # ZIP → PPTX 리팩
│   └── validate.py   # XML 검증
└── schemas/
    └── ISO-IEC29500-4_2016/  # 공식 XSD 스키마
```

---

## Template Priority Rule (필수)

PPT 생성 시 반드시 따라야 하는 프로세스:

```
1. 슬라이드 목록 작성
   └─ 콘텐츠 분석 → 슬라이드 유형/키워드 정리

2. registry.yaml 검색
   └─ 각 슬라이드별 매칭 템플릿 찾기

3. 매칭 결과 테이블 작성 (필수 출력물)
   ┌─────────┬──────────────┬─────────────────┐
   │ 슬라이드 │ 콘텐츠 유형   │ 매칭 템플릿      │
   ├─────────┼──────────────┼─────────────────┤
   │ 1       │ 표지         │ cover-centered1 │
   │ 2       │ 목차         │ toc-3col1       │
   │ 3       │ A vs B       │ comparison-2col1│
   └─────────┴──────────────┴─────────────────┘

4. 템플릿 YAML 로드
   └─ 매칭된 템플릿의 shapes[] 구조 참조

5. HTML 생성
   └─ 템플릿 geometry/style → HTML 변환
```

**금지**: registry.yaml 검색 없이 직접 디자인 (매칭 불가 시에만 허용)

---

## 디자인 토큰

콘텐츠 템플릿에서 사용하는 디자인 토큰:

| 토큰 | 용도 | 테마 적용 |
|------|------|----------|
| `primary` | 주요 강조색 | colors.primary |
| `secondary` | 보조 강조색 | colors.secondary |
| `accent` | 하이라이트 | colors.accent |
| `background` | 배경색 | colors.background |
| `surface` | 카드 배경 | colors.surface |
| `dark_text` | 본문 텍스트 | colors.dark_text |
| `light` | 밝은 텍스트 | colors.light |
| `gray` | 음소거 요소 | colors.gray |

---

## 참조 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| HTML 요소 | `references/custom-elements.md` | 지원 HTML 태그/CSS |
| 콘텐츠 스키마 | `references/content-schema.md` | 템플릿 YAML v3.0 스키마 |

---

## 의존성

**Node.js**:
- pptxgenjs - PPTX 생성
- playwright - HTML 렌더링
- sharp - 이미지 처리

**Python**:
- python-pptx - PPTX 편집
- pyyaml - YAML 파싱
- defusedxml - XML 파싱
- Pillow - 이미지 처리

**시스템**:
- LibreOffice (soffice) - PPTX → PDF 변환
- Poppler (pdftoppm) - PDF → 이미지 변환

---

## 사용 예시

```
사용자: "스마트 물류 시스템 제안서 PPT 만들어줘"

Claude:
콘텐츠를 분석하고 템플릿을 매칭하겠습니다.

매칭 결과:
| 슬라이드 | 콘텐츠 | 템플릿 |
|---------|--------|--------|
| 1 | 표지 | cover-centered1 |
| 2 | 문제점 분석 | comparison-2col1 |
| 3 | 솔루션 | feature-center-icon1 |
| 4 | 기대효과 | stats-dotgrid1 |
| 5 | 마무리 | closing-thankyou1 |

테마: deepgreen
HTML 생성 중...
PPTX 변환 완료!

파일: 스마트물류시스템_제안서.pptx
```
