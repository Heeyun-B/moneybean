<template>
  <div class="profile-container" v-if="profileData">
    <!-- 프로필 메인 카드 -->
    <div class="profile-main-card">
      <div class="card-bg">
        <div class="card-level-display">
          <div class="inline-level-tag-top" :class="currentLevel.class">
            <img :src="currentLevel.imgUrl" class="inline-level-img-top" alt="레벨 아이콘" />
            <span class="inline-level-name-top">{{ currentLevel.name }}</span>
          </div>
        </div>
      </div>
      <div class="user-content">
        <div class="avatar-box">
          <img
            :src="displayImageUrl"
            :key="imageKey"
            class="user-avatar"
            :class="{ 'editing-img': isEditing }"
            alt="프로필 이미지"
            @error="handleImageError"
          />
          <label v-if="isEditing" for="file-input" class="camera-overlay">
            <div class="camera-circle">
              <span>📷</span>
            </div>
          </label>
          <input
            id="file-input"
            type="file"
            @change="onFileChange"
            hidden
            accept="image/jpeg,image/png,image/jpg,image/webp"
          />
        </div>

        <div class="user-details">
          <template v-if="!isEditing">
            <div class="name-area">
              <h2 class="user-nickname">{{ profileData.nickname }}님</h2>
            </div>
            <div class="user-info-section">
              <p class="user-id">@{{ profileData.username }} <span class="divider">|</span> {{ profileData.email }}</p>
              <p v-if="profileData.birth_date" class="user-birth">🎂 {{ formatBirthDate(profileData.birth_date) }}</p>
              <button class="btn-toggle" @click="startEdit">프로필 수정하기</button>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 프로필 수정 폼 -->
    <div v-if="isEditing" class="edit-form-card">
      <div class="edit-form-header">
        <h3>프로필 수정</h3>
      </div>
      <div class="edit-inputs">
        <div class="input-group">
          <label class="input-label">닉네임</label>
          <input
            type="text"
            v-model="editNickname"
            class="input-field"
            maxlength="20"
            placeholder="닉네임을 입력하세요"
          />
        </div>

        <div class="input-group">
          <label class="input-label">생년월일</label>
          <div class="picker-group">
            <select v-model="birthYear" class="picker-select" aria-label="출생 연도">
              <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
            </select>
            <select v-model="birthMonth" class="picker-select" aria-label="출생 월">
              <option v-for="m in months" :key="m" :value="m">{{ m }}월</option>
            </select>
            <select v-model="birthDay" class="picker-select" aria-label="출생 일">
              <option v-for="d in days" :key="d" :value="d">{{ d }}일</option>
            </select>
          </div>
        </div>
      </div>
      <div class="edit-actions-row">
        <button class="btn-cancel" @click="cancelEdit">취소</button>
        <button class="btn-save" @click="handleUpdate" :disabled="isLoading">
          {{ isLoading ? '저장 중...' : '변경 완료' }}
        </button>
      </div>
    </div>

    <!-- 자산 섹션 -->
    <section class="asset-section" v-if="!isEditing">
      <div class="section-title">
        <h3>🏦 나의 가입 상품</h3>
      </div>
      <div class="asset-grid">
        <div class="asset-column">
          <div class="column-header">
            <span>💰 정기예금</span>
            <span class="count-tag">{{ profileData.deposit_subscriptions?.length || 0 }}</span>
          </div>
          <div v-if="profileData.deposit_subscriptions?.length > 0" class="product-list">
            <article
              v-for="item in profileData.deposit_subscriptions"
              :key="item.id"
              class="product-item clickable"
              @click="goToProductDetail('deposit', item.product_code)"
              role="button"
              tabindex="0"
              @keydown.enter="goToProductDetail('deposit', item.product_code)"
            >
              <div class="bank">{{ item.bank_name }}</div>
              <div class="title">{{ item.product_name }}</div>
              <div class="info">{{ item.interest_rate }}% | {{ item.save_term }}개월</div>
            </article>
          </div>
          <div v-else class="empty-box">가입된 예금이 없습니다.</div>
        </div>

        <div class="asset-column">
          <div class="column-header">
            <span>🐷 정기적금</span>
            <span class="count-tag">{{ profileData.saving_subscriptions?.length || 0 }}</span>
          </div>
          <div v-if="profileData.saving_subscriptions?.length > 0" class="product-list">
            <article
              v-for="item in profileData.saving_subscriptions"
              :key="item.id"
              class="product-item clickable"
              @click="goToProductDetail('saving', item.product_code)"
              role="button"
              tabindex="0"
              @keydown.enter="goToProductDetail('saving', item.product_code)"
            >
              <div class="bank">{{ item.bank_name }}</div>
              <div class="title">{{ item.product_name }}</div>
              <div class="info">{{ item.interest_rate }}% | {{ item.save_term }}개월</div>
            </article>
          </div>
          <div v-else class="empty-box">가입된 적금이 없습니다.</div>
        </div>
      </div>
    </section>

    <!-- 커뮤니티 섹션 -->
    <section class="community-section" v-if="!isEditing">
      <div class="section-title">
        <h3>📝 커뮤니티 활동</h3>
      </div>
      <div class="community-grid">
        <div class="community-column">
          <div class="column-header">
            <span>✍️ 내 게시글</span>
            <span class="count-tag">{{ myPosts.length }}</span>
          </div>
          <div v-if="myPosts.length > 0" class="post-mini-list">
            <article
              v-for="post in myPosts"
              :key="`${post.boardType}-${post.id}`"
              class="post-mini-item"
              @click="goToPost(post.boardType, post.id)"
              role="button"
              tabindex="0"
              @keydown.enter="goToPost(post.boardType, post.id)"
            >
              <div class="post-info">
                <span class="post-badge">{{ getBoardName(post.boardType) }}</span>
                <span class="post-title">{{ post.title }}</span>
                <span class="post-date">{{ formatDate(post.created_at) }}</span>
              </div>
            </article>
          </div>
          <div v-else class="empty-box">작성한 게시글이 없습니다.</div>
        </div>

        <div class="community-column">
          <div class="column-header">
            <span>💖 좋아요한 글</span>
            <span class="count-tag">{{ likedPosts.length }}</span>
          </div>
          <div v-if="likedPosts.length > 0" class="post-mini-list">
            <article
              v-for="post in likedPosts"
              :key="`${post.boardType}-${post.id}`"
              class="post-mini-item"
              @click="goToPost(post.boardType, post.id)"
              role="button"
              tabindex="0"
              @keydown.enter="goToPost(post.boardType, post.id)"
            >
              <div class="post-info">
                <span class="post-badge">{{ getBoardName(post.boardType) }}</span>
                <span class="post-title">{{ post.title }}</span>
                <span class="post-author">{{ post.author }}</span>
              </div>
              <span class="post-meta">❤️ {{ post.like_count || 0 }}</span>
            </article>
          </div>
          <div v-else class="empty-box">좋아요한 게시글이 없습니다.</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAssetStore } from '@/stores/asset'
import { useBoardStore } from '@/stores/board'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const assetStore = useAssetStore()
const boardStore = useBoardStore()

const profileData = ref(null)
const myPosts = ref([])
const likedPosts = ref([])
const isEditing = ref(false)
const isLoading = ref(false)
const imageKey = ref(Date.now())

// 생년월일 수정을 위한 상태
const editNickname = ref('')
const birthYear = ref('1995')
const birthMonth = ref('01')
const birthDay = ref('01')
const selectedFile = ref(null)
const previewUrl = ref(null)

const years = Array.from({ length: 100 }, (_, i) => String(2025 - i))
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const days = computed(() => {
  const lastDay = new Date(parseInt(birthYear.value), parseInt(birthMonth.value), 0).getDate()
  return Array.from({ length: lastDay }, (_, i) => String(i + 1).padStart(2, '0'))
})

// 레벨 정보
const currentLevel = ref({
  name: "콩",
  imgUrl: "",
  class: "lv-1"
})

// 이미지 경로 관리 (import.meta.url 사용)
const getLevelImgUrl = (imgName) => {
  try {
    return new URL(`../../assets/level_logos/${imgName}`, import.meta.url).href
  } catch (error) {
    console.error('레벨 이미지 로드 실패:', error)
    return ''
  }
}

const defaultImageUrl = computed(() => {
  try {
    return new URL('../../assets/logo_bean.png', import.meta.url).href
  } catch (error) {
    console.error('기본 이미지 로드 실패:', error)
    return ''
  }
})

// 프로필 이미지 표시 URL
const displayImageUrl = computed(() => {
  if (previewUrl.value) {
    return previewUrl.value
  }

  // profile_image_url 우선 사용 (절대 URL)
  if (profileData.value?.profile_image_url) {
    return `${profileData.value.profile_image_url}?t=${imageKey.value}`
  }

  // authStore의 profileImage 사용
  if (authStore.profileImage) {
    return `${authStore.profileImage}?t=${imageKey.value}`
  }

  return defaultImageUrl.value
})

// 계산된 balance (assetStore 우선)
const calculatedBalance = computed(() => {
  return assetStore.netWorth || profileData.value?.total_balance || 0
})

// 이미지 로드 실패 시 기본 이미지로 대체
const handleImageError = (event) => {
  event.target.src = defaultImageUrl.value
}

// 레벨 계산 로직
const calculateLevel = () => {
  const balance = calculatedBalance.value

  console.log('🎯 레벨 계산:', {
    assetStore_netWorth: assetStore.netWorth,
    profile_total_balance: profileData.value?.total_balance,
    final_balance: balance,
    timestamp: new Date().toISOString()
  })

  let levelData = { name: "콩", img: "level_bean.png", class: "lv-1" }

  if (balance >= 100000000) {
    levelData = { name: "돈나무", img: "level_money_tree.png", class: "lv-5" }
  } else if (balance >= 80000000) {
    levelData = { name: "나무", img: "level_tree.png", class: "lv-4" }
  } else if (balance >= 50000000) {
    levelData = { name: "가지", img: "level_branch.png", class: "lv-3" }
  } else if (balance >= 10000000) {
    levelData = { name: "새싹", img: "level_sprout.png", class: "lv-2" }
  }

  currentLevel.value = {
    ...levelData,
    imgUrl: getLevelImgUrl(levelData.img)
  }

  console.log('✅ 레벨 결정:', currentLevel.value.name, '(잔액:', balance.toLocaleString(), ')')
}

// calculatedBalance 변경 감지 (즉시 실행)
watch(calculatedBalance, (newVal, oldVal) => {
  console.log('👀 Balance 변경 감지:', { old: oldVal, new: newVal })
  nextTick(() => calculateLevel())
}, { immediate: true })

// assetStore.netWorth 변경 감지
watch(() => assetStore.netWorth, (newVal, oldVal) => {
  if (newVal !== oldVal && newVal !== undefined) {
    console.log('💰 netWorth 변경:', oldVal, '->', newVal)
    nextTick(() => calculateLevel())
  }
})

// 게시판 이름 반환
const getBoardName = (boardType) => {
  const boardNames = {
    'free': '자유',
    'info': '정보',
    'news': '뉴스'
  }
  return boardNames[boardType] || '게시판'
}

// 날짜 포맷 함수
const formatDate = (dateString) => {
  if (!dateString) return ''
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

const formatBirthDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 내가 작성한 글 가져오기
const fetchMyPosts = async () => {
  try {
    const boardTypes = ['free', 'info']
    const allPosts = []

    for (const boardType of boardTypes) {
      const posts = boardStore.getPosts(boardType)
      const myPostsInBoard = posts
        .filter(post => post.author === authStore.userNickname)
        .map(post => ({ ...post, boardType }))

      allPosts.push(...myPostsInBoard)
    }

    // 최신순 정렬
    myPosts.value = allPosts.sort((a, b) =>
      new Date(b.created_at) - new Date(a.created_at)
    )
  } catch (error) {
    console.error('내 게시글 로드 실패:', error)
    myPosts.value = []
  }
}

// 프로필 데이터 가져오기
const getProfile = async () => {
  try {
    const res = await axios.get(`${authStore.API_URL}/api/accounts/profile/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    profileData.value = res.data

    // 좋아요한 게시글 목록 가져오기
    likedPosts.value = boardStore.getLikedPosts()

    // 프로필 로드 후 레벨 재계산
    await nextTick()
    calculateLevel()
  } catch (error) {
    console.error('프로필 데이터 로드 실패:', error)
  }
}

// 초기 데이터 로드
onMounted(async () => {
  console.log('🚀 ProfileView 마운트')

  try {
    // 1. 자산 데이터 먼저 로드
    await assetStore.getAssets()
    console.log('💰 자산 로드 완료:', {
      netWorth: assetStore.netWorth,
      totalAssets: assetStore.totalAssets,
      totalDebt: assetStore.totalDebt
    })

    // 2. 게시판 데이터 로드
    await Promise.all([
      boardStore.fetchPosts('free'),
      boardStore.fetchPosts('info'),
      boardStore.fetchPosts('news')
    ])

    // 3. 프로필 데이터 로드
    await getProfile()

    // 4. 내 게시글 가져오기
    await fetchMyPosts()

    // 최종 레벨 계산
    await nextTick()
    calculateLevel()

    console.log('✅ 초기화 완료')
  } catch (error) {
    console.error('❌ 초기화 오류:', error)
  }
})

// 파일 선택 핸들러
const onFileChange = (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  // 파일 크기 체크 (5MB)
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    alert('파일 크기는 5MB 이하여야 합니다.')
    return
  }

  // 파일 타입 체크
  const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    alert('JPG, PNG, WEBP 형식의 이미지만 업로드 가능합니다.')
    return
  }

  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

// 프로필 수정
const handleUpdate = async () => {
  if (!editNickname.value.trim()) {
    alert('닉네임을 입력해주세요.')
    return
  }

  isLoading.value = true
  const formData = new FormData()
  formData.append('nickname', editNickname.value.trim())

  const fullDate = `${birthYear.value}-${birthMonth.value}-${birthDay.value}`
  formData.append('birth_date', fullDate)

  if (selectedFile.value) {
    formData.append('profile_image', selectedFile.value)
  }

  try {
    const res = await axios.put(
      `${authStore.API_URL}/api/accounts/profile/update/`,
      formData,
      {
        headers: {
          'Authorization': `Token ${authStore.token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    // 스토어 정보 갱신
    authStore.updateUserInfo(res.data)
    imageKey.value = Date.now()

    // 프로필 다시 로드
    await getProfile()

    isEditing.value = false
    previewUrl.value = null
    selectedFile.value = null

    alert('프로필이 수정되었습니다!')
  } catch (error) {
    console.error('프로필 수정 실패:', error)
    const errorMessage = error.response?.data?.nickname?.[0] ||
                        error.response?.data?.message ||
                        '프로필 수정에 실패했습니다.'
    alert(errorMessage)
  } finally {
    isLoading.value = false
  }
}

// 수정 모드 시작
const startEdit = () => {
  editNickname.value = profileData.value.nickname
  if (profileData.value.birth_date) {
    const parts = profileData.value.birth_date.split('-')
    birthYear.value = parts[0]
    birthMonth.value = parts[1]
    birthDay.value = parts[2]
  }
  isEditing.value = true
}

// 수정 취소
const cancelEdit = () => {
  isEditing.value = false
  previewUrl.value = null
  selectedFile.value = null

  // 미리보기 URL 메모리 해제
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
}

// 게시글로 이동
const goToPost = (boardType, postId) => {
  router.push({
    name: 'board-detail',
    params: {
      type: boardType,
      id: postId.toString()
    }
  })
}

// 상품 상세로 이동
const goToProductDetail = (type, productCode) => {
  const routeName = type === 'deposit' ? 'deposit-detail' : 'saving-detail'
  router.push({
    name: routeName,
    params: { id: productCode }
  })
}
</script>

<style scoped>
/* 기본 레이아웃 */
.profile-container {
  max-width: 950px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* 프로필 메인 카드 */
.profile-main-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  border: 1px solid #f0f0f0;
}

.card-bg {
  height: 110px;
  background: linear-gradient(135deg, #00a651 0%, #7ed957 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 40px;
}

.card-level-display {
  position: absolute;
  top: 20px;
  right: 30px;
}

.inline-level-tag-top {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 25px;
  font-weight: 700;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.inline-level-img-top {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.inline-level-name-top {
  font-weight: 800;
}

/* 레벨 테마 */
.inline-level-tag-top.lv-1 { color: #6b7280; }
.inline-level-tag-top.lv-2 { color: #059669; }
.inline-level-tag-top.lv-3 { color: #2563eb; }
.inline-level-tag-top.lv-4 { color: #9333ea; }
.inline-level-tag-top.lv-5 { color: #d97706; }

.user-content {
  padding: 0 40px 35px;
  display: flex;
  align-items: flex-start;
  gap: 30px;
  margin-top: -55px;
}

/* 아바타 */
.avatar-box {
  position: relative;
  width: 140px;
  height: 140px;
  flex-shrink: 0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 6px solid white;
  object-fit: cover;
  background: #f8f8f8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: filter 0.2s;
}

.editing-img {
  filter: brightness(0.6);
}

.camera-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.camera-overlay:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.camera-circle {
  font-size: 36px;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 사용자 상세 정보 */
.user-details {
  flex: 1;
  min-width: 0;
  padding-top: 55px;
}

.name-area {
  margin-bottom: 8px;
}

.user-nickname {
  font-size: 28px;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0;
}

.user-info-section {
  margin-top: 12px;
  padding-top: 12px;
}

.user-id {
  color: #888;
  margin: 0 0 10px 0;
  font-size: 14px;
}

.divider {
  margin: 0 8px;
  color: #ddd;
}

.user-birth {
  color: #666;
  font-size: 14px;
  margin: 0 0 15px 0;
}

.btn-toggle {
  background: white;
  border: 1px solid #00a651;
  color: #00a651;
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-block;
}

.btn-toggle:hover {
  background: #00a651;
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

/* 수정 폼 카드 */
.edit-form-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  border: 1px solid #f0f0f0;
}

.edit-form-header {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.edit-form-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: #1a1a1a;
}

/* 수정 입력 */
.edit-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 25px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.input-field {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Pretendard', sans-serif;
  outline: none;
  transition: border-color 0.2s;
}

.input-field:focus {
  border-color: #00a651;
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}

.picker-group {
  display: flex;
  gap: 10px;
}

.picker-select {
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  flex: 1;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  background: white;
  font-family: 'Pretendard', sans-serif;
  transition: border-color 0.2s;
}

.picker-select:focus {
  border-color: #00a651;
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}

.edit-actions-row {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 30px;
}

.btn-cancel {
  background: #f3f4f6;
  color: #666;
  border: none;
  padding: 14px 24px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover {
  background: #e5e7eb;
  color: #333;
}

.btn-save {
  background: #00a651;
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: #008e45;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 섹션 공통 스타일 */
.asset-section,
.community-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  border: 1px solid #f0f0f0;
}

.section-title {
  margin-bottom: 20px;
}

.section-title h3 {
  font-size: 20px;
  font-weight: 800;
  color: #1a1a1a;
  margin: 0;
}

/* 그리드 레이아웃 */
.asset-grid,
.community-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.asset-column,
.community-column {
  background: #fafafa;
  padding: 25px;
  border-radius: 18px;
  border: 1px solid #eee;
  transition: box-shadow 0.2s;
}

.asset-column:hover,
.community-column:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 800;
  font-size: 15px;
  border-bottom: 2px solid #e8e8e8;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.count-tag {
  color: #00a651;
  font-size: 14px;
  background: #f0fdf4;
  padding: 4px 10px;
  border-radius: 12px;
}

/* 상품 아이템 */
.product-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.product-item {
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #f5f5f5;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.product-item:hover,
.product-item:focus {
  border-color: #00a651;
  background: #f1fcf4;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 166, 81, 0.1);
  outline: none;
}

.bank {
  font-size: 11px;
  color: #00a651;
  font-weight: 700;
  text-transform: uppercase;
}

.title {
  font-size: 15px;
  font-weight: 700;
  margin-top: 4px;
  color: #333;
}

.info {
  font-size: 13px;
  color: #777;
  margin-top: 5px;
}

/* 게시글 아이템 */
.post-mini-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.post-mini-item {
  padding: 15px;
  border-radius: 12px;
  border: 1px solid #f5f5f5;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.post-mini-item:hover,
.post-mini-item:focus {
  border-color: #00a651;
  background: #f1fcf4;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 166, 81, 0.1);
  outline: none;
}

.post-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.post-badge {
  display: inline-block;
  background: #e5e7eb;
  color: #6b7280;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  width: fit-content;
}

.post-title {
  font-weight: 700;
  font-size: 14px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-date,
.post-author {
  font-size: 12px;
  color: #999;
}

.post-meta {
  font-size: 13px;
  color: #ff6b6b;
  font-weight: 600;
  white-space: nowrap;
}

/* 빈 상태 */
.empty-box {
  text-align: center;
  padding: 50px 20px;
  color: #ccc;
  border: 1px dashed #e8e8e8;
  border-radius: 15px;
  background: white;
  font-size: 14px;
}

/* 접근성 개선 */
.clickable {
  cursor: pointer;
}

.clickable:focus-visible {
  outline: 2px solid #00a651;
  outline-offset: 2px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .user-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 0 20px 25px;
  }

  .user-details {
    padding-top: 0;
  }

  .name-area {
    justify-content: center;
  }

  .asset-grid,
  .community-grid {
    grid-template-columns: 1fr;
  }

  .user-nickname {
    font-size: 24px;
  }

  .card-level-display {
    position: static;
    margin-bottom: 10px;
  }

  .picker-group {
    flex-direction: column;
  }
}

/* 프린트 스타일 */
@media print {
  .btn-toggle,
  .edit-actions-row {
    display: none;
  }
}
</style>
