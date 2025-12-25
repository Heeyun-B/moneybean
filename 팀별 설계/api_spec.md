# API 명세서

## 📋 목차
1. [Accounts (회원 관리)](#accounts-회원-관리)
2. [Assets (내 자산)](#assets-내-자산)
3. [Boards (커뮤니티 게시판)](#boards-커뮤니티-게시판)
4. [Finance Infos (금융 정보 게시판)](#finance-infos-금융-정보-게시판)
5. [Finance News (뉴스 크롤링)](#finance-news-뉴스-크롤링)
6. [Deposits (예금/적금)](#deposits-예금적금)
7. [Gold Prices(현물 자산)](#gold-prices-현물-자산)
8. [Quizzes(퀴즈)](#quizzes-퀴즈)
9. [AI Services (AI 기능)](#ai-services-ai-기능)

---

## Accounts (회원 관리)

### 1. 회원가입

- **URL**: `/api/accounts/signup/`
- **Method**: `POST`
- **인증**: 불필요
- **설명**: 새로운 사용자 회원가입

#### Request Body
```json
{
  "username": "testuser",
  "password": "password123!",
  "password2": "password123!",
  "email": "test@example.com",
  "nickname": "테스트닉네임",
  "birth_date": "1990-05-15"  // 선택 사항
}
```

#### Response (201 Created)
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "테스트닉네임"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### Error Response (400 Bad Request)
```json
{
  "username": ["이미 존재하는 사용자명입니다."],
  "nickname": ["이미 사용 중인 닉네임입니다."],
  "password": ["비밀번호가 일치하지 않습니다."]
}
```

---

### 2. 로그인

- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **인증**: 불필요
- **설명**: 사용자 로그인 및 토큰 발급

#### Request Body
```json
{
  "username": "testuser",
  "password": "password123!"
}
```

#### Response (200 OK)
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "nickname": "테스트닉네임",
    "is_staff": false
  }
}
```

#### Error Response (401 Unauthorized)
```json
{
  "non_field_errors": ["아이디 또는 비밀번호가 올바르지 않습니다."]
}
```

---

### 3. 로그아웃

- **URL**: `/api/accounts/logout/`
- **Method**: `POST`
- **인증**: 필요
- **설명**: 사용자 로그아웃 및 토큰 무효화

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "message": "로그아웃되었습니다."
}
```

---

### 4. 프로필 조회

- **URL**: `/api/accounts/profile/`
- **Method**: `GET`
- **인증**: 필요 (로그인 사용자)
- **설명**: 현재 로그인한 사용자의 프로필 정보 조회 (가입한 금융상품 포함)

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "테스트닉네임",
  "birth_date": "1990-05-15",
  "first_name": "홍",
  "last_name": "길동",
  "profile_image": "/media/profile_images/user1.jpg",
  "profile_image_url": "http://localhost:8000/media/profile_images/user1.jpg",
  "date_joined": "2025-12-23T10:00:00Z",
  "deposit_subscriptions": [
    {
      "id": 1,
      "product_code": "WR0001B",
      "product_name": "우리 SUPER정기예금",
      "bank_name": "우리은행",
      "interest_rate": 3.5,
      "save_term": 12,
      "subscribed_at": "2025-12-20T14:30:00Z"
    }
  ],
  "saving_subscriptions": [
    {
      "id": 1,
      "product_code": "SH001",
      "product_name": "신한 청년희망적금",
      "bank_name": "신한은행",
      "interest_rate": 4.2,
      "save_term": 12,
      "subscribed_at": "2025-12-22T09:00:00Z"
    }
  ]
}
```

---

### 5. 프로필 수정

- **URL**: `/api/accounts/profile/update/`
- **Method**: `PUT` 또는 `PATCH`
- **인증**: 필요 (로그인 사용자)
- **Content-Type**: `multipart/form-data` (이미지 업로드 시)
- **설명**: 프로필 정보 수정

#### Request Headers
```
Authorization: Token {your_token}
```

#### Request (multipart/form-data)
```
nickname: "새닉네임"
email: "newemail@example.com"
birth_date: "1995-03-20"
first_name: "김"
last_name: "철수"
profile_image: [파일]
```

#### Response (200 OK)
```json
{
  "id": 1,
  "username": "testuser",
  "email": "newemail@example.com",
  "nickname": "새닉네임",
  "birth_date": "1995-03-20",
  "first_name": "김",
  "last_name": "철수",
  "profile_image_url": "http://localhost:8000/media/profile_images/new_image.jpg"
}
```

#### Error Response (400 Bad Request)
```json
{
  "nickname": ["이미 사용 중인 닉네임입니다."]
}
```

---

### 6. 비밀번호 변경

- **URL**: `/api/accounts/profile/password/`
- **Method**: `PUT`
- **인증**: 필요 (로그인 사용자)
- **설명**: 비밀번호 변경

#### Request Headers
```
Authorization: Token {your_token}
```

#### Request Body
```json
{
  "old_password": "old_password123!",
  "new_password": "new_password123!",
  "new_password_confirm": "new_password123!"
}
```

#### Response (200 OK)
```json
{
  "message": "비밀번호가 성공적으로 변경되었습니다."
}
```

#### Error Response (400 Bad Request)
```json
{
  "old_password": ["현재 비밀번호가 일치하지 않습니다."]
}
```
또는
```json
{
  "new_password_confirm": ["새 비밀번호가 일치하지 않습니다."]
}
```

---

### 7. 프로필 이미지 삭제

- **URL**: `/api/accounts/profile/image/delete/`
- **Method**: `DELETE`
- **인증**: 필요 (로그인 사용자)
- **설명**: 프로필 이미지 삭제

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "message": "프로필 이미지가 삭제되었습니다."
}
```

#### Error Response (400 Bad Request)
```json
{
  "message": "삭제할 이미지가 없습니다."
}
```

---

### 8. 회원 탈퇴

- **URL**: `/api/accounts/profile/delete/`
- **Method**: `DELETE`
- **인증**: 필요 (로그인 사용자)
- **설명**: 회원 탈퇴

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (204 No Content)
```json
{
  "message": "회원 탈퇴가 완료되었습니다."
}
```

---

## Assets (내 자산)

### 1. 자산 카테고리 목록 조회

- **URL**: `/api/v1/assets/categories/`
- **Method**: `GET`
- **인증**: 필요 (로그인 사용자)
- **설명**: 자산 카테고리 목록 조회 (Dropdown 메뉴 구성용)

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "name": "예금",
    "group": "CASH"
  },
  {
    "id": 2,
    "name": "적금",
    "group": "CASH"
  },
  {
    "id": 3,
    "name": "주식",
    "group": "INVEST"
  },
  {
    "id": 4,
    "name": "코인",
    "group": "INVEST"
  },
  {
    "id": 5,
    "name": "대출",
    "group": "DEBT"
  }
]
```

---

### 2. 내 자산 목록 조회

- **URL**: `/api/v1/assets/my-assets/`
- **Method**: `GET`
- **인증**: 필요 (로그인 사용자)
- **설명**: 로그인한 사용자의 자산 목록 조회

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "name": "우리은행 예금",
    "category": 1,
    "current_value": 20000000,
    "order": 1,
    "created_at": "2025-12-20T10:00:00Z",
    "updated_at": "2025-12-20T10:00:00Z"
  },
  {
    "id": 2,
    "name": "삼성전자 주식",
    "category": 3,
    "current_value": 5000000,
    "order": 2,
    "created_at": "2025-12-21T11:00:00Z",
    "updated_at": "2025-12-21T11:00:00Z"
  }
]
```

---

### 3. 자산 추가

- **URL**: `/api/v1/assets/my-assets/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 새로운 자산 정보 등록

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "name": "신한은행 적금",
  "category": 2,
  "current_value": 10000000,
  "order": 3
}
```

**필드 설명:**
- `name`: 자산 이름 (필수)
- `category`: 카테고리 ID (필수)
- `current_value`: 현재 가치/잔액 (필수)
- `order`: 정렬 순서 (선택, 기본값: 0)

#### Response (201 Created)
```json
{
  "id": 3,
  "name": "신한은행 적금",
  "category": 2,
  "current_value": 10000000,
  "order": 3,
  "created_at": "2025-12-23T12:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z"
}
```

#### Error Response (400 Bad Request)
```json
{
  "name": ["이 필드는 필수 항목입니다."],
  "category": ["이 필드는 필수 항목입니다."],
  "current_value": ["이 필드는 필수 항목입니다."]
}
```

---

### 4. 자산 상세 조회

- **URL**: `/api/v1/assets/my-assets/{pk}/`
- **Method**: `GET`
- **인증**: 필요 (로그인 사용자, 본인 자산만 조회 가능)
- **설명**: 특정 자산의 상세 정보 조회

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "우리은행 예금",
  "category": 1,
  "current_value": 20000000,
  "order": 1,
  "created_at": "2025-12-20T10:00:00Z",
  "updated_at": "2025-12-20T10:00:00Z"
}
```

#### Error Response (404 Not Found)
```json
{
  "detail": "찾을 수 없습니다."
}
```

---

### 5. 자산 수정

- **URL**: `/api/v1/assets/my-assets/{pk}/`
- **Method**: `PUT` 또는 `PATCH`
- **인증**: 필요 (로그인 사용자, 본인 자산만 수정 가능)
- **설명**: 특정 자산 정보 수정

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body (PATCH - 부분 수정)
```json
{
  "current_value": 25000000
}
```

#### Request Body (PUT - 전체 수정)
```json
{
  "name": "우리은행 예금 (수정)",
  "category": 1,
  "current_value": 25000000,
  "order": 1
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "name": "우리은행 예금 (수정)",
  "category": 1,
  "current_value": 25000000,
  "order": 1,
  "created_at": "2025-12-20T10:00:00Z",
  "updated_at": "2025-12-23T13:00:00Z"
}
```

---

### 6. 자산 삭제

- **URL**: `/api/v1/assets/my-assets/{pk}/`
- **Method**: `DELETE`
- **인증**: 필요 (로그인 사용자, 본인 자산만 삭제 가능)
- **설명**: 특정 자산 삭제

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (204 No Content)
```
(응답 본문 없음)
```

#### Error Response (404 Not Found)
```json
{
  "detail": "찾을 수 없습니다."
}
```

---

### 7. 재정 정보 조회

- **URL**: `/api/v1/assets/financial-info/`
- **Method**: `GET`
- **인증**: 필요 (로그인 사용자)
- **설명**: 로그인한 사용자의 월 수입/지출 정보 조회

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "monthly_income": 5000000,
  "monthly_expense": 3000000,
  "created_at": "2025-12-20T10:00:00Z",
  "updated_at": "2025-12-20T10:00:00Z"
}
```

**필드 설명:**
- `monthly_income`: 월 수입
- `monthly_expense`: 월 지출

---

### 8. 재정 정보 수정

- **URL**: `/api/v1/assets/financial-info/`
- **Method**: `PUT` 또는 `PATCH`
- **인증**: 필요 (로그인 사용자)
- **설명**: 월 수입/지출 정보 수정 (없으면 자동 생성)

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body (PATCH - 부분 수정)
```json
{
  "monthly_income": 6000000
}
```

#### Request Body (PUT - 전체 수정)
```json
{
  "monthly_income": 6000000,
  "monthly_expense": 3500000
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "monthly_income": 6000000,
  "monthly_expense": 3500000,
  "created_at": "2025-12-20T10:00:00Z",
  "updated_at": "2025-12-23T14:00:00Z"
}
```

---

## Boards (커뮤니티 게시판)

### 1. 게시글 목록 조회

- **URL**: `/api/boards/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 커뮤니티 게시글 목록 조회 (최신순 정렬)

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "title": "투자 고민 있어요",
    "content": "주식 투자 시작하려는데...",
    "username": "user1",
    "created_at": "2025-12-23T10:00:00Z",
    "like_count": 5,
    "comment_count": 3
  },
  {
    "id": 2,
    "title": "적금 추천 부탁드려요",
    "content": "어떤 적금이 좋을까요?",
    "username": "user2",
    "created_at": "2025-12-22T15:30:00Z",
    "like_count": 10,
    "comment_count": 7
  }
]
```

---

### 2. 게시글 작성

- **URL**: `/api/boards/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 새로운 게시글 작성

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "재테크 질문 있습니다",
  "content": "월급의 몇 퍼센트를 저축하는 게 좋을까요?"
}
```

#### Response (201 Created)
```json
{
  "id": 3,
  "title": "재테크 질문 있습니다",
  "content": "월급의 몇 퍼센트를 저축하는 게 좋을까요?",
  "username": "user3",
  "created_at": "2025-12-23T11:00:00Z",
  "updated_at": "2025-12-23T11:00:00Z",
  "like_count": 0,
  "comment_count": 0,
  "comments": []
}
```

#### Error Response (400 Bad Request)
```json
{
  "title": ["이 필드는 필수 항목입니다."],
  "content": ["이 필드는 필수 항목입니다."]
}
```

---

### 3. 게시글 상세 조회

- **URL**: `/api/boards/articles/{article_pk}/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 특정 게시글 상세 정보 조회 (댓글 포함)

#### Response (200 OK)
```json
{
  "id": 1,
  "title": "투자 고민 있어요",
  "content": "주식 투자 시작하려는데 어떤 종목이 좋을까요?",
  "username": "user1",
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T10:00:00Z",
  "like_count": 5,
  "is_liked": true,
  "comments": [
    {
      "id": 1,
      "content": "삼성전자 추천드려요!",
      "username": "user2",
      "article": 1,
      "created_at": "2025-12-23T10:30:00Z"
    },
    {
      "id": 2,
      "content": "안전하게 ETF부터 시작하세요.",
      "username": "user3",
      "article": 1,
      "created_at": "2025-12-23T11:00:00Z"
    }
  ],
  "comment_count": 2
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

---

### 4. 게시글 수정

- **URL**: `/api/boards/articles/{article_pk}/`
- **Method**: `PUT`
- **인증**: 필요 (로그인 사용자, 작성자만 수정 가능)
- **설명**: 게시글 수정

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "title": "수정된 제목",
  "content": "수정된 내용",
  "username": "user1",
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z",
  "like_count": 5,
  "comment_count": 2
}
```

#### Error Response (403 Forbidden)
```json
{
  "error": "권한이 없습니다."
}
```

---

### 5. 게시글 삭제

- **URL**: `/api/boards/articles/{article_pk}/`
- **Method**: `DELETE`
- **인증**: 필요 (로그인 사용자, 작성자만 삭제 가능)
- **설명**: 게시글 삭제

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (204 No Content)
```json
{
  "message": "게시글이 삭제되었습니다."
}
```

#### Error Response (403 Forbidden)
```json
{
  "error": "권한이 없습니다."
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

---

### 6. 게시글 좋아요 토글

- **URL**: `/api/boards/articles/{article_pk}/like/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 게시글 좋아요 추가/취소

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
**좋아요 추가 시:**
```json
{
  "message": "좋아요를 눌렀습니다.",
  "is_liked": true
}
```

**좋아요 취소 시:**
```json
{
  "message": "좋아요가 취소되었습니다.",
  "is_liked": false
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

---

### 7. 댓글 작성

- **URL**: `/api/boards/articles/{article_pk}/comment_create/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 게시글에 댓글 작성

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "content": "좋은 정보 감사합니다!"
}
```

#### Response (201 Created)
```json
{
  "id": 3,
  "content": "좋은 정보 감사합니다!",
  "username": "user4",
  "article": 1,
  "created_at": "2025-12-23T12:00:00Z"
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

#### Error Response (400 Bad Request)
```json
{
  "content": ["이 필드는 필수 항목입니다."]
}
```

---

### 8. 댓글 삭제

- **URL**: `/api/boards/comments/{comment_pk}/`
- **Method**: `DELETE`
- **인증**: 필요 (로그인 사용자, 작성자만 삭제 가능)
- **설명**: 댓글 삭제

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (204 No Content)
```json
{
  "message": "댓글이 삭제되었습니다."
}
```

#### Error Response (403 Forbidden)
```json
{
  "error": "권한이 없습니다."
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "댓글을 찾을 수 없습니다."
}
```

---

## Finance Infos (금융 정보 게시판)

### 1. 게시글 목록 조회

- **URL**: `/api/finance_infos/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 금융 정보 게시글 목록 조회 (최신순 정렬)

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "title": "2024년 금융 트렌드",
    "content": "내용...",
    "username": "admin",
    "created_at": "2025-12-23T10:00:00Z",
    "like_count": 5,
    "comment_count": 3
  },
  {
    "id": 2,
    "title": "적금 vs 예금 비교",
    "content": "내용...",
    "username": "admin",
    "created_at": "2025-12-22T15:30:00Z",
    "like_count": 10,
    "comment_count": 7
  }
]
```

---

### 2. 게시글 작성

- **URL**: `/api/finance_infos/`
- **Method**: `POST`
- **인증**: 필요 (관리자만)
- **권한**: `is_staff = True`
- **설명**: 새로운 금융 정보 게시글 작성

#### Request Headers
```
Authorization: Token {admin_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "새로운 금융 정보",
  "content": "게시글 내용입니다."
}
```

#### Response (201 Created)
```json
{
  "id": 3,
  "title": "새로운 금융 정보",
  "content": "게시글 내용입니다.",
  "username": "admin",
  "created_at": "2025-12-23T11:00:00Z",
  "updated_at": "2025-12-23T11:00:00Z",
  "like_count": 0,
  "comment_count": 0
}
```

#### Error Response (403 Forbidden)
```json
{
  "detail": "이 작업을 수행할 권한이 없습니다."
}
```

---

### 3. 게시글 상세 조회

- **URL**: `/api/finance_infos/{article_pk}/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 특정 게시글 상세 정보 조회 (댓글 포함)

#### Response (200 OK)
```json
{
  "id": 1,
  "title": "2024년 금융 트렌드",
  "content": "상세 내용...",
  "username": "admin",
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T10:00:00Z",
  "like_count": 5,
  "is_liked": true,
  "comments": [
    {
      "id": 1,
      "content": "유익한 정보 감사합니다!",
      "username": "user1",
      "article": 1,
      "created_at": "2025-12-23T10:30:00Z"
    },
    {
      "id": 2,
      "content": "도움이 많이 되었어요.",
      "username": "user2",
      "article": 1,
      "created_at": "2025-12-23T11:00:00Z"
    }
  ],
  "comment_count": 2
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

---

### 4. 게시글 수정

- **URL**: `/api/finance_infos/{article_pk}/`
- **Method**: `PUT`
- **인증**: 필요 (관리자만)
- **설명**: 게시글 수정

#### Request Headers
```
Authorization: Token {admin_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "title": "수정된 제목",
  "content": "수정된 내용",
  "username": "admin",
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z"
}
```

#### Error Response (403 Forbidden)
```json
{
  "error": "권한이 없습니다."
}
```

---

### 5. 게시글 삭제

- **URL**: `/api/finance_infos/{article_pk}/`
- **Method**: `DELETE`
- **인증**: 필요 (관리자만)
- **설명**: 게시글 삭제

#### Request Headers
```
Authorization: Token {admin_token}
```

#### Response (204 No Content)
```json
{
  "message": "게시글이 삭제되었습니다."
}
```

---

### 6. 게시글 좋아요 토글

- **URL**: `/api/finance_infos/{article_pk}/like/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 게시글 좋아요 추가/취소

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
**좋아요 추가 시:**
```json
{
  "message": "좋아요를 눌렀습니다.",
  "is_liked": true
}
```

**좋아요 취소 시:**
```json
{
  "message": "좋아요가 취소되었습니다.",
  "is_liked": false
}
```

---

### 7. 댓글 작성

- **URL**: `/api/finance_infos/{article_pk}/comments/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 게시글에 댓글 작성

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "content": "댓글 내용입니다."
}
```

#### Response (201 Created)
```json
{
  "id": 3,
  "content": "댓글 내용입니다.",
  "username": "user1",
  "article": 1,
  "created_at": "2025-12-23T12:00:00Z"
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "게시글을 찾을 수 없습니다."
}
```

---

## Finance News (뉴스 크롤링)

### 1. 뉴스 목록 조회

- **URL**: `/api/finance_news/news/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 크롤링된 금융 뉴스 목록 조회

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "title": "한국은행 기준금리 동결",
    "press": "한국경제",
    "published_date": "2025-12-23T09:00:00Z",
    "link": "https://news.naver.com/..."
  },
  {
    "id": 2,
    "title": "금융시장 전망",
    "press": "매일경제",
    "published_date": "2025-12-23T08:30:00Z",
    "link": "https://news.naver.com/..."
  }
]
```

---

### 2. 뉴스 상세 조회

- **URL**: `/api/finance_news/news/{news_pk}/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 특정 뉴스 기사 상세 조회

#### Response (200 OK)
```json
{
  "id": 1,
  "title": "한국은행 기준금리 동결",
  "content": "한국은행이 기준금리를 현행 3.5%로 동결했다...",
  "link": "https://news.naver.com/...",
  "published_date": "2025-12-23T09:00:00Z",
  "press": "한국경제",
  "crawled_at": "2025-12-23T10:00:00Z"
}
```

#### Error Response (404 Not Found)
```json
{
  "error": "기사를 찾을 수 없습니다."
}
```

---

### 3. 뉴스 크롤링 실행

- **URL**: `/api/finance_news/news/crawl/`
- **Method**: `POST`
- **인증**: 필요 (관리자만)
- **설명**: 네이버 뉴스 API로 금융 뉴스 크롤링

#### Request Headers
```
Authorization: Token {admin_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "query": "금융",
  "display": 10
}
```

**필드 설명:**
- `query`: 검색 키워드 (기본값: "금융")
- `display`: 크롤링할 기사 개수 (기본값: 10, 최대: 100)

#### Response (200 OK)
```json
{
  "success": true,
  "crawled_count": 10,
  "message": "10개의 기사를 크롤링했습니다."
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "message": "크롤링 실패: API 키가 유효하지 않습니다."
}
```

---

### 4. 기사 요약 (AI)

- **URL**: `/api/finance_news/news/{news_pk}/summary/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: GPT-4o를 사용하여 특정 기사 요약

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "success": true,
  "article_id": 1,
  "article_title": "한국은행 기준금리 동결",
  "article_link": "https://news.naver.com/...",
  "summary": "# 📰 기사 요약\n\n## 🔑 핵심 내용 (3줄 요약)\n1. 한국은행이 기준금리를 3.5%로 동결했습니다.\n2. 물가 상승세가 둔화되고 있으나 여전히 불확실성이 존재합니다.\n3. 다음 통화정책회의에서는 인하 가능성도 열어두고 있습니다.\n\n## 📊 주요 수치/데이터\n- 현재 기준금리: 3.5%\n- 물가상승률: 2.3%\n\n## 💡 시사점\n금리 동결로 대출 이자 부담은 당분간 유지될 전망입니다."
}
```

#### Error Response (400 Bad Request)
```json
{
  "success": false,
  "error": "content_too_short",
  "message": "요약할 수 있는 충분한 내용이 없습니다."
}
```

---

### 5. 최신 기사 종합 요약 (AI)

- **URL**: `/api/finance_news/news/daily-summary/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 최신 금융 기사 5개를 종합 요약

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body (선택)
```json
{
  "count": 5
}
```

**필드 설명:**
- `count`: 요약할 기사 개수 (기본값: 5, 최대: 10)

#### Response (200 OK)
```json
{
  "success": true,
  "article_count": 5,
  "summary": "# 📰 오늘의 금융 뉴스 브리핑\n\n## 🔥 주요 이슈\n오늘 금융시장의 가장 큰 화두는 한국은행의 금리 동결 결정입니다...\n\n## 📊 시장 동향\n...\n\n## 💡 투자자 관점\n..."
}
```

#### Error Response (404 Not Found)
```json
{
  "success": false,
  "error": "no_articles",
  "message": "요약할 기사가 없습니다."
}
```

---

## Deposits (예금/적금)

### 1. 예금 상품 차트 데이터

- **URL**: `/api/deposits/{fin_prdt_cd}/chart/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 특정 예금 상품의 금리 차트 데이터 제공

#### Response (200 OK)
```json
{
  "product_name": "우리 SUPER정기예금",
  "bank_name": "우리은행",
  "labels": ["6개월", "12개월", "24개월"],
  "basic_rates": [3.0, 3.5, 4.0],
  "max_rates": [3.5, 4.0, 4.5]
}
```

---

### 2. 적금 상품 차트 데이터

- **URL**: `/api/savings/{fin_prdt_cd}/chart/`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 특정 적금 상품의 금리 차트 데이터 제공

#### Response (200 OK)
```json
{
  "product_name": "신한 청년희망적금",
  "bank_name": "신한은행",
  "labels": ["6개월", "12개월", "24개월"],
  "basic_rates": [3.5, 4.0, 4.5],
  "max_rates": [4.0, 4.5, 5.0]
}
```

---

### 3. 여러 상품 금리 비교

- **URL**: `/api/compare/chart/?products=WR0001B&products=KB001&save_trm=12`
- **Method**: `GET`
- **인증**: 불필요
- **설명**: 여러 상품의 금리 비교 데이터

#### Query Parameters
- `products`: 비교할 상품 코드 (여러 개 가능)
- `save_trm`: 비교 기간 (개월, 기본값: 12)

#### Response (200 OK)
```json
{
  "labels": ["우리은행\n우리 SUPER정기예금", "국민은행\nKB Star 정기예금"],
  "basic_rates": [3.5, 3.3],
  "max_rates": [4.0, 3.8]
}
```

---

## Gold Prices (현물 자산)

### 1. 금/은 시세 데이터 조회

- **URL**: `/api/gold_prices/prices/`
- **Method**: `GET`
- **인증**: 불필요 (또는 설정에 따라 다름)
- **설명**: 서버 내 저장된 엑셀 파일(`Gold_prices.xlsx`, `Silver_prices.xlsx`)을 로드하여 금 또는 은의 과거 시세 데이터를 조회합니다. 기간 필터링이 가능하며, 데이터 정제 및 보간 처리가 완료된 리스트를 반환합니다.

#### Response (200 OK)
```json
{
  "asset": "gold",
  "count": 2,
  "data": [
    {
      "Date": "2024-01-02",
      "Price": 2063.40,
      "interpolated": false
    },
    {
      "Date": "2024-01-03",
      "Price": 2042.10,
      "interpolated": false
    }
  ]
}
```

**필드 설명:**
- `asset`: 조회된 자산의 종류 (gold / silver)
- `count`: 결과 데이터의 총 개수
- `data`: 시세 상세 내역 리스트
- `Date`: 시세 기준 날짜 (YYYY-MM-DD)
- `Price`: 해당 날짜의 종가 (숫자형)

(기타 필드는 clean_and_interpolate_prices 결과에 따라 추가될 수 있음)

#### Error Response (400 Bad Request)

```JSON

{
  "error": "잘못된 자산 유형입니다."
}
```

---

## Quizzes (퀴즈)

### 1. 오늘의 퀴즈 조회

- **URL**: `/api/quizzes/today/`
- **Method**: `GET`
- **인증**: 선택적 (로그인 시 참여 여부 확인 가능)
- **설명**: 1년 중 해당 날짜(Day of Year)를 기준으로 매일 바뀌는 '오늘의 퀴즈'를 조회합니다. 로그인한 사용자의 경우, 오늘 해당 퀴즈에 이미 참여했는지 여부(`has_attended`)를 함께 반환합니다.

#### Request Headers
Authorization: Token {your_token} (선택 사항)


#### Response (200 OK)
```json
{
  "id": 15,
  "question": "금(Gold)의 원소 기호는 무엇인가요?",
  "options": ["Au", "Ag", "Fe", "Cu"],
  "answer": "Au",
  "explanation": "금의 원소 기호는 라틴어 Aurum에서 유래한 Au입니다.",
  "has_attended": false
}
```

**필드 설명:**
- `id`: 퀴즈 고유 ID
- `question`: 퀴즈 질문 내용
- `options`: 퀴즈 보기 리스트
- `answer`: 정답
- `explanation`: 퀴즈 해설
- `has_attended`: 오늘 출석 체크(퀴즈 참여) 완료 여부

---

### 2. 퀴즈 참여 (출석 체크)
- **URL**: /api/quizzes/attendance/
- **Method**: POST
- **인증**: 필요 (로그인 사용자)
- **설명**: 오늘의 퀴즈에 대한 정답을 제출하거나 참여하여 출석 체크를 완료합니다. 하루에 한 번만 참여 가능합니다.

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```JSON

{
  "quiz_id": 15
}
```

#### Response (201 Created)
```JSON

{
  "message": "출석체크 완료!"
}
```

#### Error Response (400 Bad Request)
이미 오늘 출석 체크를 완료한 경우:

```JSON

{
  "message": "이미 참여했습니다."
}
```

---

## AI Services (AI 기능)

### 1. 자산 진단

- **URL**: `/api/ais/diagnosis/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: GPT-4o를 사용하여 사용자의 자산 포트폴리오 분석 및 맞춤형 조언 제공

#### Request Headers
```
Authorization: Token {your_token}
Content-Type: application/json
```

#### Request Body
```json
{
  "totalAssets": 50000000,
  "totalCash": 30000000,
  "totalInvest": 20000000,
  "totalDebt": 5000000,
  "netWorth": 45000000,
  "income": 5000000,
  "expense": 3000000,
  "sections": [
    {
      "label": "현금성 자산",
      "total": 30000000,
      "groups": [
        {
          "categoryName": "예금",
          "totalValue": 20000000,
          "items": [
            {
              "name": "우리은행 예금",
              "current_value": 20000000
            }
          ]
        }
      ]
    }
  ]
}
```

**필드 설명:**
- `totalAssets`: 총 자산 (현금 + 투자)
- `totalCash`: 현금성 자산 합계
- `totalInvest`: 투자 자산 합계
- `totalDebt`: 총 부채
- `netWorth`: 순자산 (자산 - 부채)
- `income`: 월 소득
- `expense`: 월 지출
- `sections`: 상세 자산 내역 (계층 구조)

#### Response (200 OK)
```json
{
  "success": true,
  "sections": [
    {
      "title": "💰 자산 진단 리포트",
      "content": "고객님의 재무 상태를 종합적으로 분석한 결과입니다.",
      "is_main": true
    },
    {
      "title": "📊 포트폴리오 분석",
      "content": "현재 고객님의 총 자산은 5,000만원으로 구성되어 있으며, 현금 비중이 60%로 안정적입니다. 투자 자산은 40%를 차지하고 있어 균형잡힌 포트폴리오를 유지하고 있습니다.",
      "is_main": false
    },
    {
      "title": "💪 강점",
      "content": "1. 부채가 500만원으로 총 자산의 10%에 불과하여 재무 건전성이 우수합니다.\n2. 월 소득 대비 지출이 60% 수준으로 저축 여력이 충분합니다.\n3. 현금과 투자 자산이 적절히 분산되어 있습니다.",
      "is_main": false
    },
    {
      "title": "⚠️ 개선이 필요한 부분",
      "content": "현금 비중이 60%로 다소 높아 인플레이션 리스크에 노출되어 있습니다. 안전 자산을 유지하면서도 일부는 수익률이 높은 상품으로 전환을 고려해보세요.",
      "is_main": false
    },
    {
      "title": "💡 맞춤 실행 제안",
      "content": "1. 현금성 자산의 20%(약 600만원)을 저위험 채권형 펀드나 배당주 ETF에 투자\n2. 월 여유 자금 50만원을 적금으로 꾸준히 적립\n3. 부채 500만원은 금리가 높다면 조기 상환 고려",
      "is_main": false
    },
    {
      "title": "📈 기대 효과",
      "content": "제안사항을 실행하시면 연간 약 150만원의 추가 수익을 기대할 수 있으며, 1년 후 순자산이 약 4,800만원으로 증가할 것으로 예상됩니다.",
      "is_main": false
    }
  ]
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "error": "GPT 진단 중 오류가 발생했습니다: API rate limit exceeded"
}
```

---

### 2. 금융 운세

- **URL**: `/api/ais/luck/`
- **Method**: `POST`
- **인증**: 필요 (로그인 사용자)
- **설명**: 사용자의 생년월일 기반 오늘의 금융 운세 생성

#### Request Headers
```
Authorization: Token {your_token}
```

#### Response (200 OK)
```json
{
  "success": true,
  "luck_message": "# 🍀 오늘의 금융 운세\n\n## 💰 오늘의 재물운\n1990년생이신 35세의 당신, 오늘은 중장기 투자에 행운이 따르는 날입니다. 특히 안정적인 배당주나 채권에 관심을 가져보세요.\n\n## 💳 추천 금융 활동\n1. 적금 가입을 고려해보세요. 오늘 가입하면 좋은 결과가 있을 것입니다.\n2. 불필요한 구독 서비스를 정리하는 것도 좋습니다.\n\n## 🎯 럭키 넘버\n오늘의 행운의 숫자는 7입니다. 7개월 적금이나 7%대 금리 상품을 찾아보세요.\n\n## 💡 한 줄 조언\n작은 저축이 큰 미래를 만듭니다. 오늘부터 시작하세요!"
}

#### Error Response (400 Bad Request)
**생년월일이 없는 경우:**
```json
{
  "success": false,
  "error": "birth_date_required",
  "message": "생년월일 정보가 필요합니다. 프로필 설정에서 생년월일을 입력해주세요."
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "success": false,
  "error": "api_error",
  "message": "운세 생성 중 오류가 발생했습니다: Connection timeout"
}
```

---

## 공통 에러 응답

### 401 Unauthorized (인증 실패)
```json
{
  "detail": "Authentication credentials were not provided."
}
```
또는
```json
{
  "detail": "Invalid token."
}
```

### 403 Forbidden (권한 없음)
```json
{
  "detail": "이 작업을 수행할 권한이 없습니다."
}
```

### 404 Not Found (리소스 없음)
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error (서버 오류)
```json
{
  "error": "서버 오류가 발생했습니다."
}
```

---

## 인증 방법

모든 인증이 필요한 API는 HTTP Header에 Token을 포함해야 합니다.

Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

### 토큰 발급
1. 회원가입 시 자동 발급
2. 로그인 시 발급

### 토큰 사용 예시 (JavaScript)
```javascript
const token = localStorage.getItem('token')

axios.get('/api/accounts/profile/', {
  headers: {
    'Authorization': `Token ${token}`
  }
})
```

---

## 개발 환경 정보

- **Base URL**: `http://127.0.0.1:8000`
- **API Prefix**: `/api/`
- **인증 방식**: Token Authentication
- **응답 형식**: JSON
- **문자 인코딩**: UTF-8

---

## 주의사항

1. 모든 날짜/시간은 **ISO 8601** 형식 (예: `2025-12-23T10:00:00Z`)
2. 금액은 **숫자** 타입 (콤마 없음)
3. 이미지 업로드 시 **multipart/form-data** 사용
4. 토큰은 안전하게 보관하고 노출 금지
5. API 요청 실패 시 에러 메시지 확인