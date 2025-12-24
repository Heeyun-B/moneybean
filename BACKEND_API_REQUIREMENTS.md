# 게시판 백엔드 API - 연동 완료 현황

## ✅ 완료된 API 연동

### 1. 자유게시판 (Free Board) - `/api/boards/`

#### 게시글 API
- ✅ `GET /api/boards/` - 게시글 목록 조회
- ✅ `POST /api/boards/` - 게시글 작성 (인증 필요)
- ✅ `GET /api/boards/articles/{id}/` - 게시글 상세 조회
- ✅ `PUT /api/boards/articles/{id}/` - 게시글 수정 (작성자만)
- ✅ `DELETE /api/boards/articles/{id}/` - 게시글 삭제 (작성자만)

#### 댓글 API
- ✅ `POST /api/boards/articles/{id}/comment_create/` - 댓글 작성 (인증 필요)
- ✅ `DELETE /api/boards/comments/{id}/` - 댓글 삭제 (작성자만)

#### 좋아요 API
- ✅ `POST /api/boards/info/{id}/like/` - 좋아요 토글 (인증 필요)

**응답 데이터 구조**
```json
{
  "id": 1,
  "title": "게시글 제목",
  "content": "게시글 내용",
  "username": "작성자닉네임",
  "created_at": "2025-12-23T10:00:00Z",
  "updated_at": "2025-12-23T12:00:00Z",
  "comment_count": 5,
  "like_count": 10,
  "is_liked": true,
  "comments": [
    {
      "id": 1,
      "content": "댓글 내용",
      "username": "댓글작성자",
      "created_at": "2025-12-23T10:30:00Z"
    }
  ]
}
```

### 2. 금융정보 (Finance Info) - `/api/finance_infos/`

#### 게시글 API
- ✅ `GET /api/finance_infos/` - 게시글 목록 조회
- ✅ `POST /api/finance_infos/` - 게시글 작성 (관리자만)
- ✅ `GET /api/finance_infos/info/{id}/` - 게시글 상세 조회
- ✅ `PUT /api/finance_infos/info/{id}/` - 게시글 수정 (관리자만)
- ✅ `DELETE /api/finance_infos/info/{id}/` - 게시글 삭제 (관리자만)

#### 댓글 API
- ✅ `POST /api/finance_infos/info/{id}/comment_create/` - 댓글 작성 (인증 필요)
- ✅ `DELETE /api/finance_infos/comments/{id}/` - 댓글 삭제 (작성자만)

#### 좋아요 API
- ✅ `POST /api/finance_infos/info/{id}/like/` - 좋아요 토글 (인증 필요)

**권한 관리**
- `IsAdminOrReadOnly` 퍼미션 적용 (읽기는 모두 가능, 쓰기는 관리자만)
- 댓글은 모든 인증된 사용자 작성 가능

### 3. 금융기사 (News) - 미구현

⚠️ 현재 프론트엔드에서 Mock 데이터로 처리 중입니다.

## 🔧 백엔드 모델 구조

### boards 앱 (자유게시판)
```python
# models.py
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### finance_infos 앱 (금융정보)
```python
# models.py
class ArticleInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles_infos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentInfo(models.Model):
    article = models.ForeignKey(ArticleInfo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 📝 프론트엔드 스토어 (board.js)

프론트엔드는 다음과 같은 API 매핑을 사용합니다:

```javascript
// 게시판 타입별 엔드포인트 매핑
{
  'free': '/api/boards/',           // 자유게시판
  'info': '/api/finance_infos/',     // 금융정보
  'news': 'Mock Data'                // 뉴스 (미구현)
}
```

## 🚀 주요 개선 사항

1. **댓글 시스템 개선**
   - ✅ 게시글 상세 조회 시 댓글 포함 (Serializer 연동)
   - ✅ 댓글 삭제 API 추가 (백엔드)

2. **좋아요 기능**
   - ✅ POST 한 번으로 토글 처리
   - ✅ `is_liked` 응답 추가 (현재 사용자의 좋아요 여부)
   - ✅ 좋아요 수 자동 계산

3. **권한 관리**
   - ✅ 자유게시판: `IsAuthenticatedOrReadOnly`
   - ✅ 금융정보: `IsAdminOrReadOnly` (custom permission)
   - ✅ 게시글 수정/삭제: 작성자 검증
   - ✅ 댓글 삭제: 작성자 검증

## ⚠️ 누락된 기능 (향후 추가 필요)

### 백엔드 추가 필요 사항
1. **조회수 (view_count)**
   - 현재 모델에 필드 없음
   - 필요 시 마이그레이션으로 추가 필요

2. **공지사항 (is_notice)**
   - 현재 모델에 필드 없음
   - 관리자가 지정할 수 있는 필드 추가 필요

3. **금융기사 앱**
   - 뉴스 크롤링 및 게시판 기능 미구현
   - 별도 앱 생성 필요

4. **페이지네이션**
   - 현재 프론트엔드에서 처리 중
   - 백엔드에서 구현 시 성능 개선 가능

5. **검색 기능**
   - 현재 프론트엔드에서 처리 중
   - 백엔드에서 구현 시 성능 개선 가능

6. **이미지/파일 업로드**
   - 현재 미구현
   - multipart/form-data 처리 추가 필요

## 🔐 인증 헤더 형식

```
Authorization: Token {token}
```

프론트엔드에서 axios 요청 시 자동으로 포함됩니다.

## 📌 테스트 방법

### 백엔드 서버 실행
```bash
cd back
python manage.py runserver
```

### 프론트엔드 서버 실행
```bash
cd front
npm run dev
```

### 테스트 시나리오
1. 로그인 후 자유게시판에서 글 작성
2. 게시글 상세 페이지에서 댓글 작성/삭제
3. 좋아요 버튼 클릭 (토글)
4. 관리자 계정으로 금융정보 게시판에서 글 작성
5. 일반 사용자가 금융정보 게시판 댓글 작성 가능 확인

## 📂 관련 파일

### 프론트엔드
- [front/src/stores/board.js](front/src/stores/board.js) - Pinia 스토어
- [front/src/views/Board/BoardListView.vue](front/src/views/Board/BoardListView.vue)
- [front/src/views/Board/BoardDetailView.vue](front/src/views/Board/BoardDetailView.vue)
- [front/src/views/Board/BoardWriteView.vue](front/src/views/Board/BoardWriteView.vue)

### 백엔드
- [back/boards/](back/boards/) - 자유게시판 앱
- [back/finance_infos/](back/finance_infos/) - 금융정보 앱
- [back/backend/urls.py](back/backend/urls.py) - 메인 URL 설정

## 💡 참고사항

1. **API 응답 필드명**
   - 백엔드: `username` (user.username)
   - 프론트엔드: `author` (내부적으로 매핑)

2. **댓글 조회**
   - 게시글 상세 조회 시 comments 배열로 포함됨
   - 별도 댓글 조회 API는 사용하지 않음

3. **좋아요 수 계산**
   - Serializer에서 자동 계산 (`like_users.count()`)
   - 추가 API 호출 불필요

4. **에러 처리**
   - API 실패 시 프론트엔드에서 Mock 데이터로 fallback
   - 개발 중 백엔드 없이도 테스트 가능
