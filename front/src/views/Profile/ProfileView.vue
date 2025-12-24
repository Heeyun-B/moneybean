<template>
  <div class="profile-container" v-if="profileData">
    <div class="profile-main-card">
      <div class="card-bg">
        <div class="card-level-display">
          <div class="inline-level-tag-top" :class="levelData.class">
            <img :src="levelData.imgUrl" class="inline-level-img-top" alt="레벨 아이콘" />
            <span class="inline-level-name-top">{{ levelData.name }}</span>
          </div>
        </div>
      </div>

      <div class="user-content">
        <div class="avatar-box">
          <img
            :src="displayImageUrl"
            :key="cacheBuster"
            class="user-avatar"
            :class="{ 'editing-img': isEditing }"
            @error="handleImageError"
            alt="프로필 이미지"
          />
          <label v-if="isEditing" for="file-input" class="camera-overlay">
            <div class="camera-circle"><span>📷</span></div>
          </label>
          <input
            id="file-input"
            type="file"
            @change="onFileChange"
            hidden
            accept="image/jpeg,image/png,image/webp"
          />
        </div>

        <div class="user-details">
          <template v-if="!isEditing">
            <div class="name-area">
              <h2 class="user-nickname">{{ profileData.nickname }}님</h2>
            </div>
            <div class="user-info-section">
              <p class="user-id">
                @{{ profileData.username }} 
                <span class="divider">|</span> 
                {{ profileData.email || '이메일 없음' }}
              </p>
              <p v-if="profileData.birth_date" class="user-birth">
                🎂 {{ formatBirthDate(profileData.birth_date) }}
              </p>
              <button class="btn-toggle" @click="startEdit">프로필 수정하기</button>
            </div>
          </template>
        </div>
      </div>
    </div>

    <div v-if="isEditing" class="edit-form-card">
      <div class="edit-form-header">
        <h3>프로필 수정</h3>
      </div>
      <div class="edit-inputs">
        <div class="input-group">
          <label class="input-label">닉네임</label>
          <input type="text" v-model="editNickname" class="input-field" maxlength="20" />
        </div>
        
        <div class="input-group">
          <label class="input-label">이메일</label>
          <input type="email" v-model="editEmail" class="input-field" placeholder="example@email.com" />
        </div>

        <div class="input-group">
          <label class="input-label">생년월일</label>
          <div class="picker-group">
            <select v-model="birthYear" class="picker-select">
              <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
            </select>
            <select v-model="birthMonth" class="picker-select">
              <option v-for="m in months" :key="m" :value="m">{{ m }}월</option>
            </select>
            <select v-model="birthDay" class="picker-select">
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

    <section class="asset-section" v-if="!isEditing">
      <div class="section-title"><h3>🏦 나의 가입 상품</h3></div>
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

    <section class="community-section" v-if="!isEditing">
      <div class="section-title"><h3>📝 커뮤니티 활동</h3></div>
      <div class="community-grid">
        <div class="community-column">
          <div class="column-header">
            <span>✍️ 내 게시글</span>
            <span class="count-tag">{{ myPosts.length }}</span>
          </div>
          <div v-if="myPosts.length > 0" class="post-mini-list">
            <article
              v-for="post in myPosts"
              :key="post.id"
              class="post-mini-item clickable"
              @click="goToPost(post.boardType || 'free', post.id)"
            >
              <div class="post-info">
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
              :key="post.id"
              class="post-mini-item clickable"
              @click="goToPost(post.boardType || 'free', post.id)"
            >
              <div class="post-info">
                <span class="post-title">{{ post.title }}</span>
                <span class="post-author">by {{ post.author || '익명' }}</span>
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

// 이미지 자산 Import (Vite 기준)
import defaultLogo from '@/assets/logo_bean.png'
import levelBeanImg from '@/assets/level_logos/level_bean.png'
import levelSproutImg from '@/assets/level_logos/level_sprout.png'
import levelBranchImg from '@/assets/level_logos/level_branch.png'
import levelTreeImg from '@/assets/level_logos/level_tree.png'
import levelMoneyTreeImg from '@/assets/level_logos/level_money_tree.png'

// 레벨 이미지 import
import levelBeanImg from '@/assets/level_logos/level_bean.png'
import levelSproutImg from '@/assets/level_logos/level_sprout.png'
import levelBranchImg from '@/assets/level_logos/level_branch.png'
import levelTreeImg from '@/assets/level_logos/level_tree.png'
import levelMoneyTreeImg from '@/assets/level_logos/level_money_tree.png'

const router = useRouter()
const authStore = useAuthStore()
const assetStore = useAssetStore()
const boardStore = useBoardStore()

// --- 상태 관리 ---
const profileData = ref(null)
const myPosts = ref([])
const likedPosts = ref([])
const isEditing = ref(false)
const isLoading = ref(false)
const cacheBuster = ref(Date.now())

// 레벨 데이터
const levelData = ref({ name: "콩", imgUrl: levelBeanImg, class: "lv-1" })

// 수정용 폼 데이터
const editNickname = ref('')
const editEmail = ref('')
const birthYear = ref('1995')
const birthMonth = ref('01')
const birthDay = ref('01')
const selectedFile = ref(null)
const previewUrl = ref(null)

// --- 날짜 관련 계산 ---
const years = Array.from({ length: 80 }, (_, i) => String(2025 - i))
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const days = computed(() => {
  const lastDay = new Date(parseInt(birthYear.value), parseInt(birthMonth.value), 0).getDate()
  return Array.from({ length: lastDay }, (_, i) => String(i + 1).padStart(2, '0'))
})

// --- 이미지 경로 처리 ---
const displayImageUrl = computed(() => {
  if (previewUrl.value) return previewUrl.value
  const baseImg = authStore.profileImage || profileData.value?.profile_image_url
  return baseImg ? `${baseImg}?t=${cacheBuster.value}` : defaultLogo
})

const handleImageError = (e) => { e.target.src = defaultLogo }

// --- 레벨 계산 로직 ---
const calculateLevel = () => {
  const balance = assetStore.netWorth || profileData.value?.total_balance || 0

  console.log('🎯 레벨 계산 - 현재 자산:', balance.toLocaleString(), '원')

  if (balance >= 100000000) {
    levelData.value = { name: "돈나무", imgUrl: levelMoneyTreeImg, class: "lv-5" }
  } else if (balance >= 80000000) {
    levelData.value = { name: "나무", imgUrl: levelTreeImg, class: "lv-4" }
  } else if (balance >= 50000000) {
    levelData.value = { name: "가지", imgUrl: levelBranchImg, class: "lv-3" }
  } else if (balance >= 10000000) {
    levelData.value = { name: "새싹", imgUrl: levelSproutImg, class: "lv-2" }
  } else {
    levelData.value = { name: "콩", imgUrl: levelBeanImg, class: "lv-1" }
  }

  console.log('✅ 레벨 결정:', levelData.value.name)
}

// 자산 변경 시 레벨 실시간 업데이트
watch(() => assetStore.netWorth, () => calculateLevel())

// --- 데이터 로드 ---
const fetchActivityData = async () => {
  // 게시판 데이터 로드 및 내가 쓴 글 필터링
  const types = ['free', 'info', 'news']
  await Promise.all(types.map(t => boardStore.fetchPosts(t)))
  
  const allPosts = []
  types.forEach(type => {
    const posts = boardStore.getPosts(type)
      .filter(p => p.author === authStore.userNickname)
      .map(p => ({ ...p, boardType: type }))
    allPosts.push(...posts)
  })
  myPosts.value = allPosts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  
  // 좋아요한 게시글
  likedPosts.value = boardStore.getLikedPosts().slice(0, 5)
}

const getProfile = async () => {
  try {
    const res = await axios.get(`${authStore.API_URL}/api/accounts/profile/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    profileData.value = res.data
    calculateLevel()
  } catch (err) {
    console.error('프로필 로드 실패:', err)
  }
}

onMounted(async () => {
  isLoading.value = true
  await assetStore.getAssets()
  await getProfile()
  await fetchActivityData()
  isLoading.value = false
})

// --- 수정 핸들러 ---
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('파일 크기는 5MB 이하여야 합니다.')
      return
    }
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const startEdit = () => {
  editNickname.value = profileData.value.nickname
  editEmail.value = profileData.value.email || ''
  if (profileData.value.birth_date) {
    const [y, m, d] = profileData.value.birth_date.split('-')
    birthYear.value = y; birthMonth.value = m; birthDay.value = d
  }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  previewUrl.value = null
  selectedFile.value = null
}

const handleUpdate = async () => {
  if (!editNickname.value.trim()) return alert('닉네임을 입력해주세요.')
  
  isLoading.value = true
  const formData = new FormData()
  formData.append('nickname', editNickname.value)
  formData.append('email', editEmail.value)
  formData.append('birth_date', `${birthYear.value}-${birthMonth.value}-${birthDay.value}`)
  if (selectedFile.value) formData.append('profile_image', selectedFile.value)

  try {
    const res = await axios.put(`${authStore.API_URL}/api/accounts/profile/update/`, formData, {
      headers: { 
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'multipart/form-data' 
      }
    })
    authStore.updateUserInfo(res.data)
    cacheBuster.value = Date.now()
    await getProfile()
    isEditing.value = false
    alert('프로필이 성공적으로 수정되었습니다!')
  } catch (err) {
    alert('수정 실패: ' + (err.response?.data?.message || '오류가 발생했습니다.'))
  } finally {
    isLoading.value = false
  }
}

// --- 유틸리티 ---
const formatDate = (d) => d ? d.split('T')[0] : ''
const formatBirthDate = (d) => {
  if (!d) return ''
  const date = new Date(d)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

const goToPost = (type, id) => router.push({ name: 'board-detail', params: { type, id: id.toString() } })
const goToProductDetail = (type, id) => router.push({ name: type === 'deposit' ? 'deposit-detail' : 'saving-detail', params: { id } })
</script>

<style scoped>
/* 전체 컨테이너 */
.profile-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: 'Pretendard', sans-serif;
  color: #333;
}

/* 프로필 카드 공통 */
.profile-main-card, .edit-form-card, .asset-section, .community-section {
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  margin-bottom: 30px;
  overflow: hidden;
}

/* 상단 배경 및 레벨 */
.card-bg {
  height: 120px;
  background: linear-gradient(135deg, #00a651 0%, #7ed957 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 30px;
}

.inline-level-tag-top {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.inline-level-img-top { width: 22px; height: 22px; }

/* 레벨별 색상 */
.lv-1 { color: #6b7280; } .lv-2 { color: #059669; } .lv-3 { color: #2563eb; }
.lv-4 { color: #9333ea; } .lv-5 { color: #d97706; }

/* 사용자 정보 영역 */
.user-content {
  padding: 0 40px 40px;
  display: flex;
  gap: 30px;
  margin-top: -60px;
}

.avatar-box {
  position: relative;
  width: 150px;
  height: 150px;
  flex-shrink: 0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 6px solid white;
  object-fit: cover;
  background: #f8f8f8;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.editing-img { filter: brightness(0.6); }

.camera-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.camera-circle { font-size: 32px; color: white; }

.user-details { flex: 1; padding-top: 70px; }
.user-nickname { font-size: 32px; font-weight: 800; margin: 0; }
.user-info-section { margin-top: 15px; border-top: 1px solid #eee; padding-top: 15px; }
.user-id { color: #888; font-size: 15px; margin-bottom: 8px; }
.divider { margin: 0 10px; color: #eee; }
.user-birth { color: #555; font-size: 15px; margin-bottom: 15px; }

/* 버튼 스타일 */
.btn-toggle {
  background: white;
  border: 1.5px solid #00a651;
  color: #00a651;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.3s;
}

.btn-toggle:hover { background: #00a651; color: white; }

/* 수정 폼 */
.edit-form-card { padding: 30px; }
.input-group { margin-bottom: 20px; }
.input-label { display: block; font-weight: 700; margin-bottom: 8px; font-size: 14px; }
.input-field, .picker-select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-family: inherit;
  transition: 0.2s;
}
.input-field:focus, .picker-select:focus { border-color: #00a651; outline: none; box-shadow: 0 0 0 3px rgba(0,166,81,0.1); }
.picker-group { display: flex; gap: 10px; }

.edit-actions-row { display: flex; gap: 10px; margin-top: 20px; }
.btn-save { background: #00a651; color: white; border: none; flex: 2; padding: 15px; border-radius: 12px; font-weight: 700; cursor: pointer; }
.btn-cancel { background: #f3f4f6; color: #666; border: none; flex: 1; padding: 15px; border-radius: 12px; font-weight: 700; cursor: pointer; }

/* 섹션 그리드 */
.section-title { padding: 25px 30px 0; }
.section-title h3 { font-size: 22px; font-weight: 800; margin: 0; }

.asset-grid, .community-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  padding: 25px 30px 30px;
}

.asset-column, .community-column {
  background: #fcfcfc;
  border-radius: 20px;
  padding: 20px;
  border: 1px solid #f0f0f0;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 800;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #eee;
}

.count-tag { color: #00a651; background: #e6f6ee; padding: 4px 10px; border-radius: 10px; font-size: 13px; }

/* 리스트 아이템 */
.product-item, .post-mini-item {
  background: white;
  padding: 16px;
  border-radius: 15px;
  border: 1px solid #eee;
  margin-bottom: 12px;
  transition: 0.2s;
}

.clickable { cursor: pointer; }
.clickable:hover {
  transform: translateY(-3px);
  border-color: #00a651;
  box-shadow: 0 6px 15px rgba(0,166,81,0.1);
}

.bank { font-size: 11px; color: #00a651; font-weight: 800; }
.title { font-weight: 700; margin-top: 4px; font-size: 16px; }
.info { font-size: 13px; color: #888; margin-top: 6px; }

.post-title { font-weight: 700; font-size: 15px; display: block; }
.post-date, .post-author { font-size: 12px; color: #aaa; margin-top: 4px; }
.post-meta { color: #ff6b6b; font-weight: 700; font-size: 13px; }

.empty-box {
  padding: 40px;
  text-align: center;
  color: #bbb;
  border: 1.5px dashed #eee;
  border-radius: 15px;
  background: white;
}

/* 반응형 */
@media (max-width: 768px) {
  .asset-grid, .community-grid { grid-template-columns: 1fr; padding: 20px; }
  .user-content { flex-direction: column; align-items: center; text-align: center; }
  .user-details { padding-top: 20px; }
  .card-level-display { position: static; margin-top: 10px; justify-content: center; display: flex; }
  .picker-group { flex-direction: column; }
}
</style>