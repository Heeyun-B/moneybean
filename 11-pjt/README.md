# 🎬 관심 종목 유튜브 검색 서비스

## 1. 프로젝트 개요

### 1.1 서비스 목표
YouTube Data API v3를 활용하여 관심 있는 주제의 영상을 검색하고, 영상 상세 정보를 확인하며, 필요한 경우 나중에 볼 영상으로 저장·삭제할 수 있는 기능을 제공합니다.  
Vue.js의 컴포넌트 구조, 비동기 API 처리, Local Storage 데이터 관리 방식까지 실무 흐름을 경험하는 것이 목적입니다.

### 1.2 주요 기능 정의

| 구분 | 핵심 기능 | 상세 설명 |
| --- | --- | --- |
| 검색 | YouTube 영상 검색 | 검색어 입력 → API 호출 → 결과 목록 출력 |
| 시청 | 영상 상세 페이지 | iframe 재생 + 제목, 채널명, 설명 표시 |
| 저장 | 나중에 볼 영상 관리 | Local Storage 기반 저장/삭제 기능 |

---

## 2. 기술 스택 (Technology Stack)

| 영역 | 기술 / 도구 | 비고 |
| --- | --- | --- |
| Frontend | Vue.js 3 | 컴포넌트 기반 SPA |
| API | YouTube Data API v3 | 영상 검색 및 상세조회 |
| 환경 | Node.js 24, Vite, Axios | 비동기 통신 및 빌드 |
| Storage | Local Storage | 영상 저장/삭제 |

---

## 3. 기능 소개 (Features)

### 3.1 🔍 영상 검색  
검색창에서 키워드를 입력하면 YouTube API의 `/search` 엔드포인트를 활용하여 검색 결과를 받아옵니다.

- 썸네일
- 영상 제목
- 채널명  
- 클릭 시 영상 상세 페이지로 이동

**구현 요소**
- Axios로 API 비동기 요청  
- VideoCard 컴포넌트로 리스트 단위 UI 구성  
- 검색어 입력 → 결과 렌더링 흐름 구현  

---

### 3.2 ▶️ 영상 상세 페이지  
선택한 영상은 `/video/:id` 경로에서 확인하며, `/videos` 엔드포인트로 상세 정보를 조회합니다.

표시되는 정보:
- iframe 영상 재생  
- 제목  
- 채널명  
- 설명  
- 나중에 볼 영상 저장/삭제 버튼  

**구현 요소**
- route.params.id로 비디오 ID 획득  
- 영상 상세정보 재요청  
- iframe을 통해 재생 UI 구성  

---

### 3.3 📌 나중에 볼 영상(Local Storage)  
영상 상세 화면에서 “나중에 보기” 버튼을 클릭하면 Local Storage에 다음 데이터를 저장합니다:

- videoId  
- title  
- thumbnail  

저장한 영상은 `/later` 페이지에서 확인할 수 있으며 삭제 버튼도 포함됩니다.

**구현 요소**
- Local Storage CRUD  
- 저장 여부에 따라 버튼 라벨 토글  
- 저장된 항목이 없을 때 안내 문구 표시  

---

## 4. 폴더 구조
```
src/
├─ components/
│ ├─ NavBar.vue
│ └─ VideoCard.vue
├─ views/
│ ├─ HomeView.vue
│ ├─ AboutView.vue
│ ├─ SearchView.vue
│ ├─ VideoDetailView.vue
│ └─ LaterView.vue
├─ router/
│ └─ index.js
├─ App.vue
└─ main.js
```

---

## 5. 프로젝트 회고 (Retrospection)

### 배운 점
- YouTube API의 요청 파라미터, 응답 구조(snippet, thumbnails 등)를 이해하는 과정이 중요했습니다.
- Vue 컴포넌트 기반 구조를 통해 공통 UI와 로직을 분리하는 방법을 익혔습니다.
- Local Storage를 활용한 간단한 상태 관리 경험을 통해 클라이언트 저장 방식의 특징을 이해했습니다.

### 어려웠던 점
- API 응답 구조가 중첩되어 있어 필요한 필드를 정확하게 파악하는 작업이 필요했습니다.
- 상세 페이지 이동 후 비동기 요청 타이밍 제어가 관건이었습니다.

### 개선할 점
- API 요청 중복을 줄이기 위한 캐싱 기능  
- UI 전환 효과 및 사용자 피드백 향상  
- 저장한 영상에 대한 태그/정렬 기능 추가 