<template>
  <div class="board-container">
    <div class="board-header">
      <div class="header-content">
        <h1 class="board-title">❤️ 좋아요한 게시글</h1>
        <p class="board-subtitle">내가 좋아요 표시한 게시글을 모아보세요</p>
      </div>
    </div>

    <div class="board-stats">
      <span class="total-count">
        총 <strong>{{ likedPosts.length }}</strong>개의 글
      </span>
    </div>

    <div class="post-list">
      <div
        v-for="post in likedPosts"
        :key="post.id"
        class="post-item"
        @click="goToDetail(post)"
      >
        <div class="post-main">
          <div class="post-title-area">
            <span v-if="post.is_notice" class="notice-badge">공지</span>
            <h3 class="post-title">{{ post.title }}</h3>
            <span v-if="post.comment_count > 0" class="comment-count">[{{ post.comment_count }}]</span>
          </div>
          <p class="post-preview">{{ post.content_preview }}</p>
          <div class="post-meta">
            <span class="author">{{ post.author }}</span>
            <span class="date">{{ formatDate(post.created_at) }}</span>
            <span class="views">조회 {{ post.view_count }}</span>
          </div>
        </div>
      </div>

      <div v-if="likedPosts.length === 0" class="empty-state">
        <p>아직 좋아요한 게시글이 없습니다.</p>
        <button class="explore-btn" @click="$router.push({ name: 'board-list', params: { type: 'free' } })">
          게시판 둘러보기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useBoardStore } from '@/stores/board'

const router = useRouter()
const boardStore = useBoardStore()

const likedPosts = computed(() => boardStore.getLikedPosts())

const goToDetail = (post) => {
  // 게시글에 포함된 boardType 사용
  const boardType = post.boardType || 'free'

  router.push({ name: 'board-detail', params: { type: boardType, id: post.id } })
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
  border-bottom: 2px solid #ff6b6b;
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

.board-stats {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff5f5;
  border-radius: 10px;
}

.total-count {
  font-size: 14px;
  color: #666;
}

.total-count strong {
  color: #ff6b6b;
  font-size: 16px;
}

.post-list {
  min-height: 400px;
}

.post-item {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 12px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.post-item:hover {
  border-color: #ff6b6b;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.1);
  transform: translateY(-2px);
}

.post-main {
  flex: 1;
}

.post-title-area {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.notice-badge {
  background-color: #ff6b6b;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}

.post-title {
  font-size: 17px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.comment-count {
  color: #ff6b6b;
  font-size: 15px;
  font-weight: 600;
}

.post-preview {
  color: #666;
  font-size: 14px;
  margin: 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.post-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #999;
  margin-top: 10px;
}

.post-meta .author {
  font-weight: 600;
  color: #555;
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

.explore-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.explore-btn:hover {
  background-color: #ff5252;
}
</style>
