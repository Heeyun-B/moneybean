<template>
  <div class="detail-container">
    <div v-if="isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>게시글을 불러오는 중...</p>
    </div>

    <div v-else-if="post" class="detail-content">
      <div class="post-header">
        <div class="header-top">
          <button class="back-btn" @click="goBack">← 목록으로</button>
          <div v-if="isAuthor" class="post-actions">
            <button class="action-btn edit-btn" @click="editPost">수정</button>
            <button class="action-btn delete-btn" @click="deletePost">삭제</button>
          </div>
        </div>

        <h1 class="post-title">
          <span v-if="post.is_notice" class="notice-badge">공지</span>
          {{ post.title }}
        </h1>

        <div class="post-meta">
          <div class="meta-left">
            <span class="author">{{ post.author }}</span>
            <span class="date">작성 {{ formatDate(post.created_at) }}</span>
            <span v-if="post.updated_at && post.updated_at !== post.created_at" class="date updated">
              수정 {{ formatDate(post.updated_at) }}
            </span>
          </div>
          <div class="meta-right">
            <button
              v-if="authStore.isAuthenticated"
              class="like-btn"
              :class="{ liked: boardStore.isLiked(boardType, post.id) }"
              @click="handleLike"
            >
              {{ boardStore.isLiked(boardType, post.id) ? '❤️' : '🤍' }} {{ post.like_count || 0 }}
            </button>
          </div>
        </div>
      </div>

      <div class="post-body">
        <div v-if="boardType === 'news' && post.link" class="news-link-banner">
          <a :href="post.link" target="_blank" rel="noopener noreferrer" class="original-link-btn">
            📰 원문 기사 보기
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
        <div class="post-content notion-style" v-html="formattedContent"></div>
      </div>

      <div v-if="boardType !== 'news'" class="comment-section">
        <h3 class="comment-title">
          댓글 <span class="comment-count">{{ sortedComments.length }}</span>
        </h3>

        <div v-if="canComment" class="comment-write">
          <textarea
            v-model="newComment"
            placeholder="댓글을 작성해주세요"
            class="comment-textarea"
            rows="3"
          ></textarea>
          <button class="comment-submit-btn" @click="submitComment">
            댓글 작성
          </button>
        </div>

        <div v-else class="login-required-comment">
          <p>댓글을 작성하려면 로그인이 필요합니다.</p>
          <button class="login-link-btn" @click="$router.push('/login')">
            로그인하기
          </button>
        </div>

        <div class="comment-list">
          <div
            v-for="comment in sortedComments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <div class="comment-author-wrapper">
                <span class="comment-author">{{ comment.author }}</span>
                <span v-if="post && comment.author === post.author" class="author-badge">작성자</span>
              </div>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
            <div class="comment-footer">
              <button
                v-if="isCommentAuthor(comment)"
                class="comment-delete-btn"
                @click="deleteComment(comment.id)"
              >
                삭제
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="error-state">
      <p>게시글을 찾을 수 없습니다.</p>
      <button class="back-btn" @click="goBack">목록으로 돌아가기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBoardStore } from '@/stores/board'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const boardStore = useBoardStore()

const boardType = ref(route.params.type)
const postId = ref(route.params.id)
const isLoading = ref(false)
const newComment = ref('')

const post = computed(() => boardStore.getPost(boardType.value, postId.value))
const comments = computed(() => boardStore.getComments(postId.value))

const sortedComments = computed(() => {
  return [...comments.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

const isAuthor = computed(() => {
  if (!authStore.isAuthenticated || !post.value) return false
  if (boardType.value === 'news') return false
  return post.value.author === authStore.userNickname
})

const canComment = computed(() => {
  if (!authStore.isAuthenticated) return false
  return boardType.value !== 'news'
})

const isCommentAuthor = (comment) => {
  if (!authStore.isAuthenticated) return false
  return comment.author === authStore.userNickname
}

const formattedContent = computed(() => {
  if (!post.value) return ''
  const rawHtml = marked(post.value.content, { breaks: true, gfm: true })
  return DOMPurify.sanitize(rawHtml)
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  })
}

const goBack = () => {
  router.push({ name: 'board-list', params: { type: boardType.value } })
}

const editPost = () => {
  router.push({ name: 'board-edit', params: { type: boardType.value, id: postId.value } })
}

const deletePost = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await boardStore.deletePost(boardType.value, postId.value)
    alert('게시글이 삭제되었습니다.')
    goBack()
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    alert('게시글 삭제에 실패했습니다.')
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }
  try {
    await boardStore.createComment(boardType.value, postId.value, {
      content: newComment.value,
      author: authStore.userNickname
    })
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성에 실패했습니다.')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return
  try {
    await boardStore.deleteComment(boardType.value, commentId)
  } catch (error) {
    console.error('댓글 삭제 실패:', error)
    alert('댓글 삭제에 실패했습니다.')
  }
}

const handleLike = async () => {
  await boardStore.toggleLike(boardType.value, post.value.id)
}

const loadPost = async () => {
  isLoading.value = true
  try {
    await boardStore.fetchPostDetail(boardType.value, postId.value)
    await boardStore.fetchComments(postId.value)
  } catch (error) {
    console.error('게시글 로딩 실패:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadPost()
})
</script>

<style scoped>
.detail-container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.loading-state, .error-state { text-align: center; padding: 80px 20px; color: #999; }
.spinner { border: 3px solid #f3f3f3; border-top: 3px solid #00a651; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.detail-content { background-color: white; border: 1px solid #eee; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.post-header { padding: 30px; border-bottom: 1px solid #eee; }
.header-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.back-btn { background-color: #f5f5f5; border: none; padding: 8px 16px; border-radius: 6px; font-size: 14px; color: #666; cursor: pointer; transition: all 0.2s; }
.back-btn:hover { background-color: #e0e0e0; }
.post-actions { display: flex; gap: 8px; }
.action-btn { padding: 8px 16px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; transition: all 0.2s; }
.edit-btn { background-color: #00a651; color: white; }
.edit-btn:hover { background-color: #008e45; }
.delete-btn { background-color: #ff6b6b; color: white; }
.delete-btn:hover { background-color: #ff5252; }
.post-title { font-size: 26px; font-weight: 700; color: #333; margin: 0 0 15px 0; line-height: 1.4; }
.notice-badge { background-color: #ff6b6b; color: white; font-size: 13px; font-weight: 700; padding: 4px 10px; border-radius: 4px; margin-right: 8px; vertical-align: middle; }
.post-meta { display: flex; justify-content: space-between; align-items: center; font-size: 14px; color: #999; }
.meta-left, .meta-right { display: flex; gap: 12px; align-items: center; }
.author { font-weight: 600; color: #555; }
.like-btn { background: white; border: 1px solid #ddd; padding: 6px 12px; border-radius: 20px; font-size: 13px; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 4px; }
.like-btn:hover { background: #f8f8f8; border-color: #ff6b6b; }
.like-btn.liked { background: #fff0f0; border-color: #ff6b6b; color: #ff6b6b; }
.date.updated { color: #00a651; font-weight: 500; }
.post-body { padding: 40px 30px; min-height: 200px; height: auto; }
.comment-section { padding: 30px; background-color: #f8faf9; border-top: 1px solid #eee; }
.comment-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; color: #333; }
.comment-count { color: #00a651; margin-left: 4px; }
.comment-write { margin-bottom: 30px; }
.comment-write::after { content: ""; display: block; clear: both; }
.comment-textarea { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical; font-family: inherit; margin-bottom: 10px; box-sizing: border-box; background-color: white; }
.comment-textarea:focus { outline: none; border-color: #00a651; box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1); }
.comment-submit-btn { background-color: #00a651; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; float: right; }
.comment-submit-btn:hover { background-color: #008e45; }
.login-required-comment { text-align: center; padding: 30px; background-color: white; border-radius: 8px; margin-bottom: 20px; border: 1px solid #eee; }
.login-required-comment p { color: #666; margin-bottom: 15px; }
.login-link-btn { background-color: #00a651; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.login-link-btn:hover { background-color: #008e45; }
.comment-list { display: flex; flex-direction: column; gap: 15px; }
.comment-item { background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #eee; transition: border-color 0.2s; }
.comment-item:hover { border-color: #ddd; }
.comment-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 13px; align-items: center; }
.comment-author-wrapper { display: flex; align-items: center; gap: 6px; }
.comment-author { font-weight: 600; color: #555; }
.author-badge { background-color: #00a651; color: white; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
.comment-date { color: #999; }
.comment-content { font-size: 15px; line-height: 1.6; color: #333; margin: 0; white-space: pre-wrap; }
.comment-footer { display: flex; justify-content: flex-end; margin-top: 10px; }
.comment-delete-btn { background: none; border: none; color: #999; font-size: 13px; cursor: pointer; padding: 0; transition: color 0.2s; }
.comment-delete-btn:hover { color: #ff6b6b; text-decoration: underline; }

/* Notion Style CSS */
.notion-style {
  color: #37352f;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";
  line-height: 1.75;
  font-size: 16px;
  word-break: break-word;
}
.notion-style :deep(h1) { font-size: 1.875em; font-weight: 700; margin: 2rem 0 0.5rem; line-height: 1.3; }
.notion-style :deep(h2) { font-size: 1.5em; font-weight: 600; margin: 1.4em 0 0.3em; line-height: 1.3; padding-bottom: 6px; border-bottom: 1px solid rgba(55, 53, 47, 0.09); }
.notion-style :deep(h3) { font-size: 1.25em; font-weight: 600; margin: 1em 0 0.2em; line-height: 1.3; }
.notion-style :deep(p) { margin-bottom: 0.5em; min-height: 1em; }
.notion-style :deep(ul), .notion-style :deep(ol) { margin: 0.5em 0; padding-left: 1.5em; }
.notion-style :deep(li) { margin-bottom: 0.2em; }
.notion-style :deep(blockquote) { border-left: 3px solid #37352f; margin: 1em 0; padding-left: 1em; font-style: normal; color: inherit; opacity: 0.8; }
.notion-style :deep(code) { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; background: rgba(135,131,120,0.15); padding: 0.2em 0.4em; border-radius: 3px; font-size: 85%; color: #EB5757; }
.notion-style :deep(pre) { background: #f7f6f3; padding: 20px; border-radius: 3px; overflow-x: auto; margin: 1em 0; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; }
.notion-style :deep(pre code) { background: transparent; padding: 0; color: #37352f; font-size: 0.9em; }
.notion-style :deep(a) { color: inherit; text-decoration: underline; text-decoration-color: rgba(55, 53, 47, 0.4); text-underline-offset: 2px; }
.notion-style :deep(a:hover) { color: #00a651; text-decoration-color: #00a651; }
.notion-style :deep(hr) { margin: 2em 0; border: none; border-bottom: 1px solid rgba(55, 53, 47, 0.09); }
.notion-style :deep(table) { border-collapse: collapse; width: 100%; margin: 1em 0; }
.notion-style :deep(th), .notion-style :deep(td) { border: 1px solid #e0e0e0; padding: 8px 12px; text-align: left; }
.notion-style :deep(th) { background-color: #f7f6f3; font-weight: 600; }

/* News Link Banner */
.news-link-banner { margin-bottom: 20px; }
.original-link-btn {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, #00a651 0%, #008e45 100%);
  color: white; padding: 12px 24px; border-radius: 8px;
  text-decoration: none; font-weight: 600; font-size: 15px;
  transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0, 166, 81, 0.2);
}
.original-link-btn:hover {
  transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
  background: linear-gradient(135deg, #008e45 0%, #00a651 100%);
}
.original-link-btn svg { transition: transform 0.3s ease; }
.original-link-btn:hover svg { transform: translate(2px, -2px); }
</style>