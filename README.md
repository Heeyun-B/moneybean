# Git Branch & Commit 원칙

## 📌 Branch 원칙

### Branch 구조
```
master (production)
├── develop (개발 통합)
│   ├── feature/[기능명]
│   └── fix/[버그명]
└── hotfix/[긴급수정명]
```

### Branch 종류 및 역할

#### 1. `master` 브랜치
- **역할**: 프로덕션 배포 가능한 안정적인 코드
- **보호 규칙**: 직접 push 금지, PR을 통한 merge만 허용
- **배포**: master 브랜치에 merge되면 배포 가능 상태

#### 2. `develop` 브랜치
- **역할**: 개발 중인 기능들의 통합 브랜치
- **용도**: feature, fix 브랜치들이 merge되는 베이스
- **테스트**: develop에서 통합 테스트 진행 후 master으로 merge

#### 3. `feature/[기능명]` 브랜치
- **역할**: 새로운 기능 개발
- **생성 기준**: develop 브랜치에서 분기
- **네이밍 규칙**:
  - `feature/deposit-comparison` (예적금 비교 기능)
  - `feature/user-auth` (사용자 인증)
  - `feature/exchange-rate-api` (환율 API 연동)
  - `feature/asset-dashboard` (자산 대시보드)
- **Merge 대상**: develop 브랜치

#### 4. `fix/[버그명]` 브랜치
- **역할**: 버그 수정
- **생성 기준**: develop 브랜치에서 분기
- **네이밍 규칙**:
  - `fix/interest-calculation-error` (금리 계산 오류)
  - `fix/login-session-bug` (로그인 세션 버그)
- **Merge 대상**: develop 브랜치

#### 5. `hotfix/[긴급수정명]` 브랜치
- **역할**: 프로덕션 긴급 버그 수정
- **생성 기준**: master 브랜치에서 분기
- **네이밍 규칙**: `hotfix/critical-security-patch`
- **Merge 대상**: master과 develop 둘 다

---

## 📝 Commit 메시지 작성 규칙

### Commit Message 형식
```
[타입] 제목 (50자 이내)

본문 (선택사항, 72자 단위 줄바꿈)
- 변경 이유
- 주요 변경 내용

관련 이슈: #이슈번호
```

### Commit 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat: 예금 금리 비교 기능 구현` |
| `fix` | 코드/버그 수정 | `fix: 적금 이자 계산 오류 수정` |
| `design` | UI/UX 디자인 변경 | `design: 자산 대시보드 레이아웃 개선` |
| `style` | 코드 포맷팅 (기능 변경 없음) | `style: Django models.py 코드 정리` |
| `docs` | 문서 수정 | `docs: API 명세서 업데이트` |
| `test` | 테스트 코드 추가/수정 | `test: 예적금 비교 API 테스트 추가` |
| `chore` | 빌드, 설정 변경 | `chore: Django settings 환경변수 설정` |
| `rename` | 파일/폴더명 변경 | `rename: views.py → deposit_views.py` |
| `remove` | 파일 삭제 | `remove: 미사용 API 엔드포인트 제거` |

### Commit 메시지 예시

#### ✅ 예시
```
feat: 은행별 예금 금리 비교 API 구현
```

```
fix: Vue 컴포넌트에서 금리 계산 오류 수정
```

---

## ⏰ Commit 시점 규칙

### Commit을 남겨야 하는 시점

1. **기능 단위 완성 시**
   - 하나의 독립적인 기능이 동작하는 상태
   - 예: 예금 상품 CRUD 중 Create 기능 완성

2. **의미 있는 변경 완료 시**
   - 버그 수정 완료
   - API 연동 완료
   - 화면 UI 한 단위 완성

3. **작업 전환 전**
   - 다른 기능을 작업하기 전 현재 작업 저장
   - 하루 작업 종료 시점(`_1`, `_2`, ..., `_fin`)

4. **테스트 통과 시**
   - 작성한 코드가 정상 동작 확인 후

### Commit 하지 말아야 할 시점

- ❌ 코드가 컴파일/실행되지 않는 상태
- ❌ 작업 중간에 의미 없이 자주 커밋
- ❌ 여러 기능이 섞인 상태 (원자성 위반)

---

## 🚨 주의사항

### 1. 끝나거나 집 갈때 무조건 커밋하기.
### 2. 새로 시작할 때 무조건 `pull` 받기
### 3. Merge Conflict : 혼자서 해결하지 않고, 팀원과 같이 해결하기

---

## 📚 참고 자료
- [Git Branch 전략](https://techblog.woowahan.com/2553/)
- [Commit Message Convention](https://www.conventionalcommits.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/)