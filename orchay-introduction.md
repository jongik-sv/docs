# orchay 소개 PPT 슬라이드 내용

---

## 슬라이드 1: 표지

**orchay**
*orchestration + okay*

WezTerm 기반 AI 개발 자동화 스케줄러

---

## 슬라이드 2: 문제 정의

### AI 코딩 어시스턴트의 한계

- **단일 작업**: 한 번에 하나의 Task만 처리 가능
- **수동 관리**: 개발자가 직접 Task를 할당하고 모니터링
- **컨텍스트 손실**: Task 전환 시 이전 작업 맥락 유실
- **비효율성**: 대기 시간 동안 다른 작업 불가

### 필요한 것
> "여러 AI Worker에게 Task를 자동으로 분배하고
> 진행 상황을 모니터링하는 오케스트레이터"

---

## 슬라이드 3: orchay 소개

### orchay란?

**WBS(Work Breakdown Structure) 기반 Task 스케줄러**

- wbs.yaml 파일에서 Task 목록 추출
- 여러 Claude Code Worker pane에 자동 분배
- 실시간 진행 상황 모니터링
- 워크플로우 기반 자동 상태 전이

### 핵심 가치

| 기존 방식 | orchay 방식 |
|----------|------------|
| 1명이 1개 Task | N명이 N개 Task 병렬 처리 |
| 수동 Task 할당 | 자동 Task 분배 |
| 수동 상태 관리 | 자동 워크플로우 실행 |

---

## 슬라이드 4: 작동 원리

### 전체 흐름

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  wbs.yaml   │───▶│   orchay    │───▶│  Claude     │
│  (Task 정의) │    │ (스케줄러)   │    │  Workers    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                 │                   │
       │            파싱 & 필터링          명령 전송
       │                 │                   │
       ▼                 ▼                   ▼
   Task 목록       실행 가능 Task      /wf:start TSK-01-01
```

### 레이아웃

```
+------------+-----------+
|            |  Worker 1 |
| Scheduler  +-----------+
|    (0)     |  Worker 2 |
|            +-----------+
|            |  Worker 3 |
+------------+-----------+
```

---

## 슬라이드 5: 핵심 기능 (1/2)

### 1. WBS 파싱 & 모니터링

- YAML 형식의 wbs.yaml 파일 실시간 감시
- Task 정보 자동 추출 (ID, 상태, 우선순위, 의존성)
- 파일 변경 시 즉시 반영

### 2. 지능형 Task 분배

- **우선순위 기반**: critical > high > medium > low
- **의존성 검사**: 선행 Task 완료 여부 확인
- **상태 기반 필터링**: 실행 가능 Task만 선별

### 3. Worker 상태 감지

| 상태 | 의미 |
|------|------|
| idle | 작업 대기 중 (새 Task 할당 가능) |
| busy | 작업 실행 중 |
| done | 작업 완료 (신호 수신) |
| paused | 일시 정지 (rate limit 등) |
| error | 오류 발생 |

---

## 슬라이드 6: 워크플로우 명령어 시스템

### Slash 명령어 기반 자동화

| 단계 | 명령어 | 역할 |
|------|--------|------|
| 설계 | `/wf:start` | PRD 분석 → 설계 문서 생성 |
| 설계 | `/wf:review` | 3개 관점 병렬 리뷰 (아키텍처/보안/품질) |
| 설계 | `/wf:apply` | 리뷰 지적사항 선택적 적용 |
| 구현 | `/wf:build` | TDD 기반 구현 (Backend/Frontend 병렬) |
| 구현 | `/wf:audit` | 코드 리뷰 (품질/보안/성능 병렬 검증) |
| 구현 | `/wf:patch` | 코드 리뷰 지적사항 반영 |
| 검증 | `/wf:verify` | 통합테스트 실행 및 검증 ([im] → [vf]) |
| 검증 | `/wf:test` | TDD + E2E 테스트 실행 |
| 완료 | `/wf:done` | 매뉴얼 생성, 품질 메트릭 |

### 계층 입력 지원

```bash
/wf:start TSK-01-01      # 단일 Task
/wf:start ACT-01-01      # Activity 내 모든 Task 병렬
/wf:start WP-01          # Work Package 내 모든 Task 병렬
```

---

## 슬라이드 7: 설계 단계 명령어 (review, apply)

### /wf:review - 설계 리뷰

3개 관점에서 **병렬 품질 검증** 수행:

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ architecture-   │ │ security-       │ │ quality-        │
│ review          │⇄│ review          │⇄│ review          │
│ SOLID, 확장성   │ │ OWASP, 인증    │ │ 완전성, 추적성  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**산출물**: `021-design-review-{llm}-{n}.md`

### /wf:apply - 설계 리뷰 반영

**맥락 기반 선택적 적용** (무조건 적용 금지):

| 판단 | 조건 | 처리 |
|------|------|------|
| ✅ 적용 | 시스템&Task 적합 | 그대로 반영 |
| 📝 조정 | 취지 유효, 맞춤 필요 | 수정하여 반영 |
| ⏸️ 보류 | 범위 초과, 부적합 | 미반영 (사유 기록) |

**우선순위**: P1 100% 필수, P2 80% 이상 권장

---

## 슬라이드 8: 구현 단계 명령어 (audit, patch)

### /wf:audit - 코드 리뷰

구현 완료 후 3개 관점에서 **병렬 코드 검증**:

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ quality-audit   │ │ security-audit  │ │ performance-    │
│ SOLID, 중복,   │⇄│ 인젝션, 인증,  │⇄│ audit           │
│ 복잡도         │ │ 암호화         │ │ 쿼리, 캐싱     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**산출물**: `031-code-review-{llm}-{n}.md`

### /wf:patch - 코드 리뷰 반영

| 우선순위 | 분류 | 적용 원칙 |
|---------|------|----------|
| **P1** | Must Fix | 보안 취약점, 치명적 버그 |
| **P2** | Should Fix | 성능 이슈, 코드 품질 |
| **P3** | Nice to Have | 코딩 스타일, 문서화 |

**테스트-수정 루프**: 최대 5회 자동 반복

### 반복 리뷰-패치 사이클

```
[im] 구현 → /wf:audit → 리뷰 문서
               │
               ▼
          /wf:patch → 코드 수정 → "(적용완료)"
               │
               └── (품질 만족까지 반복)
```

---

## 슬라이드 9: 워크플로우 산출물

### 단계별 생성 문서

| 단계 | 명령어 | 생성 문서 |
|------|--------|----------|
| 설계 시작 | `/wf:start` | `010-design.md` |
| 설계 리뷰 | `/wf:review` | `021-design-review-{llm}-{n}.md` |
| 리뷰 반영 | `/wf:apply` | 설계 문서 수정, "(적용완료)" |
| 구현 | `/wf:build` | `030-implementation.md` |
| 코드 리뷰 | `/wf:audit` | `031-code-review-{llm}-{n}.md` |
| 패치 | `/wf:patch` | 코드 수정, "(적용완료)" |
| 검증 | `/wf:verify` | 통합테스트 결과 |
| 테스트 | `/wf:test` | `070-*-test-results.md` |
| 완료 | `/wf:done` | `080-manual.md` |

### 완료 신호 프로토콜

```
ORCHAY_DONE:{project}/{task-id}:{command}:{status}

예: ORCHAY_DONE:orchay/TSK-01-01:build:success
예: ORCHAY_DONE:orchay/TSK-02-03:test:error:커버리지 미달
```

> orchay 스케줄러가 이 신호를 감지하여 다음 단계를 자동 실행

---

## 슬라이드 10: 실행 모드 (workflows.json)

### 4가지 실행 모드

| 모드 | 워크플로우 범위 | 종료 상태 | 의존성 |
|------|---------------|----------|--------|
| **design** | start → review → apply | [dd] 상세설계 | 무시 |
| **quick** | start → approve → build → done | [xx] 완료 | 검사 |
| **develop** | 전체 (리뷰/테스트 포함) | [im] 구현 | 검사 |
| **force** | quick과 동일 | [xx] 완료 | 무시 |

### 상태 전이 다이어그램

```
[ ] Todo → [dd] 상세설계 → [ap] 승인 → [im] 구현 → [vf] 검증 → [xx] 완료
  start     approve        build       verify       done
```

### 카테고리별 워크플로우

| 카테고리 | 설명 | 구현 명령 |
|---------|------|----------|
| development | 신규 기능 개발 | build |
| defect | 버그 수정 | fix |
| infrastructure | 인프라/리팩토링 | build |

---

## 슬라이드 11: 기획 명령어 (/plan:*)

### WBS 자동 생성

PRD 문서를 분석하여 YAML 형식의 WBS를 자동 생성합니다.

```bash
/plan:wbs .orchay/projects/myapp/prd.md
/plan:wbs .orchay/projects/myapp/prd.md --scale large
```

### WBS YAML 구조

```yaml
project:
  id: my-project
  name: "프로젝트 이름"
  version: "0.1.0"

workPackages:
  - id: WP-01
    title: "핵심 기능"
    tasks:
      - id: TSK-01-01
        title: "로그인 구현"
        category: development
        status: "[ ]"
        priority: high
        requirements:
          prdRef: "FR-AUTH-001"
          items: ["이메일 로그인", "JWT 토큰"]
          acceptance: ["로그인 성공 시 토큰 반환"]
```

### 계층 구조 자동 결정

| 기준 | 4단계 (WP→ACT→TSK) | 3단계 (WP→TSK) |
|------|-------------------|----------------|
| 예상 기간 | 12개월+ | 12개월 미만 |
| 팀 규모 | 10명+ | 10명 미만 |
| Task 수 | 50개+ | 50개 미만 |

---

## 슬라이드 12: 아키텍처

### 시스템 구성

```
orchay/
├── main.py          # 오케스트레이터 (메인 루프)
├── scheduler.py     # Task 필터링 & 분배 로직
├── wbs_parser.py    # WBS 파일 파싱 & 감시
├── worker.py        # Worker 상태 감지
├── models/          # Pydantic 데이터 모델
└── utils/
    └── wezterm.py   # WezTerm CLI 래퍼

.claude/commands/
├── wf/              # 워크플로우 명령어
│   ├── start.md     # /wf:start
│   ├── build.md     # /wf:build
│   └── ...
└── plan/            # 기획 명령어
    └── wbs.md       # /plan:wbs
```

### 기술 스택

| 구성 요소 | 기술 |
|----------|------|
| 터미널 | WezTerm (멀티 pane 지원) |
| AI Worker | Claude Code |
| 언어 | Python 3.10+ |
| TUI | Textual + Rich |
| 파일 감시 | watchdog |

---

## 슬라이드 13: 사용법

### 기본 실행

```bash
# 프로젝트 폴더에서 실행
cd {프로젝트 루트}
orchay [프로젝트명] [옵션]

# 예시
orchay my_project           # 기본 실행
orchay my_project -w 5      # Worker 5개
orchay my_project -m design # 설계 모드
```

### 실행 화면

```
orchay - Task Scheduler v0.1.0

WBS: /project/wbs.yaml
Mode: quick | Workers: 3개 | Tasks: 9개

                 Worker Status
┌────┬──────┬────────┬──────────────┐
│ ID │ Pane │ State  │ Task         │
├────┼──────┼────────┼──────────────┤
│ 1  │ 0    │ busy   │ TSK-02-01    │
│ 2  │ 2    │ idle   │ -            │
│ 3  │ 1    │ idle   │ -            │
└────┴──────┴────────┴──────────────┘

Queue: 5 pending, 1 running, 3 done
```

---

## 슬라이드 14: 설치 방법

### 사전 요구사항

| 도구 | 용도 | 필수 |
|------|------|------|
| WezTerm | 멀티 pane 터미널 | ✅ |
| Claude Code | AI Worker | ✅ |

### 설치 옵션

**방법 1: 실행 파일 (권장)**
```bash
# GitHub Releases에서 다운로드
# Linux: orchay-linux-x64.tar.gz
# Windows: orchay-windows-x64.zip
# macOS: orchay-macos-x64.tar.gz
```

**방법 2: pipx**
```bash
pipx install orchay
```

**방법 3: pip**
```bash
pip install orchay
```

---

## 슬라이드 15: 효과 및 기대 가치

### 개발 생산성 향상

| 지표 | 기존 | orchay 적용 후 |
|------|------|---------------|
| 동시 작업 Task | 1개 | N개 (Worker 수) |
| Task 할당 | 수동 | 자동 |
| 진행 모니터링 | 수동 확인 | 실시간 대시보드 |
| 워크플로우 | 수동 전환 | 자동 실행 |

### 적용 시나리오

- **대규모 기능 개발**: 여러 Task 병렬 처리
- **마이그레이션 작업**: 반복적인 Task 자동화
- **코드 리뷰/리팩토링**: 체계적인 워크플로우 적용
- **테스트 자동화**: 구현 후 자동 테스트 실행

---

## 슬라이드 16: 향후 개발 예정 기능

### 🚀 Git Worktree 통합 (핵심 기능)

**문제**: 여러 Worker가 동일 브랜치에서 작업 시 충돌 발생

**해결**: 각 Worker별 독립 worktree 자동 생성

```
project/
├── .git/                    # 공유 Git 저장소
├── worktree-worker-1/       # Worker 1 전용 작업 공간
│   └── TSK-01-01 브랜치
├── worktree-worker-2/       # Worker 2 전용 작업 공간
│   └── TSK-01-02 브랜치
└── worktree-worker-3/       # Worker 3 전용 작업 공간
    └── TSK-02-01 브랜치
```

**기대 효과**:
- 브랜치 충돌 없는 완전 병렬 개발
- Task별 독립적인 커밋 히스토리
- 자동 브랜치 생성/정리

---

### 📊 추가 예정 기능

| 우선순위 | 기능 | 설명 |
|---------|------|------|
| **높음** | 동적 Worker 스케일링 | 부하에 따른 Worker 자동 추가/제거 |
| **높음** | 의존성 위상정렬 | Task 실행 순서 자동 최적화 |
| **높음** | 순환 의존성 감지 | 잘못된 의존성 조기 발견 |
| **중간** | 다중 LLM 지원 | Claude, GPT, Gemini 혼합 사용 |
| **중간** | Rate Limit 동적 조정 | 제공자별 제한 자동 관리 |
| **중간** | Worker 헬스체크 | 비정상 Worker 자동 재시작 |
| **낮음** | 성능 메트릭 대시보드 | 토큰 사용량, 응답 시간 시각화 |
| **낮음** | 웹 기반 WBS 편집 | orchay_web에서 직접 WBS 수정 |

---

## 슬라이드 17: 마무리

### orchay 요약

> **"AI 코딩 어시스턴트를 위한 Task 오케스트레이터"**

- WBS 기반 Task 자동 분배
- 다중 Claude Code Worker 병렬 실행
- 워크플로우 기반 자동화
- 실시간 모니터링 & 상태 관리

### 링크

- **GitHub**: github.com/jongik-sv/orchay
- **PyPI**: pypi.org/project/orchay

### Q&A

질문이 있으신가요?

---
