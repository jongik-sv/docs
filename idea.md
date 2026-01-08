# PPT 자동 생성 서비스 - 구현 현황

## 핵심 결정사항

| 항목 | 결정 |
|------|------|
| 구현 방식 | Skills만 사용 (MCP 제외) |
| 기술 스택 | PptxGenJS + html2pptx.js |
| 템플릿 DB | YAML 기반 (LLM이 직접 선택) |
| 템플릿 구조 | 3타입 분리 (문서 + 콘텐츠 + 에셋) |

---

## 워크플로우 (7가지)

| # | 워크플로우 | 트리거 | 상태 |
|---|-----------|--------|------|
| 1 | html2pptx | 새 PPT 생성 요청 | ✅ 완료 |
| 2 | template | 회사 양식으로 생성 | ✅ 완료 |
| 3 | ooxml | 기존 PPT 수정 | ✅ 완료 |
| 4 | template-analyze | PPT → YAML 등록 | ✅ 완료 |
| 5 | style-extract | 이미지 스타일 추출 | ✅ 완료 |
| 6 | design-search | 디자인 레퍼런스 검색 | ✅ 완료 |
| 7 | template-manage | 템플릿 목록/삭제 | ✅ 완료 |
| 8 | asset-manage | 에셋 관리 | ✅ 완료 |
| 9 | slide-crawl | 온라인 슬라이드 크롤링 | ✅ 완료 |

---

## 템플릿 3타입 구조

| 타입 | 폴더 | 설명 |
|------|------|------|
| 문서 | `documents/{그룹}/` | 회사/브랜드별 전체 PPT 양식 |
| 콘텐츠 | `contents/` | 슬라이드 패턴 (cover, timeline 등) |
| 에셋 | `assets/` | 공용 이미지/아이콘 |

---

## 구현 현황

### Phase 1: 핵심 스크립트 ✅ 완료

| 파일 | 상태 |
|------|------|
| `SKILL.md` | ✅ |
| `html2pptx.md` | ✅ |
| `ooxml.md` | ✅ |
| `scripts/html2pptx.js` | ✅ |
| `scripts/inventory.py` | ✅ |
| `scripts/replace.py` | ✅ |
| `scripts/rearrange.py` | ✅ |
| `scripts/thumbnail.py` | ✅ |

### Phase 2: 3타입 템플릿 시스템 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `templates/documents/dongkuk/` | ✅ | 동국그룹 폴더 |
| `templates/documents/dongkuk/config.yaml` | ✅ | 그룹 테마 |
| `templates/documents/dongkuk/registry.yaml` | ✅ | 양식 목록 |
| `templates/documents/dongkuk/제안서1.yaml` | ✅ | 제안서 양식 |
| `templates/contents/registry.yaml` | ✅ | 콘텐츠 레지스트리 |
| `templates/contents/templates/*.yaml` | ✅ | 8개 콘텐츠 템플릿 |
| `templates/assets/registry.yaml` | ✅ | 에셋 레지스트리 |
| `scripts/template-analyzer.py` | ✅ | PPTX → YAML 분석 (3타입 구조 지원) |

### Phase 3: 레퍼런스 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `references/custom-elements.md` | ✅ | 요소 스키마 (HTML 태그, CSS, Placeholder) |
| `references/design-system.md` | ✅ | 디자인 규칙 (타이포, 레이아웃, 검증) |
| `references/color-palettes.md` | ✅ | 컬러 팔레트 (브랜드 + 18개 범용) |

### Phase 4: 유틸리티 스크립트 ✅ 완료

| 파일 | 상태 | 설명 |
|------|------|------|
| `scripts/asset-manager.py` | ✅ | 에셋 관리 CLI (추가/검색/삭제) |
| `scripts/template-manager.py` | ✅ | 템플릿 관리 CLI (목록/아카이브/삭제) |
| `scripts/style-extractor.py` | ✅ | 이미지 스타일 추출 (색상 분석) |
| `scripts/slide-crawler.py` | ✅ | 온라인 슬라이드 크롤링 |

---

## 완료 현황

1. ~~폴더 구조 생성~~ ✅
2. ~~registry.yaml 파일들 생성~~ ✅
3. ~~template-analyzer.py 스크립트 구현~~ ✅
4. ~~dongkuk 그룹 샘플 템플릿 구현~~ ✅
5. ~~Phase 3: 레퍼런스 문서 작성~~ ✅
6. ~~Phase 4: 유틸리티 스크립트 구현~~ ✅
7. ~~GUIDE.md 학습 가이드 작성~~ ✅

**모든 Phase 및 문서화 완료!**

---

## 기술 스택

- **Node.js**: pptxgenjs, playwright, sharp
- **Python**: python-pptx, markitdown, defusedxml


skills.cokac.com 에서 스킬 등록해서 배포 할 수 있음
https://www.youtube.com/watch?v=rNtpNY41h5o 코깍노 참고


이 컨텐츠를 재사용하려면 썸네일도 있어야 하고 컨텐츠의 모양을 더 자세하게 표편해야해. 각 도형의 종류와, 도형 또는 텍스트에 대한 ppt 페이지(1980x1080 크기로 치환)의 좌표(x, y), 크기(cx, cy) 스타일(투명도, 그림자 설정), 오브젝트간 상대적 거리와 계층 구조의 벡터화,  색상(다른 테마로 쉽게 바꿀 수 있는 형태; primary, secondery 등으로 표현), LLM의 디자인 품질 점수(9.5/10.0), 디자인 의도(Comparision, Timeline, FeatureSpec, Hierarchy, ... 등), 추가적인 정보로 아이콘 크기,  아이콘 종류 등을 추출해야 디자인에 대한 재사용이 가능해.



 SKILL.md 를 리펙토링 하자. 각 워크플로우별로 지시를 분리해서 관리하는 것이 좋겠어. 

 컨텐츠와 썸네일이 한 폴더에 있으니 관리하기가 좋지 않아. 각 추출한 컨텐츠는 폴더로 분류해서 저장하는 것이 좋겠어. 



우석지니(https://blog.naver.com/wooseokjin) 에서 템플릿 추출하자.


 ppt-gen 에서 아래에 나오는 인터넷 이미지에 대해서 컨텐츠를 추출해줘. \
  https://blog.naver.com/wooseokjin/224127136621?photoView=27
  https://blog.naver.com/wooseokjin/224127136621?photoView=15
  https://blog.naver.com/wooseokjin/224125145028?photoView=2
  https://blog.naver.com/wooseokjin/224125145028?photoView=3
  https://blog.naver.com/wooseokjin/224125145028?photoView=4
  https://blog.naver.com/wooseokjin/224125145028?photoView=5
  https://blog.naver.com/wooseokjin/224125145028?photoView=9
  https://blog.naver.com/wooseokjin/224125145028?photoView=12
  https://blog.naver.com/wooseokjin/224125145028?photoView=16
  https://blog.naver.com/wooseokjin/224125145028?photoView=20
  https://blog.naver.com/wooseokjin/224125145028?photoView=27
  https://blog.naver.com/wooseokjin/224125145028?photoView=29
  https://blog.naver.com/wooseokjin/224125145028?photoView=31
  https://blog.naver.com/wooseokjin/224125145028?photoView=33
  https://blog.naver.com/wooseokjin/224125145028?photoView=35
  https://blog.naver.com/wooseokjin/224125145028?photoView=36


네이버에서 다운안되게 해놓은 이미지 크롤링하는 방법을 연구해봐. 웹 검색해서 방법을 찾아봐.

ppt-gen 스킬에서 ppt양식 및 컨텐츠 추출할때 작성하는 yaml 파일에 그 양식이나 컨텐츠를 생성하는 프롬프트를 추론해서 만들어줘.  추론된 프롬프트를 입력으로 해서 PPT를 생성하면 해당 양식(페이지별)과 컨텐츠가 만들어지도록 해야해. 그 내용을 registry.yaml 에 예상 프롬프트 항목으로 넣을 수 있도록 해줘.
ppt를 생성할때 방금전에 생성한 항목을 검색해서 참고하도록 적용해줘.



ppt-gen 스킬에서 컨텐츠와 양식 내 페이지안에 배경 이미지가 들어갈 경우 이미지에 대한 간단한 설명도 포함 될 수 있도록 스킬을 수정해줘.



antigravity gemini 3 pro
flow-circular-apple1.png
 파일에서 각 텍스트 박스(위치, 크기, 폰트 크기), 이미지(위치, 크기, 종류) 들을 추출해서 
flow-circular-apple1.yaml
 파일 형태로 저장해봐. 추출한 이미지가 일반 그림이면 그림에 대한 간단한 설명, 그래프 형태면 SVG로 변환을 부탁해.




각 단계별로 output 폴더에 json 파일을 업데이트 할거야. 
json 파일에 각 단계 표시가 있으면 되고 pptx 생성을 위한 모든 데이터가 포함 되면 된다.
1. 발표내용, 발표 청중, 발표 목적, 발표 문서양식, 발표 시간, 테마, 문서 종류, ... 선택 
2. 발표내용 생성(슬라이드 별 내용)
3. 슬라이드 별 컨텐츠 종류 선정
4. 슬라이드 별 컨텐츠 생성
5. 슬라이드 별 컨텐츠를 ppt로 생성



● 모든 README.md 파일 업데이트를 완료했습니다.

  업데이트 요약

  | 파일                  | 추가된 내용                                                    |
  |-----------------------|----------------------------------------------------------------|
  | ppt-gen/README.md     | 5단계 파이프라인 다이어그램, Output 폴더 구조, 세션 관리 설명  |
  | ppt-create/README.md  | 4-5단계 담당 역할, Output 파일 구조                            |
  | ppt-design/README.md  | 1단계 (설정 선택) 지원 역할, stage-1-setup.json 설명           |
  | ppt-extract/README.md | 3단계 (템플릿 매칭) 지원 역할, stage-3-matching.json 설명      |
  | ppt-image/README.md   | 5단계 (검증) 담당 역할, thumbnails 폴더 구조, 피드백 루프 언급 |

  각 스킬의 파이프라인 역할 배분:

  1단계 설정 선택     → ppt-design (디자인 검색/분석)
  2단계 발표내용 생성  → ppt-gen (메인 스킬)
  3단계 템플릿 매칭    → ppt-extract (템플릿 제공)
  4단계 콘텐츠 생성    → ppt-create (HTML 생성)
  5단계 PPT 생성      → ppt-create + ppt-image (PPTX 변환 + 썸네일 검증)


  
  | 스킬        | 실제 역할                           | 파이프라인 관계               |
  |-------------|-------------------------------------|-------------------------------|
  | ppt-extract | PPT/이미지에서 콘텐츠·오브젝트 추출 | 파이프라인 외부 (템플릿 준비) |
  | ppt-design  |
  | ppt-create  | PPT 생성/수정 (html2pptx, ooxml)    | ?                             |
  | ppt-image   | 썸네일/이미지 생성                  | ?                             |
  | ppt-gen     | 메인 스킬 (전체 조율)               | 파이프라인 전체               |




## 추출 기능
1. 테마 추출
2. 컨텐츠 / 오브젝트 추출 
  - 입력 : PPTX, 이미지
  - 출력 : 컨텐츠, 오브젝트, 배경이미지 설명
3. 기존 PPT에서 문서 양식 추출 
  - 슬라이드 마스터 추출
  - 회사 로고

## 생성 워크플로우(ppt-gen)
1. 발표 자료 생성 
  - 입력 : 문서 종류, 발표 청중, 발표 목적, 발표 시간, 테마 / 문서양식(회사별 디자인)
2. 자료 검색 후 발표 자료 생성 
  - 입력 0에서 입력 받은 문서 종류, 발표 청중, 발표 목적, 발표 시간
  - 출력 json : 슬라이드 별 발표 내용 (슬라이드1 - 슬라이드n)
3. 슬라이드 별 컨텐츠 종류 선정(LLM이 선정함) - DB로 관리되는 컨텐츠, 오브젝트
  - 입력 : 2의 출력 json, 1에서 입력받은 테마 / 문서양식
  - 출력 json : 슬라이드 별 컨텐츠, 오브젝트 선정(적당한 오브젝트가 없으면 이미지 생성 프롬프트 생성기 call -> 이미지 생성 필요하면 이미지 생성 프롬프트)
4. 이미지 생성 프롬프트로 이미지 생성(아직 생성 기능 없음, skip 하면 됨)
  - 입력 : 3의 출력 json
  - 출력 : 이미지 생성 서비스로 생성된 이미지
5. 슬라이드 별 컨텐츠를 HTML / PPTX로 생성
  - 입력 : 3의 출력 json, 4의 출력 이미지(아직 기능이 없으므로 텍스트 박스로 처리)
  - 출력 : html/pptx





'c:\project\docs\깔끔이 딥그린.pptx'을 ppt-extract 스킬로 컨텐츠, 오브젝트 추출해줘.  

기본양식에서 문서양식을 뽑자.