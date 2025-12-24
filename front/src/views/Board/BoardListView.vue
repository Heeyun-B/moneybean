<template>
  <div class="board-container">
    <div class="board-header">
      <div class="header-content">
        <h1 class="board-title">{{ boardConfig.title }}</h1>
        <p class="board-subtitle">{{ boardConfig.subtitle }}</p>
      </div>
      <button
        v-if="canWrite"
        class="write-btn"
        @click="goToWrite"
      >
        글쓰기
      </button>
    </div>

    <div class="board-stats">
      <span class="total-count">
        총 <strong>{{ posts.length }}</strong>개의 글
      </span>
      <div class="search-box">
        <select v-model="searchType" class="search-select">
          <option value="title">제목</option>
          <option value="content">내용</option>
          <option value="author">작성자</option>
        </select>
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="검색어를 입력하세요"
          class="search-input"
          @keyup.enter="searchPosts"
        >
        <button class="search-btn" @click="searchPosts">🔍</button>
      </div>
    </div>

    <div class="post-list">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>게시글을 불러오는 중...</p>
      </div>

      <template v-else>
        <div
          v-for="post in displayedPosts"
          :key="post.id"
          class="post-item"
          @click="goToDetail(post.id)"
        >
          <div class="post-number">{{ post.id }}</div>
          <div class="post-main">
            <div class="post-title-area">
              <span v-if="post.is_notice" class="notice-badge">공지</span>
              <h3 class="post-title">{{ post.title }}</h3>
              <span v-if="boardType !== 'news' && post.comment_count > 0" class="comment-count">[{{ post.comment_count }}]</span>
            </div>
          </div>
          <div class="post-info">
            <span class="author" :class="{ 'news-press': boardType === 'news' }">
              {{ boardType === 'news' && post.press ? post.press : post.author }}
            </span>
          </div>
          <div class="post-date">
            <span>{{ formatDate(post.created_at) }}</span>
          </div>
          <div class="post-stats">
            <span class="stat-item">
              <span class="stat-icon">❤️</span>
              <span class="stat-value">{{ post.like_count || 0 }}</span>
            </span>
            <span v-if="boardType !== 'news'" class="stat-item">
              <span class="stat-icon">💬</span>
              <span class="stat-value">{{ post.comment_count || 0 }}</span>
            </span>
          </div>
        </div>

        <div v-if="displayedPosts.length === 0" class="empty-state">
          <p>아직 작성된 게시글이 없습니다.</p>
          <button v-if="canWrite" class="empty-write-btn" @click="goToWrite">
            첫 게시글 작성하기
          </button>
        </div>
      </template>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        이전
      </button>
      <button
        v-for="page in pageNumbers"
        :key="page"
        class="page-num"
        :class="{ active: page === currentPage }"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBoardStore } from '@/stores/board'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const boardStore = useBoardStore()

const boardType = computed(() => route.params.type || 'free')
const isLoading = ref(false)
const searchType = ref('title')
const searchKeyword = ref('')
const currentPage = ref(1)
const postsPerPage = 10

// 게시판 설정
const boardConfig = computed(() => {
  const configs = {
    free: {
      title: '자유게시판',
      subtitle: '자유롭게 소통하고 정보를 공유하세요',
      canWrite: authStore.isAuthenticated
    },
    news: {
      title: '금융기사',
      subtitle: '최신 금융 뉴스를 확인하세요',
      canWrite: false
    },
    info: {
      title: '금융정보',
      subtitle: '유용한 금융 정보와 꿀팁을 확인하세요',
      canWrite: authStore.isAuthenticated && authStore.isStaff
    }
  }
  return configs[boardType.value] || configs.free
})

const canWrite = computed(() => boardConfig.value.canWrite)

// 게시글 목록
const posts = computed(() => boardStore.getPosts(boardType.value))

// 검색된 게시글
const filteredPosts = computed(() => {
  if (!searchKeyword.value) return posts.value

  return posts.value.filter(post => {
    const keyword = searchKeyword.value.toLowerCase()
    if (searchType.value === 'title') {
      return post.title.toLowerCase().includes(keyword)
    } else if (searchType.value === 'content') {
      return post.content.toLowerCase().includes(keyword)
    } else if (searchType.value === 'author') {
      return post.author.toLowerCase().includes(keyword)
    }
    return false
  })
})

// 페이지네이션
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / postsPerPage))

const displayedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage
  const end = start + postsPerPage
  return filteredPosts.value.slice(start, end)
})

const pageNumbers = computed(() => {
  const pages = []
  const maxPages = 5
  let startPage = Math.max(1, currentPage.value - Math.floor(maxPages / 2))
  let endPage = Math.min(totalPages.value, startPage + maxPages - 1)

  if (endPage - startPage < maxPages - 1) {
    startPage = Math.max(1, endPage - maxPages + 1)
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  return pages
})

// 메서드
const searchPosts = () => {
  currentPage.value = 1
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToWrite = () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }
  router.push({ name: 'board-write', params: { type: boardType.value } })
}

const goToDetail = (id) => {
  router.push({ name: 'board-detail', params: { type: boardType.value, id } })
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const diffHours = Math.floor(diff / (1000 * 60 * 60))

  if (diffHours < 24) {
    if (diffHours < 1) {
      const diffMinutes = Math.floor(diff / (1000 * 60))
      return `${diffMinutes}분 전`
    }
    return `${diffHours}시간 전`
  }

  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const loadPosts = async () => {
  isLoading.value = true
  try {
    await boardStore.fetchPosts(boardType.value)
  } catch (error) {
    console.error('게시글 로딩 실패:', error)
    alert('게시글을 불러오는데 실패했습니다.')
  } finally {
    isLoading.value = false
  }
}

watch(() => route.params.type, (newType) => {
  if (newType) {
    currentPage.value = 1
    searchKeyword.value = ''
    loadPosts()
  }
})

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.board-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #00a651;
}

.header-content h1 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.board-subtitle {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.write-btn {
  background-color: #00a651;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.write-btn:hover {
  background-color: #008e45;
  transform: translateY(-1px);
}

.board-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8faf9;
  border-radius: 10px;
}

.total-count {
  font-size: 14px;
  color: #666;
}

.total-count strong {
  color: #00a651;
  font-size: 16px;
}

.search-box {
  display: flex;
  gap: 8px;
}

.search-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  cursor: pointer;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  width: 250px;
  outline: none;
}

.search-input:focus {
  border-color: #00a651;
}

.search-btn {
  background-color: white;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.search-btn:hover {
  background-color: #f5f5f5;
}

.post-list {
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
}

.post-item {
  display: grid;
  grid-template-columns: 80px 1fr 120px 140px 120px;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.2s;
  gap: 16px;
}

.post-item:last-child {
  border-bottom: none;
}

.post-item:hover {
  background-color: #f8fdf9;
}

.post-number {
  font-size: 14px;
  color: #999;
  font-weight: 500;
  text-align: center;
}

.post-main {
  flex: 1;
  min-width: 0;
}

.post-title-area {
  display: flex;
  align-items: center;
  gap: 8px;
}

.notice-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff5252);
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(255, 107, 107, 0.3);
}

.post-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.post-item:hover .post-title {
  color: #00a651;
}

.comment-count {
  color: #00a651;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.post-info {
  text-align: center;
}

.post-info .author {
  font-size: 14px;
  font-weight: 500;
  color: #555;
}

.post-info .author.news-press {
  color: #00a651;
  font-weight: 600;
}

.post-date {
  font-size: 13px;
  color: #999;
  text-align: center;
}

.post-stats {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: center;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-icon {
  font-size: 14px;
}

.stat-value {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  min-width: 20px;
  text-align: right;
}

.loading-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #00a651;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.empty-state p {
  font-size: 16px;
  margin-bottom: 20px;
}

.empty-write-btn {
  background-color: #00a651;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.empty-write-btn:hover {
  background-color: #008e45;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 40px;
}

.page-btn,
.page-num {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled),
.page-num:hover {
  background-color: #f5f5f5;
  border-color: #00a651;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-num.active {
  background-color: #00a651;
  color: white;
  border-color: #00a651;
  font-weight: 600;
}
</style>