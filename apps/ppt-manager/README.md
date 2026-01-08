# ppt-manager

PPT 템플릿 및 에셋을 관리하는 Electron 데스크톱 앱.

## 개요

| 항목 | 값 |
|------|---|
| 앱 타입 | Electron Desktop App |
| 버전 | 1.0 (계획) |
| 프레임워크 | Electron + React |

## 기능

### P0 (필수)

| 기능 | 설명 |
|------|------|
| 템플릿 목록 | 썸네일 그리드 뷰로 모든 템플릿 표시 |
| 템플릿 상세 | 미리보기 + 메타데이터 (카테고리, 테마, 키워드) |
| 템플릿 삭제 | 선택한 템플릿 삭제 |
| 템플릿 아카이브 | 비활성화 (삭제 없이 숨김) |

### P1 (중요)

| 기능 | 설명 |
|------|------|
| 에셋 추가 | 드래그&드롭으로 아이콘/이미지 업로드 |
| 에셋 검색 | 태그/키워드 기반 필터링 |
| 카테고리 필터 | 템플릿 카테고리별 필터 |
| 테마 필터 | 호환 테마별 필터 |

### P2 (향후)

| 기능 | 설명 |
|------|------|
| 태그 관리 | 태그 추가/수정/삭제 |
| 테마 미리보기 | 색상 팔레트 시각화 |
| 문서 템플릿 관리 | 회사별 문서 양식 관리 |

---

## UI 설계

```
┌─────────────────────────────────────────────────────────────────┐
│  ppt-manager                                          [─][□][×] │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────┐ ┌─────────────────────────────────────────────┐   │
│ │ 사이드바   │ │                 메인 영역                    │   │
│ │           │ │                                             │   │
│ │ ▼ 템플릿   │ │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │   │
│ │   콘텐츠   │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │   문서     │ │  │cover│ │ toc │ │comp │ │proc │ │stat │  │   │
│ │   테마     │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │           │ │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │   │
│ │ ▼ 에셋    │ │                                             │   │
│ │   아이콘   │ │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │   │
│ │   이미지   │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ │           │ │  │grid │ │time │ │quote│ │close│ │cycle│  │   │
│ │           │ │  │     │ │     │ │     │ │     │ │     │  │   │
│ └───────────┘ │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘  │   │
│               └─────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│ 검색: [________________] 카테고리: [전체 ▼] 테마: [전체 ▼]       │
└─────────────────────────────────────────────────────────────────┘
```

### 템플릿 상세 뷰

```
┌─────────────────────────────────────────────────────────────────┐
│  ← 뒤로                              comparison-2col1           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────┐  ┌───────────────────────┐│
│  │                                 │  │ 정보                   ││
│  │                                 │  ├───────────────────────┤│
│  │         썸네일 미리보기          │  │ ID: comparison-2col1  ││
│  │                                 │  │ 카테고리: comparison   ││
│  │                                 │  │ 테마: deepgreen        ││
│  │                                 │  │ 품질: 9.2              ││
│  └─────────────────────────────────┘  │                       ││
│                                       │ 키워드:               ││
│                                       │ 비교, vs, 대비        ││
│                                       ├───────────────────────┤│
│                                       │ [아카이브] [삭제]      ││
│                                       └───────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| 프레임워크 | Electron 28+ |
| 프론트엔드 | React 18+ |
| 상태관리 | Zustand |
| UI 라이브러리 | Tailwind CSS + Radix UI |
| 빌드 | Vite + electron-builder |
| Python 연동 | child_process (spawn) |

---

## 폴더 구조

```
apps/ppt-manager/
├── package.json
├── electron/
│   ├── main.ts              # Electron 메인 프로세스
│   ├── preload.ts           # 프리로드 스크립트
│   └── ipc/                  # IPC 핸들러
│       ├── templates.ts      # 템플릿 관련 IPC
│       └── assets.ts         # 에셋 관련 IPC
├── src/
│   ├── App.tsx
│   ├── components/
│   │   ├── Sidebar.tsx
│   │   ├── TemplateGrid.tsx
│   │   ├── TemplateDetail.tsx
│   │   ├── AssetLibrary.tsx
│   │   ├── SearchBar.tsx
│   │   └── FilterDropdown.tsx
│   ├── hooks/
│   │   ├── useTemplates.ts
│   │   └── useAssets.ts
│   ├── services/
│   │   ├── templateService.ts
│   │   └── assetService.ts
│   └── store/
│       └── appStore.ts
├── scripts/                  # 기존 Python 스크립트
│   ├── template-manager.py
│   └── asset-manager.py
└── README.md
```

---

## 데이터 흐름

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│  IPC Handler    │────▶│  Python Script  │
│                 │     │  (Electron)     │     │                 │
│  TemplateGrid   │◀────│  templates.ts   │◀────│  template-      │
│  AssetLibrary   │     │  assets.ts      │     │  manager.py     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │  templates/     │
                        │  (파일 시스템)   │
                        │                 │
                        │  ├── themes/    │
                        │  ├── contents/  │
                        │  ├── documents/ │
                        │  └── assets/    │
                        └─────────────────┘
```

---

## IPC API

### 템플릿 API

```typescript
// 템플릿 목록 조회
ipcRenderer.invoke('templates:list', {
  type: 'contents' | 'documents' | 'themes',
  category?: string,
  theme?: string
})

// 템플릿 상세 조회
ipcRenderer.invoke('templates:get', { id: string })

// 템플릿 아카이브
ipcRenderer.invoke('templates:archive', { id: string })

// 템플릿 삭제
ipcRenderer.invoke('templates:delete', { id: string })
```

### 에셋 API

```typescript
// 에셋 검색
ipcRenderer.invoke('assets:search', {
  query: string,
  type: 'icon' | 'image'
})

// 에셋 추가
ipcRenderer.invoke('assets:add', {
  file: File,
  tags: string[]
})

// 에셋 삭제
ipcRenderer.invoke('assets:delete', { id: string })
```

---

## 개발 가이드

### 시작하기

```bash
cd apps/ppt-manager

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 빌드
npm run build

# 패키징
npm run package
```

### 환경 설정

```env
# .env
TEMPLATES_PATH=/home/jji/project/docs/templates
PYTHON_PATH=/usr/bin/python3
```

---

## 기존 스크립트 연동

### template-manager.py

```python
# 목록 조회
python template-manager.py list --type contents

# 상세 조회
python template-manager.py info --id cover-centered1

# 아카이브
python template-manager.py archive --id cover-centered1

# 삭제
python template-manager.py delete --id cover-centered1
```

### asset-manager.py

```python
# 검색
python asset-manager.py search --query "chart"

# 추가
python asset-manager.py add --file icon.svg --tags "chart,data"

# 삭제
python asset-manager.py delete --id chart-line
```

---

## 로드맵

### v1.0 (MVP)
- [ ] 프로젝트 초기 설정 (Electron + React)
- [ ] 템플릿 목록/상세 뷰
- [ ] 템플릿 삭제/아카이브
- [ ] 기본 검색 기능

### v1.1
- [ ] 에셋 라이브러리
- [ ] 드래그&드롭 업로드
- [ ] 태그 관리

### v2.0
- [ ] 테마 미리보기/편집
- [ ] 문서 템플릿 관리
- [ ] 템플릿 복제/수정
