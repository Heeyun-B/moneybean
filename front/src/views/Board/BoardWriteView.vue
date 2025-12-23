<template>
  <div class="write-container">
    <div class="write-header">
      <h1 class="write-title">{{ isEdit ? '게시글 수정' : '게시글 작성' }}</h1>
      <button class="cancel-btn" @click="goBack">취소</button>
    </div>

    <div class="write-form">
      <div class="form-group">
        <label for="title" class="form-label">제목</label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          placeholder="제목을 입력하세요"
          class="form-input"
          maxlength="100"
        >
        <span class="char-count">{{ formData.title.length }} / 100</span>
      </div>

      <div class="form-group">
        <div class="content-header">
          <label for="content" class="form-label">내용</label>
          <div class="preview-toggle">
            <button
              type="button"
              class="toggle-btn"
              :class="{ active: !showPreview }"
              @click="showPreview = false"
            >
              작성
            </button>
            <button
              type="button"
              class="toggle-btn"
              :class="{ active: showPreview }"
              @click="showPreview = true"
            >
              미리보기
            </button>
          </div>
        </div>
        
        <textarea
          v-show="!showPreview"
          id="content"
          v-model="formData.content"
          placeholder="내용을 입력하세요..."
          class="form-textarea"
          rows="15"
        ></textarea>
        
        <div 
          v-show="showPreview" 
          class="markdown-preview notion-style" 
          v-html="markdownPreview"
        ></div>
        
        <span class="char-count">{{ formData.content.length }}자</span>
      </div>

      <div v-if="canSetNotice" class="form-group checkbox-group">
        <label class="checkbox-label">
          <input
            v-model="formData.is_notice"
            type="checkbox"
            class="form-checkbox"
          >
          <span>공지사항으로 등록</span>
        </label>
      </div>

      <div class="form-actions">
        <button class="submit-btn" @click="submitPost">
          {{ isEdit ? '수정하기' : '작성하기' }}
        </button>
        <button class="cancel-action-btn" @click="goBack">
          취소
        </button>
      </div>
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
const isEdit = computed(() => !!postId.value)
const showPreview = ref(false)

// 태그, 이미지 관련 상태 제거
const formData = ref({
  title: '',
  content: '',
  is_notice: false,
})

const markdownPreview = computed(() => {
  if (!formData.value.content) return '<p class="empty-preview">내용을 입력하면 미리보기가 표시됩니다.</p>'
  const rawHtml = marked(formData.value.content, { breaks: true, gfm: true })
  return DOMPurify.sanitize(rawHtml)
})

const canSetNotice = computed(() => {
  return authStore.userRole === 'admin'
})

const goBack = () => {
  if (confirm('작성을 취소하시겠습니까?')) {
    if (isEdit.value) {
      router.push({ name: 'board-detail', params: { type: boardType.value, id: postId.value } })
    } else {
      router.push({ name: 'board-list', params: { type: boardType.value } })
    }
  }
}

const validateForm = () => {
  if (!formData.value.title.trim()) {
    alert('제목을 입력해주세요.')
    return false
  }
  if (!formData.value.content.trim()) {
    alert('내용을 입력해주세요.')
    return false
  }
  return true
}

const submitPost = async () => {
  if (!validateForm()) return

  try {
    // 태그, 이미지 관련 필드 전송 제거
    const postData = {
      title: formData.value.title.trim(),
      content: formData.value.content.trim(),
      is_notice: formData.value.is_notice,
      author: authStore.userNickname,
    }

    if (isEdit.value) {
      await boardStore.updatePost(boardType.value, postId.value, postData)
      alert('게시글이 수정되었습니다.')
      router.push({ name: 'board-detail', params: { type: boardType.value, id: postId.value } })
    } else {
      const newPostId = await boardStore.createPost(boardType.value, postData)
      alert('게시글이 작성되었습니다.')
      router.push({ name: 'board-detail', params: { type: boardType.value, id: newPostId } })
    }
  } catch (error) {
    console.error('게시글 저장 실패:', error)
    alert('게시글 저장에 실패했습니다.')
  }
}

const loadPost = async () => {
  if (!isEdit.value) return

  try {
    const post = await boardStore.fetchPostDetail(boardType.value, postId.value)
    
    if (post) {
      if (post.author !== authStore.userNickname) {
        alert('수정 권한이 없습니다.')
        router.push({ name: 'board-list', params: { type: boardType.value } })
        return
      }
      showPreview.value = false
      formData.value.title = post.title || ''
      formData.value.content = post.content || ''
      formData.value.is_notice = post.is_notice || false
      // 태그, 이미지 로드 로직 제거
    } else {
      alert('게시글을 찾을 수 없습니다.')
      goBack()
    }
  } catch (error) {
    console.error('게시글 로딩 실패:', error)
    alert('게시글을 불러오는데 실패했습니다.')
    goBack()
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }
  if (boardType.value === 'info' && !authStore.isStaff) {
    alert('작성 권한이 없습니다.')
    router.push({ name: 'board-list', params: { type: boardType.value } })
    return
  }
  if (boardType.value === 'news') {
    alert('금융기사는 작성할 수 없습니다.')
    router.push({ name: 'board-list', params: { type: 'news' } })
    return
  }
  loadPost()
})
</script>

<style scoped>
.write-container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.write-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #00a651; }
.write-title { font-size: 26px; font-weight: 700; color: #333; margin: 0; }
.cancel-btn { background-color: #f5f5f5; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; color: #666; cursor: pointer; transition: all 0.2s; }
.cancel-btn:hover { background-color: #e0e0e0; }
.write-form { background-color: white; padding: 40px; border: 1px solid #eee; border-radius: 12px; }
.form-group { margin-bottom: 30px; position: relative; }
.content-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.preview-toggle { display: flex; gap: 4px; background-color: #f5f5f5; padding: 4px; border-radius: 8px; }
.toggle-btn { padding: 6px 16px; border: none; background-color: transparent; color: #666; cursor: pointer; border-radius: 6px; font-size: 13px; font-weight: 500; transition: all 0.2s; }
.toggle-btn:hover { background-color: #e0e0e0; }
.toggle-btn.active { background-color: #00a651; color: white; }
.form-label { display: block; font-size: 15px; font-weight: 600; color: #333; }
.form-input, .form-textarea { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; font-family: inherit; transition: all 0.2s; box-sizing: border-box; }
.form-input:focus, .form-textarea:focus { outline: none; border-color: #00a651; box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1); }
.form-textarea { resize: vertical; line-height: 1.6; }
.char-count { position: absolute; right: 0; bottom: -20px; font-size: 12px; color: #999; }
.checkbox-group { margin-bottom: 40px; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 15px; color: #555; }
.form-checkbox { width: 18px; height: 18px; cursor: pointer; }
.form-actions { display: flex; gap: 12px; justify-content: center; margin-top: 40px; }
.submit-btn, .cancel-action-btn { padding: 14px 40px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.submit-btn { background-color: #00a651; color: white; }
.submit-btn:hover { background-color: #008e45; transform: translateY(-1px); }
.cancel-action-btn { background-color: #f5f5f5; color: #666; }
.cancel-action-btn:hover { background-color: #e0e0e0; }
.markdown-preview { min-height: 400px; padding: 40px; border: 1px solid #ddd; border-radius: 8px; background-color: #fff; }
.empty-preview { color: #999; text-align: center; padding: 60px 20px; font-size: 14px; }

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
</style>