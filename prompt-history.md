design_prompt와 image_generation_prompt를 모두 다 사용해서 @project-plan.json 을 pptx 로 만들어줘. pptx스킬과 dongkuk-brand 스킬을 사용해. V3 버전
---

@project-plan.json 파일의 내용으로 ppt를 생성해줘. 양식은 @.claude\includes\PPT기본양식.pptx 을 사용하고 양식에 대한 설명은 @.claude\includes\PPT기본양식_분석보고서.md 을 참고해.  --ultrathink  V4 버전 (완전 망함)

---
<!-- > @project-plan.json 과 @.claude\includes\PPT기본양식_분석보고서.md 를 읽고 `## 슬라이드 값 맵핑 규칙`을         
완성해줘. -->

@project-plan.json 파일의 내용으로 ppt를 생성해줘. 양식은 @.claude\includes\PPT기본양식.pptx 을 사용하고 양식에 대한 설명은 @.claude\includes\PPT기본양식_분석보고서.md 을 참고해. 각 페이지는 project-plan.json파일의 "slide_number" 의 PPT기본양식.pptx의 마스터슬라이드의 "layout" 번호에 해당하는 슬라이드를 사용해 생성해줘. 

## 슬라이드 맵핑규칙
  - ppt의 slide 1은 project-plan.json의 slide_number 1에 해당한다.
  - ppt의 slide 2는 project-plan.json의 slide_number 2에 해당한다.
  - ppt의 slide 3은 project-plan.json의 slide_number 3에 해당한다.
  - ppt의 slide 4는 project-plan.json의 slide_number 4에 해당한다.
  - ppt의 slide 5는 project-plan.json의 slide_number 5에 해당한다.

## 슬라이드 값 맵핑 규칙

### JSON → Layout Placeholder ID 맵핑

| JSON 필드 | Layout 1 (표지) | Layout 2 (목차) | Layout 3 (내지+Action) | Layout 4 (내지+Action, Body無) | Layout 5 (내지) |
|-----------|----------------|-----------------|----------------------|------------------------------|-----------------|
| `title` | **ID 15** | - | - | - | - |
| `subtitle` | **ID 27** (idx=13) | - | - | - | - |
| `main_title` | - | - | **ID 17** (idx=19) | **ID 17** (idx=19) | **ID 17** (idx=19) |
| `action_title` | - | - | **ID 16** (title) | **ID 16** (title) | - |
| `body` | - | - | **ID 15** (idx=18) | - | **ID 14** (idx=18) |
| `toc_items.number` | - | **ID 22** (idx=17) | - | - | - |
| `toc_items.title` | - | **ID 20** (idx=13) | - | - | - |
| `toc_items.pages` | - | **ID 17** (idx=14) | - | - | - |

### 상세 맵핑

```
Layout 1 (표지)
├── placeholders.title      → ID 15 (제목 1)
└── placeholders.subtitle   → ID 27 (텍스트 개체 틀 26, idx=13)

Layout 2 (목차)
├── toc_items[].number      → ID 22 (번호 열, idx=17)
├── toc_items[].title       → ID 20 (목차 제목 열, idx=13)
└── toc_items[].pages       → ID 17 (페이지 번호 열, idx=14)

Layout 3 (내지 - Action Title 사용)
├── placeholders.main_title   → ID 17 (텍스트 개체 틀 12, idx=19)
├── placeholders.action_title → ID 16 (제목 1, title type)
└── placeholders.body         → ID 15 (텍스트 개체 틀 3, idx=18)

Layout 4 (내지 - Action Title, Body 삭제)
├── placeholders.main_title   → ID 17 (텍스트 개체 틀 12, idx=19)
├── placeholders.action_title → ID 16 (제목 1, title type)
└── custom_elements           → 자유 콘텐츠 영역 (차트, 표, 이미지)

Layout 5 (내지 - Action Title 미사용)
├── placeholders.main_title   → ID 17 (텍스트 개체 틀 12, idx=19)
└── placeholders.body         → ID 14 (텍스트 개체 틀 3, idx=18)
```

### 공통 요소 (모든 내지 레이아웃)

| 요소 | Placeholder ID | 위치 |
|------|---------------|------|
| 슬라이드 번호 | **ID 23** (idx=4) | 하단 우측 끝 |
| 바닥글 | **ID 24** (idx=3) | 하단 우측 |
| 로고 | **ID 14** (picture) | 좌측 하단 |
| 구분선 | **ID 13** (cxnSp) | Main Title 하단 |

콘텐츠는 한쪽으로 쏠리면 안되고 중앙에 정렬되어야 해. 디자인도 디자인 프롬프트와 이미지 생성 프롬프트에 맞게 잘 만들면 된다. 플래이스 홀드에는 단순히 값만 들어가면 된다.
--ultrathink

---
1. PPT 생성 절차
 - image_generation_prompt를 사용해서 svg 이미지 생성
 - Image Converter cairosvg.svg2png()로 SVG → PNG 변환

2. ppt 생성용 json 파일을 사용하여 slide_number에 해당하는 양식 슬라이드를 생성 후 placeholder 내용만 대입

3. ppt 생성용 json 파일의 컨텐츠 영역 디자인 프롬프트로 HTML 생성

4. 2에서 만든 ppt 파일에 3에서 만든 HTML을 삽입 하여 ppt 파일 완성

5. 생성한 소스코드, html 삭제